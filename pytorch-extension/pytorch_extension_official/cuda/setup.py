from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension,CppExtension
import os
import glob

# 头文件目录
library_dirs = os.path.dirname(os.path.abspath(__file__))
# 源代码目录
source_cuda = glob.glob(os.path.join(library_dirs, 'lltm_cuda','*.cu'))
source_cuda+=glob.glob(os.path.join(library_dirs, 'lltm_cuda','*.cpp'))


setup(
    name='lltm_cuda',
    ext_modules=[
        CUDAExtension('lltm_cuda',
                      sources = source_cuda,
                      library_dirs =[ library_dirs],
                      ),
    ],
    cmdclass={
        'build_ext': BuildExtension
    })
