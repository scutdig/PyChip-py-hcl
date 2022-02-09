def indent(string: str) -> str:
    return string.replace('\n', '\n  ')


def backspace(string: str) -> str:
    return string.replace('\n  ', '\n')


def backspace1(string: str) -> str:
    return string if string[-3:-1] != '\n  ' else string[:-2]


def deleblankline(string: str) -> str:
    list = string.split("\n")
    lines = [line for line in list if line.strip()]
    return "\n".join(lines)


def auto_connect(ma, mb):
    from pyhcl import IO
    assert hasattr(ma, "value") and hasattr(mb, "value")
    assert type(ma.value) == IO and type(mb.value) == IO

    for (key_left, value_left) in ma.value._ios.items():
        for (key_right, value_right) in mb.value._ios.items():
            from pyhcl import Input, Output
            assert type(value_left) == Input or type(value_left) == Output
            assert type(value_right) == Input or type(value_right) == Output

            if key_left == key_right and type(value_left) != type(value_right):
                io_left = getattr(ma, key_left)
                io_right = getattr(mb, key_right)
                if type(value_left) == Input:
                    io_left <<= io_right
                else:
                    io_right <<= io_left
