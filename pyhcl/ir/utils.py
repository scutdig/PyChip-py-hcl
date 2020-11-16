INPUT = 0
OUTPUT = 1

# typ
SI = 2
PC = 3


def indent(string: str) -> str:
    return string.replace('\n', '\n  ')


def auto_mapping(ma, mb, typ):
    print(ma.io)
    print(mb.io)

    if typ == SI:
        for key in ma.io.value._ios:
            temp = key
            direction = INPUT

            # directions
            if isinstance(ma.io.value._ios[key], Input):
                pass
            else:
                direction = OUTPUT
            for _key in mb.io.value._ios:
                if temp == _key:
                    # match
                    match_direction = INPUT
                    if isinstance(mb.io.value._ios[_key], Input):
                        pass
                    else:
                        match_direction = OUTPUT

                    if direction != match_direction and ma.io.value._ios[key].typ.width == mb.io.value._ios[_key].typ.width:
                        print("match + " + key)

                        if direction == INPUT:
                            mb.io.value._ios[_key] <<= ma.io.value._ios[key]
                        else:
                            ma.io.value._ios[key] <<= mb.io.value._ios[_key]