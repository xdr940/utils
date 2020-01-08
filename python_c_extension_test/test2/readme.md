>该方法通过python调用纯c/cpp共享库(不是专门为python写的).so库

### 准备
files tree
```shell

test2
├── add_cpp.cpp
├── main.py
└── mul.c

```
files
```c
//mul_c.c
#include <stdio.h>
void mul(int a,int b){
    printf("result :%d",a*b);
}
```

```cpp
//add_cpp.cpp
#include <iostream>
extern "C"//修饰符，按照c的编译
void add(int a,int b){
    std::cout<<"the result:"<<a+b<<std::endl;
}
```

```python
#main.py
import ctypes
dll = ctypes.cdll.LoadLibrary
lib = dll('./add_cpp.so')
lib2 = dll('./mul_c.so')
lib.add(2,3)
lib2.mul(4,5)
```
### 编译 链接
command

```shell
gcc mul.c -fPIC -shared -o mul.so
g++ add_cpp.cpp -fPIC -shared -o add.so
tree
```
files tree
```shell
.
├── add_cpp.cpp
├── add.so #cpp生成的共享库
├── main.py
├── mul.c 
└── mul.so #c生成的共享库
```
### 运行
main.py
```shell
(pt) roit@main:~/aws/cdbws/python_c_extension_test/test2$ python main.py 
the result:5 #out
result :20
```

