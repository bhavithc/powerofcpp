from ctypes import cdll
lib = cdll.LoadLibrary("./build/libtest.so")
print("Temp:", lib.add(10, 20))


