# 速查表

## 核心公式

| 场景 | 公式 |
|---|---|
| 一次函数 | $y=kx+b$ |
| 导数定义 | $f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$ |
| 幂函数导数 | $(x^n)'=nx^{n-1}$ |
| 链式法则 | $\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}$ |
| 点积 | $\mathbf{w}\cdot\mathbf{x}=\sum_i w_ix_i$ |
| 一层前向 | $\mathbf{z}=\mathbf{W}\mathbf{h}+\mathbf{b}$，$\mathbf{h}=\sigma(\mathbf{z})$ |
| sigmoid | $\sigma(z)=\frac{1}{1+e^{-z}}$ |
| sigmoid 导数 | $\sigma'(z)=\sigma(z)(1-\sigma(z))$ |
| ReLU | $\max(0,z)$ |
| 平方损失 | $L=(y-\hat{y})^2$ |
| 交叉熵 | $L=-[y\ln\hat{y}+(1-y)\ln(1-\hat{y})]$ |
| 梯度下降 | $\theta\leftarrow\theta-\eta\frac{\partial L}{\partial\theta}$ |
| 输出层 δ（平方） | $\delta_o=2(\hat{y}-y)\hat{y}(1-\hat{y})$ |
| 输出层 δ（交叉熵） | $\delta_o=\hat{y}-y$ |
| 隐藏层 δ | $\boldsymbol{\delta}_l=(\mathbf{W}_{l+1}^{\mathsf{T}}\boldsymbol{\delta}_{l+1})\odot\sigma'(\mathbf{z}_l)$ |
| 权重梯度 | $\frac{\partial L}{\partial\mathbf{W}_l}=\boldsymbol{\delta}_l\mathbf{h}_{l-1}^{\mathsf{T}}$ |
| 偏置梯度 | $\frac{\partial L}{\partial\mathbf{b}_l}=\boldsymbol{\delta}_l$ |

## 本教程网络的数值

| 量 | 值 |
|---|---|
| 输入 | $x_1=1.0$，$x_2=0.5$ |
| 隐藏打分 | $z_1=0.45$，$z_2=0.4$ |
| 隐藏输出 | $h_1=0.610639$，$h_2=0.598688$ |
| 输出打分 | $z_o=0.326908$ |
| 预测 | $\hat{y}=0.581007$ |
| 损失（$y=1$） | $0.175555$ |
| 输出层 $\delta_o$ | $-0.203998$ |
| 隐藏层 $\delta_1,\delta_2$ | $-0.029101$，$0.019605$ |
| 更新后损失 | $0.140693$ |

## 检查清单

**写代码前**

- 维度：$\mathbf{W}_l$ 是 $n_l\times n_{l-1}$，$\mathbf{b}_l$ 是 $n_l$ 维。
- 激活：隐藏层用什么、输出层用什么，先定。
- 损失：回归用平方，分类用交叉熵。

**训练中**

- 前向输出有没有 NaN：有就是数值溢出，检查 $\exp$ 的参数范围。
- 损失是否稳定下降：震荡查学习率，不降查梯度符号。
- 验证损失：每若干轮看一次，开始升就早停。

**反向传播手算**

- $\delta_o$ 先算，再往回递推。
- 每个 $\delta$ 都乘了 $\sigma'(z)$。
- 每个权重梯度都是"$\delta$ × 该权重的输入"。
- 更新方向：梯度为正，参数减小。

## 符号对照

| 符号 | 读法 | 含义 |
|---|---|---|
| $\sigma$ | sigma | sigmoid 函数，也常指数求和符号，按上下文区分 |
| $\sum$ | 求和 | 把下标范围内的项全加起来 |
| $\prod$ | 连乘 | 把下标范围内的项全乘起来 |
| $\partial$ | 偏导 | 只对一个变量求导，其余当常数 |
| $\nabla$ | nabla | 把所有偏导打包成向量 |
| $\odot$ | 逐元素乘 | 两个同形矩阵对应位置相乘 |
| $\mathsf{T}$ | 转置 | 行列互换 |
| $\delta$ | delta | 误差项，损失对打分的导数 |
| $\eta$ | eta | 学习率 |
