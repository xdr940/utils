>通过setup来构建 c extension, 是一种C专门为python写拓展的方法，**得到的共享库C没法用的**

### 准备

files tree
```shell
test1
├── calc.c
├── python_test
│   ├── add_pkg
│   │   └── __init__.py
│   └── main.py
└── setup.py
```
files

```python
# setup.py
#from package import module.function
from distutils.core import setup, Extension
import setuptools
module1 = Extension('calc',#build处的模块名字
                    sources=['calc.c'])#源文件

#发布信息
setup(name='calc_model',
      version='1.0',
      description='Hello ?',
      ext_modules=[module1]
)

```

```c
//  calc.c
#include <Python.h>

int add(int x, int y){ // C 函数
    return x + y;
}

static PyObject *calc_add(PyObject *self, PyObject *args){

    int x, y;
    // Python传入参数
    // "ii" 表示传入参数为2个int型参数，将其解析到x, y变量中
    if(!PyArg_ParseTuple(args, "ii", &x, &y))
        return NULL;
    return PyLong_FromLong(add(x, y));
}

// 模块的方法列表
static PyMethodDef CalcMethods[] = {
     {"add", calc_add, METH_VARARGS, "函数描述"},
     {NULL, NULL, 0, NULL}
};

// 模块
static struct PyModuleDef calcmodule = {
    PyModuleDef_HEAD_INIT,
    "calc", // 模块名
    NULL, // 模块文档
    -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
    CalcMethods
};

// 初始化
PyMODINIT_FUNC PyInit_calc(void)
{
    return PyModule_Create(&calcmodule);
}

```
```python
#main.py
from add_pkg.calc import add
print(add(1,2))
```

command

```shell
python setup.py build
tree
```
```shell
.
├── build #新生成的文件夹
│   ├── lib.linux-x86_64-3.6
│   │   └── calc.cpython-36m-x86_64-linux-gnu.so
│   └── temp.linux-x86_64-3.6
│       └── calc.o
├── calc.c
├── python_test
│   ├── add_pkg
│   │   └── __init__.py
│   └── main.py
└── setup.py

5 directories, 6 files
```
把.so文件放到 add_package下面
```shell
.
├── build #新生成的文件夹
│   ├── lib.linux-x86_64-3.6
│   │   └── calc.cpython-36m-x86_64-linux-gnu.so
│   └── temp.linux-x86_64-3.6
│       └── calc.o
├── calc.c
├── python_test
│   ├── add_pkg
│   │   ├── __init__.py
│   │   └── calc.cpython-36m-x86_64-linux-gnu.so#这个文件可以重命名为calc.pyd
│   └── main.py
└── setup.py

5 directories, 7 files
```
conmmand

```shell
cd python_test
python main.py
>>3 #out
```

### 安装包

```shell
/test1
├── calc.c
├── python_test
│   ├── add_pkg
│   │   └── __init__.py
│   └── main.py
├── readme.md
└── setup.py



(base) roit@main:~/aws/utils/python_c_extension_test/test1$ python setup.py install# 包括了build
...

/test1
├── build
│   ├── bdist.linux-x86_64
│   ├── lib.linux-x86_64-3.7
│   │   └── calc.cpython-37m-x86_64-linux-gnu.so
│   └── temp.linux-x86_64-3.7
│       └── calc.o
├── calc.c
├── calc_model.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── dist
│   └── calc_model-1.0-py3.7-linux-x86_64.egg
├── python_test
│   ├── add_pkg
│   │   └── __init__.py
│   └── main.py
├── readme.md
└── setup.py

#get
site-package\
	|--calc_model-1.0-py3.6.egg-info
	|--calc.cpython-36m-x86_64-linux-gnu.so
```

```python
#main2.py
import calc.add as add
print(add(1,2))
```

或者

```shell
/test1
├── calc.c
├── python_test
│   ├── add_pkg
│   │   └── __init__.py
│   └── main.py
├── readme.md
└── setup.py

/test1$ python setup.py bdist_wheel

/test1
├── build
│   ├── bdist.linux-x86_64
│   ├── lib.linux-x86_64-3.7
│   │   └── calc.cpython-37m-x86_64-linux-gnu.so
│   └── temp.linux-x86_64-3.7
│       └── calc.o
├── calc.c
├── calc_model.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── dist
│   └── calc_model-1.0-cp37-cp37m-linux_x86_64.whl
├── python_test
│   ├── add_pkg
│   │   └── __init__.py
│   └── main.py
├── readme.md
└── setup.py


```



