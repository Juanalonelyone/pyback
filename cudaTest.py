# import torch
#
# # 检查PyTorch版本
# print(f"PyTorch 版本: {torch.__version__}")
#
# # 检查CUDA是否可用
# if torch.cuda.is_available():
#     device = torch.device("cuda")
#     print(f"CUDA 可用！")
#     print(f"CUDA 版本: {torch.version.cuda}")
#     print(f"CUDA 设备名称: {torch.cuda.get_device_name(0)}")
#     print(f"CUDA 设备名称: {torch.cuda.device_count()}")
# else:
#     device = torch.device("cpu")
#     print("CUDA 不可用！使用 CPU 运行。")
#
# # 创建一个随机张量并将其移动到设备上
# x = torch.rand(3, 3).to(device)
# print(f"张量 x 的设备: {x.device}")
#
# # 进行张量运算
# y = torch.matmul(x, x)
# print(f"结果张量 y: {y}")

import tensorflow as tf

print(tf.test.is_gpu_available)
print(tf.config.list_physical_devices('GPU'))
