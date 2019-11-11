from io import BytesIO


def serialize_equal(serializable, target):
    output = BytesIO()
    serializable.serialize(output)
    output.flush()
    assert str(output.getvalue(), "utf-8") == target
    output.close()
