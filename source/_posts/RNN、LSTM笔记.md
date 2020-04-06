---
title: RNN、LSTM笔记
date: 2020-04-06 10:37:09
tags: NLP
categories: 李宏毅课程笔记
---

![head](RNN、LSTM笔记/head.jpg)

<!--more-->

# RNN

对于 Slot Filling 问题，需要识别出句子中的某些特定词，比如我要在十一月二号到台北去，识别出目的地是台北，时间是十一月二号。对词进行编码的方法可以采用 1-of-N encoding 和 word hashing 或者其他高级方法，词语表征成向量后丢到神经网络里判断词属于每个 slot 的概率，比如台北属于目的地的概率和属于时间的概率。

但是这种方法有很严重的问题，“我要在十一月二号到台北去”和“我要在十一月二号从台北走”用上述方法判断的目的地都是台北。因此需要 Neural Netowork 有“记忆”，引入 RNN（Recurrent Neural Network）。

隐藏层的输出会保存到记忆单元里供后面使用。RNN 在考虑 input 的 sequence 的时候，并非是 independent

也就是 RNN 会考虑 input sequence 的 order，所以任意调换 input 的顺序，他的 output 结果是不一样的。

![1586140035945](RNN、LSTM笔记/1586140035945.png)

考虑多个隐藏层的结构，深度网络。如果是将隐藏层的输出存储在记忆中称为 Elman Network，将输出层的输出值存储在记忆中就称为 Jordan Network。

双向(Bidirectional)RNN从顺逆两个方向上考虑。双向的好处是，我们在产生 output 时，我们不止有看了从句首到句尾这个方向，同时也看了句尾到句首的方向，这样双向的理解比较全面。

# LSTM

长短时记忆网络(Long Short-term Memory,LSTM)指的是具有多个长的短时间记忆网络。

![1586140012498](RNN、LSTM笔记/1586140012498.png)

其网络形状有四个输入，一个输出。

- 单纯把原本的 NN 换成 LSTM 就完成了和 Neural Network 的整合

![1586140057257](RNN、LSTM笔记/1586140057257.png)

![1586140068570](RNN、LSTM笔记/1586140068570.png)

换成 LSTM 后，因为有 4 个 input 所以比起一般的 NN，参数数量多四倍

- 对于简版的 LSTM，可以看成 xt 经过 transform 得到 zf , zi, z , zo 四个 vector 分别去控制 LSTM 四个参数，ct-1 代表 memory cell 裡面上一个时间点 t-1 的值

![1586140279459](RNN、LSTM笔记/1586140279459.png)

- 真正的 LSTM 还会把 hidden layer 的输出 h 接上，还会加上所谓的 “peephole” 就是把上一个时间点 memory cell 的值 ct-1 也接过来，再在经过不同的 transform 得到四个不同的 z vector 去控制 LSTM，LSTM 也不止一层，可以叠个五六层

![1586140369076](RNN、LSTM笔记/1586140369076.png)

Keras 有支援 LSTM，所以虽然架构超级複杂，但实作起来还算容易
GRU：简化版本的 LSTM 只有两个 Gate 参数比较少，比较不容易 overfitting

**参考链接**

[[ML筆記] Recurrent Neural Network (RNN) - Part I](http://violin-tao.blogspot.com/2017/12/ml-recurrent-neural-network-rnn-part-i.html)

[李宏毅机器学习2016 第二十二讲 循环神经网络RNN](https://zhuanlan.zhihu.com/p/33149238)
































