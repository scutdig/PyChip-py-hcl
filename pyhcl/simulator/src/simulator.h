#include <verilated.h>
#include <verilated_vcd_c.h>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <sys/mman.h>
#include <unistd.h>
#include <fcntl.h>
#include <vector>
#include <map>

using namespace std;

// Signals value
#define WAIT  0
#define DOUT  1
#define DIN   2
#define TERM  3
#define STEP  4
#define START 5
#define RESET 6

/* Simulation finish flag */
size_t is_exit = 0;

class DataWrapper
{
public:
    virtual void poke(uint64_t value) = 0;
    virtual uint64_t peek() = 0;
};

// Wrap Verilator data types
class CDataWrapper: public DataWrapper
{
private:
    CData *signal;
public:
    CDataWrapper(CData *_signal)
    {
        this->signal = _signal;
    }

    virtual void poke(uint64_t value)
    {
        uint64_t mask = 0xff;
        *signal = (CData) (mask & value);
    }

    virtual uint64_t peek()
    {
        return (uint64_t) *signal;
    }
};

class SDataWrapper: public DataWrapper
{
private:
    SData *signal;
public:
    SDataWrapper(SData *_signal)
    {
        this->signal = _signal;
    }

    virtual void poke(uint64_t value)
    {
        uint64_t mask = 0xffff;
        *signal = (SData) (mask & value);
    }

    virtual uint64_t peek()
    {
        return (uint64_t) *signal;
    }
};

class IDataWrapper: public DataWrapper
{
private:
    IData *signal;
public:
    IDataWrapper(IData *_signal)
    {
        this->signal = _signal;
    }

    virtual void poke(uint64_t value)
    {
        uint64_t mask = 0xffffffff;
        *signal = (IData) (mask & value);
    }

    virtual uint64_t peek()
    {
        return (uint64_t) *signal;
    }
};

class QDataWrapper: public DataWrapper
{
private:
    QData *signal;
public:
    QDataWrapper(QData *_signal)
    {
        this->signal = _signal;
    }

    virtual void poke(uint64_t value)
    {
        *signal = (QData) value;
    }

    virtual uint64_t peek()
    {
        return (uint64_t) *signal;
    }
};

template<class T> struct Sim_data
{
    vector<T> inputs;
    vector<T> outputs;
};

template<class T> class Simulator
{
protected:
    uint64_t *in;
    uint64_t *out;
    uint64_t *sig;
    Sim_data<T> sim_datas;
    uint64_t main_time;
    int in_fd;
    int out_fd;
    int sig_fd;

public:
    Simulator()
    {
        // Create file memory mapping
        this->in_fd = open("in.dat", O_RDWR | O_CREAT, 00777);
        this->out_fd = open("out.dat", O_RDWR | O_CREAT, 00777);
        this->sig_fd = open("sig.dat", O_RDWR | O_CREAT, 00777);

        int psize = getpagesize();
        ftruncate(this->in_fd, psize);
        ftruncate(this->out_fd, psize);
        ftruncate(this->sig_fd, psize);

        this->in = (uint64_t*)mmap(NULL, psize, PROT_WRITE | PROT_READ, MAP_SHARED, this->in_fd, 0);
        this->out = (uint64_t*)mmap(NULL, psize, PROT_WRITE | PROT_READ, MAP_SHARED, this->out_fd, 0);
        this->sig = (uint64_t*)mmap(NULL, psize, PROT_WRITE | PROT_READ, MAP_SHARED, this->sig_fd, 0);

        if (this->in == MAP_FAILED || this->out == MAP_FAILED || this->sig == MAP_FAILED)
        {
            perror("mmap failed");
            exit(1);
        }

        *(this->sig) = WAIT;    // Initial signal
        this->main_time = 0;
    }

    virtual void input_value(uint64_t *in)
    {
        int signal_num = (int)in[1];
        T obj = this->sim_datas.inputs[signal_num];
        obj->poke(in[0]);
    }

    virtual void output_value(uint64_t *out)
    {
        int signal_num = (int)out[1];
        T obj = this->sim_datas.outputs[signal_num];
        uint64_t wdata = obj->peek();
        out[0] = wdata;
    }

    virtual void step() = 0;
    virtual void reset() = 0;
    virtual void start() = 0;
    virtual void finish()
    {
        is_exit = 1;
    }

    bool isexit()
    {
        return is_exit;
    }

    void tick()
    {
        /* Signal ticks, deal with every incomming signal */

        // Waiting for signal
        while(1)
        {
            while (*sig == WAIT);

            switch (*sig)
            {
                case DIN: input_value(this->in); break;
                case DOUT: output_value(this->out); break;
                case STEP: step(); break;
                case RESET: reset(); break;
                case TERM: finish(); break;
                case START: start(); break;
                default: break;
            }

            if (is_exit)
                break;

            // Wait for next signal
            *sig = WAIT;
        }
    }
};
