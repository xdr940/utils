import ctypes
dll = ctypes.cdll.LoadLibrary
lib = dll('./add_cpp.so')
lib2 = dll('./mul_c.so')
lib.add(2,3)
lib2.mul(4,5)