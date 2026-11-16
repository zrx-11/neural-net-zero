# 深度推导：反向传播的每一步

第 11 章给了流程和数值。这一节把每一步的"为什么"补齐，并把标量公式推广到任意多层。读完你应该能对任何一个分层网络，写出它的反向传播公式。

## 一、问题摆清楚

网络有 $P$ 个参数。训练需要每个参数的偏导 $\partial L/\partial \theta_i$，一共 $P$ 个数。

**数值微分**的做法：固定其他参数，把 $\theta_i$ 加一个很小的 $h$，算两次损失，相除。每个参数要两次前向，总计算量约 $2P$ 次前向。$P=10^6$ 时就是两百万次前向，一次训练迭代都跑不完。

**反向传播**：一次前向 + 一次反向，计算量约是前向的 2 到 3 倍，与 $P$ 无关（只与网络的规模线性相关）。这是它能用的唯一理由。

## 二、把网络拆成计算图

任何网络都能拆成一串基本运算：乘、加、激活、损失。每个运算有两个方向：

- 前向：输入 $\to$ 输出，算出数值；
- 反向：已知"输出处的梯度"，算出"输入处的梯度"。

反向传播就是沿计算图倒着走，每经过一个运算，把传进来的梯度乘上这个运算的局部导数。

设某一层的计算是：

$$
\mathbf{z}=\mathbf{W}\mathbf{h}_{\text{prev}}+\mathbf{b},\qquad \mathbf{h}=\sigma(\mathbf{z})
$$

$\sigma$ 对向量逐元素作用。$\mathbf{h}_{\text{prev}}$ 是上一层的输出，$\mathbf{h}$ 是这一层的输出。

## 三、δ 是什么

定义：

$$
\boldsymbol{\delta}=\frac{\partial L}{\partial \mathbf{z}}
$$

它是一个向量，第 $j$ 个分量是 $\partial L/\partial z_j$。含义：这一层第 $j$ 个神经元在激活之前的打分变动一点点，损失变多少。

为什么盯住 $\mathbf{z}$ 而不是 $\mathbf{h}$？因为参数只出现在 $\mathbf{z}=\mathbf{W}\mathbf{h}_{\text{prev}}+\mathbf{b}$ 里，$\mathbf{h}$ 只是 $\mathbf{z}$ 经过激活的结果。把 $\mathbf{z}$ 的梯度算出来，参数的梯度就是一次乘法的事。

## 四、输出层

输出层的计算取决于损失函数。分两种。

### 平方损失 + sigmoid

$$
L=\frac{1}{2}(\hat{y}-y)^2,\qquad \hat{y}=\sigma(z_o)
$$

（这里加 $\frac{1}{2}$ 是为了让导数变成 $\hat{y}-y$，少一个常数因子，不影响最优位置。）

$$
\delta_o=\frac{\partial L}{\partial z_o}
=\frac{\partial L}{\partial \hat{y}}\cdot\frac{\partial \hat{y}}{\partial z_o}
=(\hat{y}-y)\cdot\hat{y}(1-\hat{y})
$$

第 11 章用的是不加 $\frac{1}{2}$ 的版本，所以前面多一个 2。两种写法等价，只差常数。

### 交叉熵 + sigmoid

$$
L=-\big[y\ln\hat{y}+(1-y)\ln(1-\hat{y})\big]
$$

对 $\hat{y}$ 求导：

$$
\frac{\partial L}{\partial \hat{y}}=-\frac{y}{\hat{y}}+\frac{1-y}{1-\hat{y}}
=\frac{\hat{y}-y}{\hat{y}(1-\hat{y})}
$$

乘以 $\hat{y}(1-\hat{y})$，两项约掉：

$$
\delta_o=\hat{y}-y
$$

这就是为什么分类任务喜欢"交叉熵 + sigmoid"：输出层的 $\delta$ 直接等于"预测减真实"，干净得不像话。平方损失配 sigmoid 会多出一个 $\hat{y}(1-\hat{y})$ 因子，当预测接近 0 或 1 时这个因子很小，梯度被压扁，学得慢。

## 五、隐藏层：δ 的递推

设第 $l$ 层的输出 $\mathbf{h}_l$ 喂给第 $l+1$ 层。第 $l+1$ 层的打分：

$$
\mathbf{z}_{l+1}=\mathbf{W}_{l+1}\mathbf{h}_l+\mathbf{b}_{l+1}
$$

$L$ 通过 $\mathbf{z}_{l+1}$ 依赖 $\mathbf{h}_l$。由链式法则：

$$
\frac{\partial L}{\partial \mathbf{h}_l}=\mathbf{W}_{l+1}^{\mathsf{T}}\boldsymbol{\delta}_{l+1}
$$

