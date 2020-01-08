
[参考](https://pytorch.org/tutorials/advanced/cpp_extension.html#performance-on-gpu-devices)

files tree
```shell
cpp
├── jit.py
├── lltm
│   ├── __init__.py
│   └── lltm.py
├── lltm_cpp_dir
│   ├── lltm.cpp
│   └── lltm.h
├── perform_test_gpu.py
├── perform_test.py
├── readme.md
└── setup.py

```
command
```shell
cpp$ python setup.py build

```

files tree

```shell

.
├── build
│   ├── lib.linux-x86_64-3.6
│   │   └── lltm_cpp.cpython-36m-x86_64-linux-gnu.so #生成的共享库
│   └── temp.linux-x86_64-3.6
│       └── home
│           └── roit
│               └── aws
│                   └── utils
│                       └── pytorch_extension
│                           └── cpp
│                               └── lltm_cpp_dir
│                                   └── lltm.o
├── jit.py
├── lltm
│   ├── __init__.py
│   └── lltm.py
├── lltm_cpp_dir
│   ├── lltm.cpp
│   └── lltm.h
├── perform_test_gpu.py
├── perform_test.py
├── readme.md
└── setup.py

```

```shell
#共享库放到lltm python package里面去
cp build/lib.linux-x86_64-3.6/lltm_cpp.cpython-36m-x86_64-linux-gnu.so lltm

```

可以执行了.

