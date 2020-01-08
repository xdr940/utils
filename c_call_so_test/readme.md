# linux c调用动态链接共享库(shared library)

### 准备:
```shell
#tree
call_so_test/
├── main.c
├── call_so_test.h
├── test_a.c
├── test_b.c
└── test_c.c
```



test.h：
```c
#include <stdio.h>
void test_a();
void test_b();
void test_c();
```
test_a.c：
```c
#include "so_test.h"
void test_a()
{
  printf("this is in test_a...\n");
}
```

test_b.c：
```c
#include "so_test.h"
void test_b(){
    printf("this is in test_b...\n");
}
```
test_c.c
```c
#include "so_test.h"
void test_c(){
    printf("this is in test_c...\n");
    }
```
主函数
```c
//main.c
#include "call_so_test.h"
void main(){
	test_a();
	test_b();
	test_c();
}

```

### 编译 汇编 链接成.so
command
```shell
gcc test_a.c test_b.c test_c.c -fPIC -shared -o call_so_test.so
```
files tree
```shell
call_so_test/
├── main.c
├── call_so_test.h
├── call_so_test.so #生成的共享库
├── test_a.c
├── test_b.c
└── test_c.c

```

### 链接构建出可执行程序
command
```shell
gcc main.c -L. call_so_test.so -o test
```
files tree
```shell
call_so_test/
├── call_so_test.h
├── call_so_test.so
├── main.c
├── test #生成的可执行程序
├── test_a.c
├── test_b.c
└── test_c.c
```

 
 ### 动态库path添加
 
 >如果执行test的时候出现

```shell
(pt) roit@main:~/aws/cdbws/call_so_test$ ./test 
./test: error while loading shared libraries: call_so_test.so: cannot open shared object file: No such file or directory
```
当前目录不在共享库的查找范围内

command
```shell
echo $LD_LIBRARY_PATH #查看查找路径

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD #添加当前路径为查找路径

#输出
(pt) roit@main:~/aws/cdbws/call_so_test$ ./test 
this is in test_a...
this is in test_b...
this is in test_c...

```

> export方式在重启后失效，所以也可以用 vim /etc/bashrc ，修改其中的LD_LIBRARY_PATH变量。 　　
例如：LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/au1200_rm/build_tools/bin。


