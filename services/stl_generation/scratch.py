# if __name__ == "__main__":
#     hawaii_white = r"C:\Users\color\Workspace\stl_generation\services\stl_generation\tests\test_hawaii_white.bin"

#     with open(hawaii_white, "rb") as f:
#         data = f.read()

#     print(data[0:100])

import io

buffer = io.BytesIO()
buffer.write(b"Hello, world!")  # Write bytes
data_to_send = buffer.getvalue()
print(data_to_send)