为什么是转置？$\mathbf{z}_{l+1}$ 是 $n_{l+1}$ 维，$\mathbf{h}_l$ 是 $n_l$ 维。$\partial \mathbf{z}_{l+1}/\partial \mathbf{h}_l$ 是一个 $n_{l+1}\times n_l$ 的矩阵，正好等于 $\mathbf{W}_{l+1}$（因为 $z_i=\sum_j W_{ij}h_j+b_i$，对 $h_j$ 的偏导就是 $W_{ij}$）。把梯度从 $n_{l+1}$ 维映回 $n_l$ 维，需要乘这个矩阵的转置。

再乘激活函数的导数：

$$
\boldsymbol{\delta}_l=\frac{\partial L}{\partial \mathbf{z}_l}
=\frac{\partial L}{\partial \mathbf{h}_l}\odot\sigma'(\mathbf{z}_l)
=\big(\mathbf{W}_{l+1}^{\mathsf{T}}\boldsymbol{\delta}_{l+1}\big)\odot\sigma'(\mathbf{z}_l)
$$

$\odot$ 是逐元素相乘。$\sigma'(\mathbf{z}_l)$ 是一个同样维数的向量，每个分量是 $\sigma'(z_j)$。

标量情况（一个神经元）就退化成第 11 章的公式：

$$
\delta_l=\delta_{l+1}\cdot w_{l+1}\cdot\sigma'(z_l)
$$

## 六、参数梯度

有了 $\boldsymbol{\delta}_l$，第 $l$ 层的参数梯度：

$$
\frac{\partial L}{\partial \mathbf{W}_l}=\boldsymbol{\delta}_l\mathbf{h}_{l-1}^{\mathsf{T}}
$$

$$
\frac{\partial L}{\partial \mathbf{b}_l}=\boldsymbol{\delta}_l
$$

形状检查：$\boldsymbol{\delta}_l$ 是 $n_l$ 维列向量，$\mathbf{h}_{l-1}^{\mathsf{T}}$ 是 $1\times n_{l-1}$ 行向量，乘出来是 $n_l\times n_{l-1}$，正好和 $\mathbf{W}_l$ 同形。

标量情况：$\partial L/\partial w=\delta\cdot h_{\text{prev}}$，$\partial L/\partial b=\delta$。和上一节一致。

## 七、数值算例（和正文同一组参数）

$$
x_1=1.0,\ x_2=0.5,\quad y=1
$$

$$
\mathbf{W}_1=\begin{bmatrix}0.5&-0.3\\0.2&0.8\end{bmatrix},\quad
\mathbf{b}_1=\begin{bmatrix}0.1\\-0.2\end{bmatrix}
$$

$$
\mathbf{W}_2=\begin{bmatrix}0.6&-0.4\end{bmatrix},\quad b_2=0.2
$$

**前向**：

$$
\mathbf{z}_1=\begin{bmatrix}0.45\\0.4\end{bmatrix},\quad
\mathbf{h}_1=\begin{bmatrix}0.610639\\0.598688\end{bmatrix}
$$

$$
z_2=0.326908,\quad \hat{y}=0.581007
$$

$$
L=(1-0.581007)^2=0.175555
$$

**输出层 δ**：

$$
\delta_2=2(\hat{y}-y)\hat{y}(1-\hat{y})=2(-0.418993)(0.243438)=-0.203998
$$

**输出层参数梯度**：

$$
\frac{\partial L}{\partial \mathbf{W}_2}=\delta_2\mathbf{h}_1^{\mathsf{T}}
=\begin{bmatrix}-0.124569&-0.122131\end{bmatrix}
$$

$$
\frac{\partial L}{\partial b_2}=-0.203998
$$

**隐藏层 δ**：

$$
\boldsymbol{\delta}_1=\big(\mathbf{W}_2^{\mathsf{T}}\delta_2\big)\odot\sigma'(\mathbf{z}_1)
$$

$$
\mathbf{W}_2^{\mathsf{T}}\delta_2=\begin{bmatrix}0.6\\-0.4\end{bmatrix}(-0.203998)
=\begin{bmatrix}-0.122399\\0.081599\end{bmatrix}
$$

$$
\sigma'(\mathbf{z}_1)=\begin{bmatrix}0.237759\\0.240261\end{bmatrix}
$$

$$
\boldsymbol{\delta}_1=\begin{bmatrix}-0.122399\times 0.237759\\0.081599\times 0.240261\end{bmatrix}
=\begin{bmatrix}-0.029101\\0.019605\end{bmatrix}
$$

**隐藏层参数梯度**：

