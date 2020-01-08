from setuptools import setup
import os
import glob
from torch.utils.cpp_extension import BuildExtension, CppExtension

# 头文件目录 '/home/roit/aws/utils/pytorch_extension/cpp'
include_dirs = os.path.dirname(os.path.abspath(__file__))
# 源代码目录 <class 'list'>: ['/home/roit/aws/utils/pytorch_extension/cpp/lltm_cpp_dir/lltm.cpp']
source_cpu = glob.glob(os.path.join(include_dirs, 'lltm_cpp_dir', '*.cpp'))

setup(
    name='lltm_cpp',
	ext_modules=[
        CppExtension('lltm_cpp', sources=source_cpu, include_dirs=[include_dirs]),
    ],
    cmdclass={
        'build_ext': BuildExtension
    })
