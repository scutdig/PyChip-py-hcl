from io import BytesIO


def serialize_equal(serializable, target):
    output = BytesIO()
    serializable.serialize(output)
    output.flush()
    str_equal(str(output.getvalue(), "utf-8"), target)
    output.close()


def serialize_stmt_equal(serializable, target):
    output = BytesIO()
    serializable.serialize_stmt(output, 0)
    output.flush()
    str_equal(str(output.getvalue(), "utf-8"), target)
    output.close()


def str_equal(lf, rt):
    # for the more precise error report
    assert lf == rt
