#!/usr/bin/env python3
"""把正文里要用的每个数字算出来，避免手算出错。
输出：_work/numeric-results.txt
"""
import math

def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))

lines = []
def p(s=""):
    lines.append(str(s))

# ---------- ch03: x^2 在 x=3 处的平均变化率 ----------
p("【ch03】f(x)=x^2 在 x=3 处，取不同 h 的平均变化率 [f(3+h)-f(3)]/h：")
for h in (1.0, 0.5, 0.1, 0.01, 0.001):
    v = ((3 + h) ** 2 - 3 ** 2) / h
    p(f"  h={h:<6} -> {v:.6f}")
p("  理论极限 = 2x = 6")
p()

# ---------- ch07: sigmoid 数值 ----------
p("【ch07】sigmoid 数值表：")
p("  z      sigma(z)   sigma'(z)=sigma(1-sigma)")
for z in (-4, -2, -1, -0.5, 0, 0.4, 0.45, 1, 2, 4):
    s = sigmoid(z)
    p(f"  {z:>5}  {s:.6f}   {s*(1-s):.6f}")
p()

# ---------- ch08/ch11: 2-2-1 网络 ----------
x1, x2 = 1.0, 0.5
w11, w12, b1 = 0.5, -0.3, 0.1
w21, w22, b2 = 0.2, 0.8, -0.2
v1, v2, bo = 0.6, -0.4, 0.2
y = 1.0
eta = 0.5

z1 = w11 * x1 + w12 * x2 + b1
h1 = sigmoid(z1)
z2 = w21 * x1 + w22 * x2 + b2
h2 = sigmoid(z2)
zo = v1 * h1 + v2 * h2 + bo
yhat = sigmoid(zo)

p("【ch08】2-2-1 前向传播")
p(f"  z1 = {w11}*{x1} + ({w12})*{x2} + {b1} = {z1:.4f}")
p(f"  h1 = sigmoid({z1:.4f}) = {h1:.6f}")
p(f"  z2 = {w21}*{x1} + {w22}*{x2} + ({b2}) = {z2:.4f}")
p(f"  h2 = sigmoid({z2:.4f}) = {h2:.6f}")
p(f"  zo = {v1}*{h1:.6f} + ({v2})*{h2:.6f} + {bo} = {zo:.6f}")
p(f"  yhat = sigmoid({zo:.6f}) = {yhat:.6f}")
p()

p("【ch09】损失（平方误差，y=1）")
L = (yhat - y) ** 2
p(f"  L = ({yhat:.6f} - 1)^2 = {L:.6f}")
p()

p("【ch11】反向传播")
dL_dyhat = 2 * (yhat - y)
p(f"  dL/dyhat = 2({yhat:.6f} - 1) = {dL_dyhat:.6f}")
sig_zo = yhat * (1 - yhat)
p(f"  sigma'(zo) = yhat(1-yhat) = {sig_zo:.6f}")
d_o = dL_dyhat * sig_zo
p(f"  delta_o = dL/dyhat * sigma'(zo) = {d_o:.6f}")
p()
d_v1 = d_o * h1
d_v2 = d_o * h2
d_bo = d_o
p(f"  dL/dv1 = delta_o * h1 = {d_v1:.6f}")
p(f"  dL/dv2 = delta_o * h2 = {d_v2:.6f}")
p(f"  dL/dbo = delta_o = {d_bo:.6f}")
p()
sig_z1 = h1 * (1 - h1)
sig_z2 = h2 * (1 - h2)
d1 = d_o * v1 * sig_z1
d2 = d_o * v2 * sig_z2
p(f"  sigma'(z1) = h1(1-h1) = {sig_z1:.6f}")
p(f"  delta_1 = delta_o * v1 * sigma'(z1) = {d1:.6f}")
p(f"  sigma'(z2) = h2(1-h2) = {sig_z2:.6f}")
p(f"  delta_2 = delta_o * v2 * sigma'(z2) = {d2:.6f}")
p()
d_w11 = d1 * x1
d_w12 = d1 * x2
d_b1 = d1
d_w21 = d2 * x1
d_w22 = d2 * x2
d_b2 = d2
p(f"  dL/dw11 = delta_1 * x1 = {d_w11:.6f}")
p(f"  dL/dw12 = delta_1 * x2 = {d_w12:.6f}")
p(f"  dL/db1  = delta_1      = {d_b1:.6f}")
p(f"  dL/dw21 = delta_2 * x1 = {d_w21:.6f}")
p(f"  dL/dw22 = delta_2 * x2 = {d_w22:.6f}")
p(f"  dL/db2  = delta_2      = {d_b2:.6f}")
p()
p(f"【ch11】更新（eta={eta}）：新值 = 旧值 - eta * 梯度")
upd = [
    ("v1", v1, d_v1), ("v2", v2, d_v2), ("bo", bo, d_bo),
    ("w11", w11, d_w11), ("w12", w12, d_w12), ("b1", b1, d_b1),
    ("w21", w21, d_w21), ("w22", w22, d_w22), ("b2", b2, d_b2),
]
for name, old, g in upd:
    new = old - eta * g
    p(f"  {name:<4} {old:>8.3f} - {eta}*({g:.6f}) = {new:.6f}")
