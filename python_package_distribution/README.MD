# python package distribution

### 文件建立
建立文件结构如下,工程根目录应该在packaging_tutorial，不然有问题

```shell

packaging_tutorial/
├── example_pkg# 包名字.包应该为二级文件夹
│   ├── __init__.py
│   ├── part_1.py
│   └── part_2.py
├── LICENSE
├── README.md
└── setup.py

1 directory, 6 files

```


```python
# __init__.py

from __future__ import absolute_import
from .part_1 import *
from .part_2 import *

name="example_pkg"
version='0.0.1'
```

```python
#part_1.py

def out():
    print('at example_pkg_out_test')

```
```python
#part_2.py

class testClass():
    __init__(self):
        print('at class init func')
```

```python
#setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example_pkg", # Replace with your own username
    version="0.0.1",
    author="WangDali",
    author_email="xdr94@126.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xdr940/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

```
LICENSE
````md
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

README.MD

```md
# Example Package
This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.
```


### 打包安装

安装setuptools, wheel, egg

wheel和,egg是打包工具

```shell

python3 -m pip install --user --upgrade setuptools wheel egg

```

```shell

python3 setup.py  bdist_wheel#打包成wheel格式

```
tree看下目录结构

```shell


packaging_tutorial/
├── build
│   ├── bdist.linux-x86_64
│   └── lib
│       └── example_pkg
│           ├── __init__.py
│           ├── part_1.py
│           └── part_2.py
├── dist
│   └── example_pkg-0.0.1-py3-none-any.whl #生成的wheel文件,解压后包含源码
├── example_pkg
│   ├── __init__.py
│   ├── part_1.py
│   └── part_2.py
├── example_pkg.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── LICENSE
├── README.md
└── setup.py

7 directories, 14 files

```

进入到.whl文件所在目录,安装

```shell

(pt) roit@main:~/aws/pythonWS/module/packaging_tutorial/dist$ pip install example_pkg-0.0.1-py3-none-any.whl 
Processing ./example_pkg-0.0.1-py3-none-any.whl
Installing collected packages: example-pkg
Successfully installed example-pkg-0.0.1
(pt) roit@main:~/aws/pythonWS/module/packaging_tutorial/dist$ 

```
发现site-package目录下多了俩文件

```shell
(base) roit@main:~/wkpgs/Anaconda3/envs/pt/lib/python3.6/site-packages$ ls -a|grep example
example_pkg_xdr94
example_pkg_xdr94-0.0.1.dist-info
```


### 测试

```python
#main.py
from  example_pkg.part_1 import out #module1 函数import
out()
from example_pkg.part_2 import testC #part_2 class import
a = testC()
from example_pkg import name #共用 字符串(变量)import
print(name)
from example_pkg import version
print(version)

```
输出

```shell

/home/roit/wkpgs/Anaconda3/envs/pt/bin/python /home/roit/aws/pythonWS/module/tests.py
at example_pkg_out_test
at init class
example_pkg
0.0.1

Process finished with exit code 0


```

### 上传

安装工具
```shell

pip install twine
```
注册PYPI后上传

```shell
(pt) roit@main:~/aws/pythonWS/module/packaging_tutorial$ cd dist/
(pt) roit@main:~/aws/pythonWS/module/packaging_tutorial/dist$ twine upload example_pkg_xdr94-0.0.1-py3-none-any.whl
Enter your username: xdr94
Enter your password:
Uploading distributions to https://upload.pypi.org/legacy/
Uploading example_pkg_xdr94-0.0.1-py3-none-any.whl
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6.10k/6.10k [00:09<00:00, 637B/s]

View at:
https://pypi.org/project/example-pkg-xdr94/0.0.1/
(pt) roit@main:~/aws/pythonWS/module/packaging_tutorial/dist$
```

网站[查看](https://pypi.org/manage/projects/)
