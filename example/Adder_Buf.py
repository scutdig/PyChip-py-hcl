from pyhcl import *


class Addr_Buffer(Module):
    io = IO(
        addr_input=Input(U.w(32)),
        flush=Input(Bool),
        record=Input(Bool),
        front=Output(U.w(32)),
    )

    buffer = Mem(3, U.w(32))
    counter = Mem(3, U.w(2))
    is_used = Mem(3, Bool)

    io.front <<= Mux(counter[U(0)] > counter[U(1)],
                     Mux(counter[U(0)] > counter[U(2)], buffer[U(0)], buffer[U(2)]),
                     Mux(counter[U(1)] > counter[U(2)], buffer[U(1)], buffer[U(2)]))

    write_index = Mux(is_used[U(0)] == U(0), U(0), Mux(is_used[U(1)] == U(0), U(1), U(2)))

    temp_used_list = []

    for i in range(0, 3):
        temp_used_list.append(Mux(io.record.to_bool(), Mux(write_index == U(i), Bool(1), is_used[U(i)]),
                                  is_used[U(i)]))

    for i in range(0, 3):
        is_used[U(i)] <<= Mux(io.flush.to_bool(), Bool(0), Mux(counter[U(i)] == U(2), Bool(0), temp_used_list[i]))

    for i in range(0, 3):
        counter[U(i)] <<= Mux(io.flush.to_bool(), U(0),
                              Mux(counter[U(i)] == U(2), U(0),
                                  Mux(is_used[U(i)], counter[U(i)] + U(1), counter[U(i)])))

    for i in range(0, 3):
        buffer[U(i)] <<= Mux(io.flush.to_bool(), U(0),
                             Mux(counter[U(i)] == U(2), U(0),
                                 Mux(io.record.to_bool(),
                                     Mux(write_index == U(i), io.addr_input, buffer[U(i)]), buffer[U(i)])))


def main():
    Emitter.dumpVerilog(Emitter.dump(Emitter.emit(Addr_Buffer()), "adder_buf.dir"))


if __name__ == '__main__':
    main()