p()

# 更新后再前向一次，看损失变化
w11n = w11 - eta * d_w11
w12n = w12 - eta * d_w12
b1n = b1 - eta * d_b1
w21n = w21 - eta * d_w21
w22n = w22 - eta * d_w22
b2n = b2 - eta * d_b2
v1n = v1 - eta * d_v1
v2n = v2 - eta * d_v2
bon = bo - eta * d_bo
z1n = w11n * x1 + w12n * x2 + b1n
h1n = sigmoid(z1n)
z2n = w21n * x1 + w22n * x2 + b2n
h2n = sigmoid(z2n)
zon = v1n * h1n + v2n * h2n + bon
yhatn = sigmoid(zon)
Ln = (yhatn - y) ** 2
p("【ch11】更新一次后重新前向")
p(f"  h1 = {h1n:.6f}, h2 = {h2n:.6f}")
p(f"  yhat = {yhatn:.6f}")
p(f"  L = {Ln:.6f}  （原 {L:.6f}，减少 {L-Ln:.6f}）")
p()

# ---------- ch10: 梯度下降 L=(w-1)^2 ----------
p("【ch10】L(w)=(w-1)^2, dL/dw=2(w-1), 从 w=3 出发 eta=0.1")
w = 3.0
p("  初始 w=3.000  L=4.000")
for step in range(1, 7):
    g = 2 * (w - 1)
    w = w - 0.1 * g
    p(f"  第{step}步: 梯度={g:.4f}  w={w:.6f}  L={ (w-1)**2 :.6f}")
p()

p("【ch10】eta 过大的对照：eta=1.0，从 w=3 出发")
w = 3.0
for step in range(1, 6):
    g = 2 * (w - 1)
    w = w - 1.0 * g
    p(f"  第{step}步: 梯度={g:.4f}  w={w:.4f}  L={(w-1)**2:.4f}")
p()

# ---------- ch06: AND/OR/XOR 用阶跃 ----------
p("【ch06】感知机 w=(1,1), 阶跃 z>0 输出 1")
for label, (a, b) in [("AND b=-1.5", (1,1)), ("OR b=-0.5", (1,1))]:
    pass
p("  x1 x2 | z=1*x1+1*x2-1.5 (AND) | z=1*x1+1*x2-0.5 (OR) | XOR 期望")
for a, b in [(0,0),(0,1),(1,0),(1,1)]:
    z_and = a + b - 1.5
    z_or = a + b - 0.5
    p(f"  {a}  {b}  | {z_and:>10.1f} -> {1 if z_and>0 else 0}      | {z_or:>10.1f} -> {1 if z_or>0 else 0}     | {a ^ b}")
p()

# ---------- ch13: XOR 两层 ----------
p("【ch13】XOR 两层网络：h1=OR(w=1,1,b=-0.5), h2=AND(w=1,1,b=-1.5), 输出= h1 AND (NOT h2): w=(1,-1), b=-0.5")
for a, b in [(0,0),(0,1),(1,0),(1,1)]:
    h1v = 1 if (a + b - 0.5) > 0 else 0
    h2v = 1 if (a + b - 1.5) > 0 else 0
    zo = h1v - h2v - 0.5
    out = 1 if zo > 0 else 0
    p(f"  ({a},{b}) -> h1={h1v}, h2={h2v}, z={zo:>4.1f}, out={out}, 期望={a ^ b}")
p()

# 写出结果
out = "\n".join(lines)
with open("_work/numeric-results.txt", "w", encoding="utf-8") as f:
    f.write(out)
print(out)
