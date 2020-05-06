#include "VAdder.h"
#include "simulator.h"
using namespace std;

class Adder_Simulator: public Simulator<DataWrapper*>
{
private:
    VAdder* dut;
    VerilatedVcdC *tfp;
    int psize;

public:
    Adder_Simulator(VAdder* _dut): Simulator()
    {
        this->dut = _dut;
        this->psize = getpagesize();
    }

    ~Adder_Simulator()
    {
        munmap(this->in, this->psize);
        munmap(this->sig, this->psize);
        munmap(this->out, this->psize);
        close(this->in_fd);
        close(this->out_fd);
        close(this->sig_fd);
        remove("./in.dat");
        remove("./sig.dat");
        remove("./out.dat");
    }

    void init_tfp(VerilatedVcdC *_tfp)
    {
        this->tfp = _tfp;
    }

    void init_simdata()
    {
        this->sim_datas.inputs.clear();
        this->sim_datas.outputs.clear();

		this->sim_datas.inputs.push_back(new CDataWrapper(&(dut->clock)));
		this->sim_datas.inputs.push_back(new CDataWrapper(&(dut->reset)));
		this->sim_datas.inputs.push_back(new CDataWrapper(&(dut->io_a)));
		this->sim_datas.inputs.push_back(new CDataWrapper(&(dut->io_b)));
		this->sim_datas.inputs.push_back(new CDataWrapper(&(dut->io_cin)));
		this->sim_datas.outputs.push_back(new CDataWrapper(&(dut->io_sum)));
		this->sim_datas.outputs.push_back(new CDataWrapper(&(dut->io_cout)));
	}

    virtual void step()
    {
        this->dut->clock = 0;
        this->dut->eval();
        this->tfp->dump(this->main_time);
        this->main_time++;

        this->dut->clock = 1;
        this->dut->eval();
        this->tfp->dump(this->main_time);
        this->main_time++;
    }

    virtual void reset()
    {
        this->dut->reset = 1;
        step();
    }

    virtual void start()
    {
        this->dut->reset = 0;
        step();
    }
};

int main(int argc, char **argv)
{
    Verilated::commandArgs(argc, argv);
    Verilated::traceEverOn(true);
    VAdder *top = new VAdder;
    VerilatedVcdC *tfp = new VerilatedVcdC;
    tfp = new VerilatedVcdC;
    top->trace(tfp, 99);
    tfp->open("Adder.vcd");
    Adder_Simulator sim(top);
    sim.init_simdata();
    sim.init_tfp(tfp);

    top->reset = 1;

    while(!sim.isexit())
        sim.tick();

    delete tfp;
    delete top;
    exit(0);
}        
        