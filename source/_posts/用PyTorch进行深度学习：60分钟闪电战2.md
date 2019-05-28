---
title: 用 PyTorch 进行深度学习：60 分钟闪电战——02.自动求导
date: 2019-05-28 16:59:40
tags: 
- 深度学习
- pytorch
---

![](用PyTorch进行深度学习：60分钟闪电战2/000.jpeg)

<!--more-->

> 请确保已经安装 torch 和 torchvision 包，之前的[我的安装过程](https://purenjie.github.io/2019/04/30/Linux-%E5%AE%89%E8%A3%85-CPU-%E7%89%88%E6%9C%AC-PyTorch/)可供参考
>
> 这基本上是 PyTorch 官方指导文档“60 分钟闪电战”的翻译版本，官方原版地址[在此](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)

# AUTOGRAD：自动求导

PyTorch 中所有神经网络的核心是 `autograd` 包。让我们首先简要地访问它，然后我们将去训练我们的第一个神经网络。

`autograd` 包提供 Tensors 上所有操作的自动求导方法。它是一个运行时定义的框架，这意味着你的反向传播是根据你代码运行的方式来定义的，因此每一轮迭代都可以各不相同。

以这些例子来讲，让我们用更简单的术语来看看这些特性。

## 张量（Tensor）

`torch.Tensor` 是这个包的核心类。如果将其属性 `.requires_grad` 设置为 `True`，则会开始跟踪其上的所有操作。完成计算后，你可以调用 `.backward()` 方法并自动计算所有梯度。计算的张量（tensor）的梯度将累积到 `.grad` 属性中。

要停止追踪张量（tensor）的历史记录，可以调用 `.detach()` 方法将其从计算历史记录中分离出来，并防止之后的计算被追踪。

为了防止追踪历史记录（和使用内存），你还可以使用 `withtorch.no_grad():` 包装代码块。在评估模型时，这一方法可能特别有用，因为模型可能有一些 `requires_grad` 属性为 `True` 的可训练参数，但我们不需要这些参数的梯度。

还有一个类对于自动求导实现非常重要 ——一个 `Function`。

`Tensor` 和 `Function` 互相连接并构建一个非循环图，这个非循环图记录了完整的张量计算历史。每个张量（tensor）都有一个 `.grad_fn` 属性，该属性引用已创建 Tensor 的 Function（除了用户创建的 Tensors  - 他们的 grad_fn 为 None）。

如果要计算导数，可以在 `Tensor`上调用 `.backward()` 方法。如果 `Tensor` 是一个标量（即它包含一个元素数据），则不需要为 `backward()` 方法指定任何参数，然而如果它有更多元素，你需要指定一个 `gradient` 参数，这个参数需要和张量的大小相同。

```python
import torch
```

创建一个张量(tensor)并设置 `requires_grad=True` 来追踪这个张量的计算

```python
x = torch.ones(2, 2, requires_grad=True)
print(x)
```

输出：

```python
tensor([[1., 1.],
        [1., 1.]], requires_grad=True)
```

进行一次张量（tensor）操作：

```python
y = x + 2
print(y)
```

输出：

```python
tensor([[3., 3.],
        [3., 3.]], grad_fn=<AddBackward0>)
```

`y` 作为这一次加法操作的结果，具有 `grad_fn` 属性。

```python
print(y.grad_fn)
```

输出：

```python
<AddBackward0 object at 0x7f4325b3a898>
```

对 `y ` 做更多的操作

```python
z = y * y * 3
out = z.mean()

print(z, out)
```

输出：

```python
tensor([[27., 27.],
        [27., 27.]], grad_fn=<MulBackward0>) tensor(27., grad_fn=<MeanBackward1>)
```

`.requires_grad_( ... )` 方法可以更改现有 Tensor  `requires_grad` 的布尔值。没有给出时 `requires_grad` 属性默认为  `False` 。

```python
a = torch.randn(2, 2)
a = ((a * 3) / (a - 1))
print(a.requires_grad)
a.requires_grad_(True)
print(a.requires_grad)
b = (a * a).sum()
print(b.grad_fn)
```

输出：

```python
False
True
<SumBackward0 object at 0x7f4325b3a7f0>
```

## 梯度

现在我们来使用反向传播。因为 `out` （`tensor(27., grad_fn=<MeanBackward1>)`）只包含一个标量，`out.backward()` 等价于 `out.backward(torch.tensor(1.))`.

```python
out.backward()
```

输出 d(out)/dx

```python
print(x.grad)
```

输出：

```python
tensor([[4.5000, 4.5000],
        [4.5000, 4.5000]])
```

你得到有一个值都是 4.5 的矩阵。不妨把张量 out 称为“o”。我们有 $o = \frac{1}{4}\sum_i z_i$，$z_i = 3(x_i+2)^2$，并且$z_i\bigr\rvert_{x_i=1} = 27$。因此，o 对 x 的偏导 $\frac{\partial o}{\partial x_i} = \frac{3}{2}(x_i+2)$，进而 $\frac{\partial o}{\partial x_i}\bigr\rvert_{x_i=1} = \frac{9}{2} = 4.5$

在数学上，如果你有一个向量值函数 $\vec{y}=f(\vec{x})$，那么 $\vec{y}$ 对于 $\vec{x}$ 的梯度是[雅可比矩阵（Jacobian matrix）](https://baike.baidu.com/item/%E9%9B%85%E5%8F%AF%E6%AF%94%E7%9F%A9%E9%98%B5)：

$$\begin{split}J=\left(\begin{array}{ccc}  \frac{\partial y_{1}}{\partial x_{1}} & \cdots & \frac{\partial y_{1}}{\partial x_{n}}\\  \vdots & \ddots & \vdots\\  \frac{\partial y_{m}}{\partial x_{1}} & \cdots & \frac{\partial y_{m}}{\partial x_{n}}  \end{array}\right)\end{split}$$

一般来说，`torch.autograd` 是用来计算 vector-Jacobian product（没有找到很好的中文翻译） 的工具。也就是说，对于给定任何向量 $v=\left(\begin{array}{cccc} v_{1} & v_{2} & \cdots & v_{m}\end{array}\right)^{T}​$ ，计算 $v^{T}\cdot J​$ 的结果。如果 $v​$ 恰好是标量函数 $l=g\left(\vec{y}\right)​$ 的梯度，也就是说，$v=\left(\begin{array}{ccc}\frac{\partial l}{\partial y_{1}} & \cdots & \frac{\partial l}{\partial y_{m}}\end{array}\right)^{T}​$ ，那么通过链式求导规则，the vector-Jacobian product 是 $\vec{x}​$ 对 $l​$ 的梯度：

$$\begin{split}J^{T}\cdot v=\left(\begin{array}{ccc}  \frac{\partial y_{1}}{\partial x_{1}} & \cdots & \frac{\partial y_{m}}{\partial x_{1}}\\  \vdots & \ddots & \vdots\\  \frac{\partial y_{1}}{\partial x_{n}} & \cdots & \frac{\partial y_{m}}{\partial x_{n}}  \end{array}\right)\left(\begin{array}{c}  \frac{\partial l}{\partial y_{1}}\\  \vdots\\  \frac{\partial l}{\partial y_{m}}  \end{array}\right)=\left(\begin{array}{c}  \frac{\partial l}{\partial x_{1}}\\  \vdots\\  \frac{\partial l}{\partial x_{n}}  \end{array}\right)\end{split}$$

（注意，$v^{T}\cdot J$ 给出了一个行向量，可以通过 $J^{T}\cdot v$ 将其视为列向量）

vector-Jacobian product 这种特性使得将外部梯度返回到具有非标量输出的模型中非常方便。

现在让我们看一下 vector-Jacobian product 的例子：

```python
x = torch.randn(3, requires_grad=True)

y = x * 2
print(y)
while y.data.norm() < 1000:
    y = y * 2
print(y)
```

输出：

```python
tensor([-0.6076,  0.2554, -0.9332], grad_fn=<MulBackward0>)
tensor([-622.2171,  261.5012, -955.5557], grad_fn=<MulBackward0>)
```

现在在这种情况下， `y` 不再是标量。`torch.autograd` 无法直接计算完整雅可比行列，但是如果我们只想要 vector-Jacobian product，只需通过 `backward` 将向量作为参数传入：

```python
v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float)
y.backward(v)

print(x.grad)
```

输出：

```
tensor([2.0480e+02, 2.0480e+03, 2.0480e-01])
```

你也可以通过使用 `with torch.no_grad():` 包装代码块来停止使用 `.requires_grad=True` 的张量通过追踪历史进行自动求导。

```python
print(x.requires_grad)
print((x ** 2).requires_grad)

with torch.no_grad():
    print((x ** 2).requires_grad)
```

输出：

```
True
True
False
```

**稍后阅读：** 

 `autograd` 和 `Function` 的文档位于 <https://pytorch.org/docs/autograd>

**参考阅读**

知乎高赞整合指导

[PyTorch深度学习：60分钟入门(Translation)](https://zhuanlan.zhihu.com/p/25572330)

Medium 对于autograd 的更详细容易理解的解释（推荐）

[PyTorch Autograd](https://towardsdatascience.com/pytorch-autograd-understanding-the-heart-of-pytorchs-magic-2686cd94ec95)





 