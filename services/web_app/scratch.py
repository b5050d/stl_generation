import os

a = os.getenv("DEVELOPMENT", "no")

print(a)

if a:
    print("ayye")
else:
    print("asdf")
