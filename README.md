# 神经网络：从一条直线推到反向传播

一套从初中数学起步、一路推到反向传播的交互学习页。单文件 `index.html`，双击就能打开；也可以直接放进 GitHub Pages。

## 打开方式

- 本地：双击 `index.html`，或拖进浏览器。
- 在线：<https://zrx-11.github.io/neural-net-zero/> （已部署在 GitHub Pages）。

公式用 KaTeX 渲染，流程图用 Mermaid，两者走 CDN。**离线时公式会显示源码，文字、导航、测验仍然可用。** 首次打开建议联网。

## 这里面有什么

| 模块 | 数量 | 说明 |
|---|---|---|
| 章节 | 13 | 从函数、斜率、导数，到前向传播、损失、梯度下降、反向传播 |
| 概念页 | 12 | 每个概念一句话定义、常见误解、在书中出现的脉络 |
| 深度推导 | 2 | 链式法则为什么是乘、反向传播的每一步；默认折叠 |
| 测验 | 32 | 单选、多选、填空，答错给解析 |
| 抽认卡 | 34 | 正面问题，背面答案 |
| 术语 | 55 | 按章节标注首现位置 |
| 学习路径 | 13 步 | 按依赖拓扑排序，每步带检查点 |

学习路径是主线，概念页是查漏补缺的索引，诊断测试会随机抽 5 题，答错时沿前置链倒推根因。

## 目录结构

```
神经网络-从零推透/
├── index.html              # 学习页（单文件，所有内容内联）
├── manifest.json           # 结构化清单：章节、概念、测验、卡片、术语
├── chapters/               # 13 章 Markdown 源文
├── concepts/               # 12 个概念页 + 2 个深度推导片段
├── patterns.md             # 模式库：拆解框架、决策规则、反模式
├── cheatsheet.md           # 速查表：公式、数值、检查清单
├── quiz.md                 # 测验的可读副本
├── flashcards.md           # 抽认卡的可读副本
├── glossary.md             # 术语表
├── README.md               # 本文件
├── 交付说明.md              # 交付与验证说明
├── .nojekyll               # 关闭 GitHub Pages 的 Jekyll
└── _work/                  # 过程产物（数值脚本、验证记录、截图）
```

`index.html` 是构建产物，内容全部内联。修改章节 Markdown 后需要重新构建：

```bash
python3 <知枢技能目录>/scripts/build_companion.py --manifest manifest.json --out index.html
```

## 部署到 GitHub Pages

当前已部署：仓库 [zrx-11/neural-net-zero](https://github.com/zrx-11/neural-net-zero)，线上地址 <https://zrx-11.github.io/neural-net-zero/>，分支 `main`、目录 `/(root)`。以下步骤供换账号或重建时参考。

第一次建仓：

```bash
cd 神经网络-从零推透
git init
git add .
git commit -m "神经网络学习页"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

然后在仓库 **Settings → Pages → Build and deployment**：

- Source 选 **Deploy from a branch**
- Branch 选 **main**，目录选 **/(root)**
- 保存后等 1～2 分钟

访问 `https://<你的用户名>.github.io/<仓库名>/`。如果仓库名本身是 `<用户名>.github.io`，访问 `https://<用户名>.github.io/`。

已有仓库时，把目录内容复制进仓库根目录，`git add . && git commit -m "update" && git push` 即可。

`.nojekyll` 必须保留，否则以 `_` 开头的目录可能被 Jekyll 忽略。

## 内容来源

全部为自撰推导，不是教材摘录。数值算例由 `_work/derive_numbers.py` 逐项计算，正文中的每个数都能在该脚本输出里对上。

## 已知限制

- 公式与流程图依赖 CDN，纯离线环境会降级为源码/提示，不影响阅读文字与做题。
- 进度存在浏览器 `localStorage`，换浏览器或清缓存会丢，可用页面顶部「导出进度 / 导入进度」迁移。
- 手工设计的异或网络用阶跃函数，只为验证表达力；实际训练需要可导的激活函数。
