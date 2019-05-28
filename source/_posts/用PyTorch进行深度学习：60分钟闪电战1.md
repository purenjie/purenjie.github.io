---
title: 用 PyTorch 进行深度学习：60 分钟闪电战——01.什么是 PyTorch？
date: 2019-05-27 09:02:20
tags: 
- 深度学习
- pytorch
---

![](用PyTorch进行深度学习：60分钟闪电战1/000.jpeg)

<!--more-->

> 请确保已经安装 torch 和 torchvision 包，之前的[我的安装过程](https://purenjie.github.io/2019/04/30/Linux-%E5%AE%89%E8%A3%85-CPU-%E7%89%88%E6%9C%AC-PyTorch/)可供参考
> 这基本上是 PyTorch 官方指导文档“60 分钟闪电战”的翻译版本，官方原版地址[在此](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)

# 什么是 PyTorch？

这是一个基于 Python 的科学计算软件包，用于以下两种场景：

- NumPy 的替代品，可以使用 GPU 的强大功能
- 深入学习研究平台，提供最大的灵活性和速度

## 开始了解

### 张量（Tensors）

张量（Tensors）与 NumPy 的 ndarray 类似，除此之外张量（Tensors）也可用于 GPU 以加速计算。

```python
from __future__ import print_function
import torch
```

构造一个未初始化的 5x3 矩阵：

```python
x = torch.empty(5, 3)
print(x)
```

输出:

```python
tensor([[1.0895e+18, 3.0938e-41, 0.0000e+00],
        [0.0000e+00, 0.0000e+00, 0.0000e+00],
        [0.0000e+00, 0.0000e+00, 1.4013e-45],
        [0.0000e+00, 1.4013e-45, 0.0000e+00],
        [1.4013e-45, 0.0000e+00, 4.1123e+36]])
```

构造一个随机初始化的矩阵：

```python
x = torch.rand(5, 3)
print(x)
```

输出：

```python
tensor([[0.2505, 0.3974, 0.0744],
        [0.6448, 0.5842, 0.4680],
        [0.6063, 0.4385, 0.4689],
        [0.3561, 0.4130, 0.5176],
        [0.3285, 0.7430, 0.0147]])
```

构造一个用 0 填充的矩阵，并且矩阵元素的类型是 long 型

[torch.dtype 官方文档](https://pytorch.org/docs/stable/tensor_attributes.html#torch.torch.dtype)

```python
# torch.dtype 是表示 torch.Tensor 数据类型的一个对象
x = torch.zeros(5, 3, dtype=torch.long)
print(x)
```

输出：

```python
tensor([[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]])
```

直接从数据构造一个张量(tensor)：

```python
x = torch.tensor([5.5, 3])
print(x)
```

输出：

```python
tensor([5.5000, 3.0000])
```

或者根据现有的张量创建张量（tensor）。这些方法将复用**输入张量**的属性，例如 dtype 的属性，如果要修改属性需要在方法中设置新的属性

```python
x = x.new_ones(5, 3, dtype=torch.double)      # new_ * 方法采用大小
print(x)

x = torch.randn_like(x, dtype=torch.float)    # 重写 dtype！
print(x)                                      # 结果大小相同（5×3）
```

输出：

```python
tensor([[1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.],
        [1., 1., 1.]], dtype=torch.float64)
tensor([[-1.0728, -1.1668, -1.3842],
        [ 0.4314,  0.5510, -1.4960],
        [ 0.7383,  0.2974,  0.6049],
        [-0.0214, -0.5223,  1.3273],
        [ 0.9419, -0.0901,  1.1472]])
```

求得 x 的大小：

```python
print(x.size())
```

输出：

```python
torch.Size([5, 3])
```

> 注意
>
> `torch.Size` 实际上是一个元组（tuple），所以它支持所有的元组操作

### 对张量（tensor）进行操作

PyTorch 中有多种对张量操作的语法。在下面的示例中，我们来看一下加法操作

加法操作：语法 1

```python
y = torch.rand(5, 3)
print(x + y)
```

输出：

```python
tensor([[ 1.8656,  0.7212,  0.8959],
        [ 0.7013,  2.4756,  0.6954],
        [-0.4004,  0.1529,  0.1956],
        [ 1.2527,  1.0778,  1.1045],
        [ 1.6561,  1.3652,  1.8487]])
```

加法操作：语法 2

```python
print(torch.add(x, y))
```

输出：

```python
tensor([[ 1.8656,  0.7212,  0.8959],
        [ 0.7013,  2.4756,  0.6954],
        [-0.4004,  0.1529,  0.1956],
        [ 1.2527,  1.0778,  1.1045],
        [ 1.6561,  1.3652,  1.8487]])
```

加法操作：传入**输出张量**作为参数

```python
result = torch.empty(5, 3)
torch.add(x, y, out=result)
print(result)
```

输出：

```python
tensor([[ 1.8656,  0.7212,  0.8959],
        [ 0.7013,  2.4756,  0.6954],
        [-0.4004,  0.1529,  0.1956],
        [ 1.2527,  1.0778,  1.1045],
        [ 1.6561,  1.3652,  1.8487]])
```

加法操作：就地相加

```python
# 把 x 加到 y 上
y.add_(x)
print(y)
```

输出：

```python
tensor([[ 1.8656,  0.7212,  0.8959],
        [ 0.7013,  2.4756,  0.6954],
        [-0.4004,  0.1529,  0.1956],
        [ 1.2527,  1.0778,  1.1045],
        [ 1.6561,  1.3652,  1.8487]])
```

> 注意
>
> 任何就地调整张量的操作都是用 `_` 后固定的（也就是改变前面张量的值）。例如：`x.copy_(y)`, `x.t_() ` 都是改变 `x` 的值

你可以使用标准的 NumPy 索引及其相关操作

```python
print(x)
print(x[:, 1])  # 输出第 2 列
```

输出：

```python
tensor([[ 1.1219, -0.0120,  0.7449],
        [ 0.2799,  1.6878,  0.2842],
        [-1.2035,  0.0741, -0.3446],
        [ 0.8438,  0.3227,  0.5376],
        [ 0.9681,  0.5945,  0.9335]])

tensor([-0.0120,  1.6878,  0.0741,  0.3227,  0.5945])
```

调整大小：如果要调整/重塑张量大小，可以使用 `torch.view`:

```python
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)  # 大小 -1 是从其他维度推断出来的,在这里是 16÷8=2
print("x:", x)
print("y:", y)
print("z:", z)
print(x.size(), y.size(), z.size())
```

输出：

```python
x: tensor([[ 1.1114,  0.6949, -0.8329, -1.0590],
        [ 0.6232, -0.5550, -0.1172,  1.1504],
        [-0.5527, -0.2880,  1.9386,  0.5860],
        [-2.1687, -0.8960,  0.3042, -2.0107]])
y: tensor([ 1.1114,  0.6949, -0.8329, -1.0590,  0.6232, -0.5550, -0.1172,  1.1504,
        -0.5527, -0.2880,  1.9386,  0.5860, -2.1687, -0.8960,  0.3042, -2.0107])
z: tensor([[ 1.1114,  0.6949, -0.8329, -1.0590,  0.6232, -0.5550, -0.1172,  1.1504],
        [-0.5527, -0.2880,  1.9386,  0.5860, -2.1687, -0.8960,  0.3042, -2.0107]])
torch.Size([4, 4]) torch.Size([16]) torch.Size([2, 8])
```

如果你有一个只有一个元素的张量，使用 `.item()` 可以得到张量值作为 Python 的数字

```python
x = torch.randn(1)
print(x)
print(x.item())
```

输出：

```python
tensor([-0.9047])
-0.9046847820281982
```

**稍后阅读**

> 100 多个张量运算，包括转置，索引，切片，数学运算，线性代数，随机数等
>
> 详见：[torch 官方文档](https://pytorch.org/docs/stable/torch.html)

## NumPy 桥

将 Torch 的 Tensor 和 Numpy 的 array 相互转换简直就是洒洒水啦。

如果 Torch 的 Tensor 在 CPU 上，Torch 的 Tensor 和 NumPy 的 array 将共享内存中的存储位置，也就意味着更改其中一个将同时改变另一个。

### 将 Torch Tensor 转化为 NumPy Array

```python
a = torch.ones(5)
print(a)
```

输出：

```python
tensor([1., 1., 1., 1., 1.])
```

```python
b = a.numpy()
print(b)
```

输出：

```python
[1. 1. 1. 1. 1.]
```

观察 numpy 数组的值如何变化

```python
a.add_(1)
print(a)
print(b)
```

输出：

```python
tensor([2., 2., 2., 2., 2.])
[2. 2. 2. 2. 2.]
```

### 将 NumPy Array 转化为 Torch Tensor

观察更改 numpy array 的值如何自动更改 Torch 的 Tensor 值

```python
import numpy as np
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)
```

输出：

```python
[2. 2. 2. 2. 2.]
tensor([2., 2., 2., 2., 2.], dtype=torch.float64)
```

除了 CharTensor 之外，CPU 上的所有张量（Tensor）都可以转换为 Numpy 并且可以再转换回来

## 在 CUDA 上使用张量（Tensor）

[CUDA 百度百科](https://baike.baidu.com/item/CUDA) （英伟达显卡才可以使用 CUDA 进行训练，A 卡表示很难过）

通过调用 `.to` 方法，可以将张量移动到任何设备上（这里我无法使用 CUDA，因此用的官方结果代码）

```python
# 让我们只在 CUDA 可用的情况下运行下面的代码
# 我们将使用 torch.device 对象将张量放入和移出 GPU
if torch.cuda.is_available():
    device = torch.device("cuda")          # 一个 CUDA 设备对象
    y = torch.ones_like(x, device=device)  # 直接在 GPU 上创建一个张量
    x = x.to(device)                       # 或者直接使用 .to("cuda") 方法
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))       # .to() 方法可以同时改变 dtype 的类型
```

输出：

```python
tensor([0.1926], device='cuda:0')
tensor([0.1926], dtype=torch.float64)
```

 **参考阅读**

知乎高赞整合指导

[PyTorch深度学习：60分钟入门(Translation)](https://zhuanlan.zhihu.com/p/25572330)