$$
\frac{\partial L}{\partial \mathbf{W}_1}=\boldsymbol{\delta}_1\mathbf{x}^{\mathsf{T}}
=\begin{bmatrix}-0.029101\\0.019605\end{bmatrix}\begin{bmatrix}1.0&0.5\end{bmatrix}
=\begin{bmatrix}-0.029101&-0.014551\\0.019605&0.009803\end{bmatrix}
$$

$$
\frac{\partial L}{\partial \mathbf{b}_1}=\begin{bmatrix}-0.029101\\0.019605\end{bmatrix}
$$

和正文逐项对得上。矩阵写法一次算完一层，不用逐个神经元循环。

## 八、为什么反向传播这么快

前向时每个运算的输入输出都要存下来（激活值、打分值）。反向时每个 $\delta$ 只做一次矩阵乘和一次逐元素乘。总计算量：

$$
\text{前向}\approx \sum_l n_l n_{l-1},\qquad \text{反向}\approx 2\sum_l n_l n_{l-1}
$$

和参数数量同阶，不是平方。这就是它能扩展到几十层、上亿参数的原因。

代价是显存：训练时要保存每一层的中间值，batch 越大、层数越多，占用越高。梯度检查点（gradient checkpointing）就是拿计算换显存——不存全部中间值，反向时重算一部分。

## 九、四个常见错误

**错误一：忘记转置。** 隐藏层 $\delta$ 用 $\mathbf{W}^{\mathsf{T}}$，不是 $\mathbf{W}$。维度对不上会直接报错，但如果两层恰好同宽，错误会被掩盖，训练照跑但学不对。

**错误二：把激活函数的导数用错位置。** $\sigma'(\mathbf{z}_l)$ 用的是激活**之前**的打分 $\mathbf{z}_l$，不是输出 $\mathbf{h}_l$。sigmoid 恰好有 $\sigma'(z)=\sigma(z)(1-\sigma(z))=h(1-h)$，用 $h$ 算也行；换成 tanh 或别的函数，这个巧合就不成立。

**错误三：batch 的平均漏掉。** 一个 batch 有 $B$ 个样本，损失取平均，梯度也要按 $B$ 平均。漏了会让有效学习率变成原来的 $B$ 倍。

**错误四：更新时用了旧梯度。** 一个 batch 内，所有梯度要用同一组参数算出来，再统一更新。边算边更新会让后面的样本用上已变的参数，梯度不再对应同一个损失。

## 十、把整条链再走一遍

对任意层 $l$：

1. 前向：$\mathbf{z}_l=\mathbf{W}_l\mathbf{h}_{l-1}+\mathbf{b}_l$，$\mathbf{h}_l=\sigma(\mathbf{z}_l)$，一路到 $\hat{y}$ 和 $L$。
2. 输出层：$\boldsymbol{\delta}_{\text{out}}=\partial L/\partial \mathbf{z}_{\text{out}}$，按损失函数和激活函数的具体形式算。
3. 往回递推：$\boldsymbol{\delta}_l=\big(\mathbf{W}_{l+1}^{\mathsf{T}}\boldsymbol{\delta}_{l+1}\big)\odot\sigma'(\mathbf{z}_l)$。
4. 参数梯度：$\partial L/\partial \mathbf{W}_l=\boldsymbol{\delta}_l\mathbf{h}_{l-1}^{\mathsf{T}}$，$\partial L/\partial \mathbf{b}_l=\boldsymbol{\delta}_l$。
5. 更新：$\mathbf{W}_l\leftarrow\mathbf{W}_l-\eta\,\partial L/\partial \mathbf{W}_l$，$\mathbf{b}_l$ 同理。

这五步对全连接网络成立。换成卷积层，$\mathbf{W}$ 换成卷积核，"矩阵乘"换成卷积运算，链式法则的结构不变；换成注意力层，$\mathbf{W}$ 变成查询、键、值的投影矩阵，同样是一串局部导数相乘。

## 差生通读检查

- 用到的矩阵转置、逐元素乘、链式法则，前面都讲过。转置第一次作为"把梯度映回原维度"的工具出现，已经解释。
- 每一步都能自己补下一行：$\mathbf{W}_1$ 的梯度展开成了 $2\times 2$ 的四个数，没有跳步。
- 符号有白话：$\boldsymbol{\delta}$ 是"打分的梯度"，$\odot$ 是"对应位置相乘"，$\mathsf{T}$ 是"行列互换"。
- 给了"为什么"：为什么用转置（维度必须对上）、为什么反向快（计算量和参数同阶，不是平方）、为什么交叉熵配 sigmoid 干净（$\hat{y}-y$ 直接出来）。
