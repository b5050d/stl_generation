import os
import io

from stl_generation.modules.process_byte_streams import cookie_cutter


def test_generate_stl():
    currdir = os.path.dirname(__file__)
    with open(currdir + "\\test_hawaii_white.bin", "rb") as f:
        data = f.read()

    response = cookie_cutter(data)
    assert type(response) is io.BytesIO
