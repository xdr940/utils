#include <torch/extension.h>
#include <vector>

// 前向传播
torch::Tensor forward_cpu(const torch::Tensor& inputA,
                            const torch::Tensor& inputB);
// 反向传播
std::vector<torch::Tensor> backward_cpu(const torch::Tensor& gradOutput);
