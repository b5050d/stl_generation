import os
import io

from stl_generation.modules.process_byte_streams import cookie_cutter


def test_generate_stl():
    currdir = os.path.dirname(__file__)
    filepath = os.path.join(currdir, "test_hawaii_white.bin")
    with open(filepath, "rb") as f:
        data = f.read()

    response = cookie_cutter(data)
    assert type(response) is io.BytesIO
