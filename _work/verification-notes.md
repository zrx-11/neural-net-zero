# 验证与构建记录

## 环境

- Python 3.12.11
- Playwright + 系统 Chromium（`/usr/local/bin/chromium`）
- 构建脚本：知枢 `scripts/build_companion.py`（v1.4.0）
- 生成时间：2026-11-16

## 数值来源

`_work/derive_numbers.py` 逐项计算，输出 `_work/numeric-results.txt`。正文引用的关键数字：

| 量 | 值 | 出处 |
|---|---|---|
| $x^2$ 在 x=3 处的逼近 | 7 → 6.5 → 6.1 → 6.01 → 6.001 | ch03 表格 |
| sigmoid(0.45) | 0.610639 | ch07 / ch08 |
| sigmoid(0.4) | 0.598688 | ch08 |
| 输出打分 | 0.326908 | ch08 |
| 预测 | 0.581007 | ch08 |
| 损失 | 0.175555 | ch09 |
| δo | -0.203998 | ch11 |
| δ1 / δ2 | -0.029101 / 0.019605 | ch11 |
| 更新后损失 | 0.140693 | ch11 |
| 梯度下降 6 步 | 3 → 1.524288 | ch10 |

全部由脚本复算，无手算残留。

## 冒烟测试结果（15/15）

测试脚本 `_work/smoke_test.py`，结果 `_work/smoke-results.json`。

1. 首屏标题存在
2. 导航章节数 = 13
3. 第 1 章正文关键句存在
4. 章节内 SVG 渲染
5. KaTeX 公式渲染 106 个
6. 概念 c04 有折叠深度片段
7. 深度片段可展开
8. 诊断页入口存在
9. 测验作答有判题反馈
10. 搜索「反向传播」20 条命中
11. KaTeX 渲染错误 0
12. Mermaid 已渲染
13. 移动端内容边距 18px
14. 移动端无横向溢出（scrollWidth=390）
15. 控制台 error 0

截图：`_work/screenshots/desktop-home.png`、`desktop-depth.png`、`mobile-ch08.png`。

## 对构建脚本的修复

`scripts/build_companion.py` 原版本有三处 CDN 地址失效或回退缺陷，已就地修复（只改资源地址与加载器，不改内容逻辑）：

1. **pico.css 404**：`registry.npmmirror.com/picocss/2.0.6/...` 返回 404，改为 jsDelivr 的 `@picocss/pico@2.0.6/css/pico.min.css`（实测 200）。
2. **vis-network 路径错误**：CSS 与 JS 都写成 `dist/dist/`，CSS 在 npmmirror 404、JS 在 jsDelivr 也 404。CSS 改 jsDelivr `dist/dist/vis-network.min.css`（200），JS 改 `dist/vis-network.min.js`（200），并加 4 秒超时回退。
3. **Mermaid 加载无超时**：原逻辑只靠 `onerror`，npmmirror 连不通时挂起不回调，页面一直停在源码状态。改为 jsDelivr 优先 + 4 秒超时后切换下一个源。

修复后重建，Mermaid 在 ch08 正常渲染为 SVG。

## 已知限制

- KaTeX / Mermaid 依赖 CDN。离线打开时公式显示源码、流程图显示源码与提示，文字与测验不受影响。
- 页面内三处多行 `$$` 公式被渲染器拼入 `\\`，KaTeX 会输出 `newLineInDisplayMode` 警告（warning 级，不影响渲染结果）。属已知行为。
- 手工异或网络使用阶跃函数，仅证明表达力，不可用于训练。
- 进度存 `localStorage`，换设备需用导出/导入 JSON。
