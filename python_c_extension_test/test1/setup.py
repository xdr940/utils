# setup.py
#from package import module.function
import setuptools
from distutils.core import setup, Extension

module1 = Extension('calc',#build处的模块名字
                    sources=['calc.c'])#源文件

#发布信息
setup(name='calc_model',
      version='1.0',
      description='Hello ?',
      ext_modules=[module1]
)
