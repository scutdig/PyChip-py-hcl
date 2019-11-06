import py_hcl


def test_addition():
    assert 4 == py_hcl.add(2, 2)


def test_subtraction():
    assert 2 == py_hcl.subtract(4, 2)
