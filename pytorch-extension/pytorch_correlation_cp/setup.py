from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
from os.path import join

project_root = 'Correlation_Module'
sources = [join(project_root, file) for file in ['correlation.cpp',
                                                 'correlation_sampler.cpp',
                                                 'correlation_cuda_kernel.cu']]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='spatial_correlation_sampler',
    version="0.1.0",
    author="Clement Pinard",
    author_email="clement.pinard@ensta-paristech.fr",
    description="Correlation module for pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ClementPinard/Pytorch-Correlation-extension",
    install_requires=['torch>=1.0.1','numpy'],
    ext_modules=[
        CUDAExtension('spatial_correlation_sampler_backend',
                      sources,
                      extra_compile_args={'cxx': ['-fopenmp'], 'nvcc':[]},
                      extra_link_args=['-lgomp'])
    ],
    package_dir={'': project_root},
    packages=['spatial_correlation_sampler'],
    cmdclass={
        'build_ext': BuildExtension
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ])
