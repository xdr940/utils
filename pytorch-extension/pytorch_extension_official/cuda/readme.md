
 - 文件与函数

```shell
lltm_cuda
 ├── lltm_cuda.cpp
 └── lltm_cuda_kernel.cu
```  
 - 函数调用

```shell
std::vector<torch::Tensor> lltm_forward( #.cpp, cpu, only check inputs
  ├── lltm_cuda_forward #.cu cpu warper function
  │   ├── __global__ void lltm_cuda_forward_kernel #.cu gpu
```
