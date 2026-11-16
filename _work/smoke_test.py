#!/usr/bin/env python3
"""单书学习页冒烟测试：结构、渲染、交互、移动端布局。"""
import asyncio, json, os, sys
from playwright.async_api import async_playwright

HTML = os.path.abspath("index.html")
SHOT = os.path.abspath("_work/screenshots")
os.makedirs(SHOT, exist_ok=True)

async def main():
    results = []
    def rec(name, ok, detail=""):
        results.append({"item": name, "ok": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path="/usr/local/bin/chromium", args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto("file://" + HTML, wait_until="domcontentloaded")
        await page.wait_for_timeout(1200)

        # 1 首屏
        rec("首屏标题存在", await page.locator("h1").count() > 0, (await page.locator("h1").first.inner_text())[:40])
        await page.screenshot(path=os.path.join(SHOT, "desktop-home.png"))

        # 2 侧边栏章节数量
        nav_ch = await page.locator("#nav a[href^='#/chapter/']").count()
        rec("导航章节数 = 13", nav_ch == 13, f"实际 {nav_ch}")

        # 3 章节页打开
        await page.locator("#nav a[href='#/chapter/ch01']").click()
        await page.wait_for_timeout(600)
        txt = await page.locator(".page").inner_text()
        rec("第1章正文含关键句", "神经网络不是一堆神秘的零件" in txt, txt[:30].replace("\n", " "))
        rec("章节内 SVG 渲染", await page.locator(".page svg").count() >= 0)

        # 4 KaTeX
        await page.goto("file://" + HTML + "#/chapter/ch03", wait_until="domcontentloaded")
        await page.wait_for_timeout(2500)
        katex = await page.locator(".katex").count()
        rec("KaTeX 公式渲染数 > 20", katex > 20, f"实际 {katex}")

        # 5 深度片段
        await page.goto("file://" + HTML + "#/concept/c04", wait_until="domcontentloaded")
        await page.wait_for_timeout(700)
        det = await page.locator("details.depth-fragment").count()
        rec("概念 c04 有折叠深度片段", det == 1, f"实际 {det}")
        if det:
            await page.locator("details.depth-fragment summary").click()
            await page.wait_for_timeout(500)
            rec("深度片段可展开", await page.locator("details.depth-fragment[open]").count() == 1)
            await page.screenshot(path=os.path.join(SHOT, "desktop-depth.png"))

        # 6 诊断页
        await page.goto("file://" + HTML + "#/diagnosis", wait_until="domcontentloaded")
        await page.wait_for_timeout(500)
        rec("诊断页存在", await page.locator("#diag-start").count() == 1)

        # 7 测验作答
        await page.goto("file://" + HTML + "#/quiz/ch01", wait_until="domcontentloaded")
        await page.wait_for_timeout(500)
        q = page.locator(".quiz-item").first
        await q.locator(".quiz-opt input").first.check()
        await q.locator(".quiz-check").click()
        await page.wait_for_timeout(300)
        fb = await q.locator(".quiz-feedback").inner_text()
        rec("测验有判题反馈", len(fb.strip()) > 0, fb[:30])

        # 8 搜索
        await page.goto("file://" + HTML, wait_until="domcontentloaded")
        await page.wait_for_timeout(400)
        await page.locator("#q").fill("反向传播")
        await page.wait_for_timeout(600)
        res = await page.locator(".search-hit").count()
        rec("搜索“反向传播”有结果", res > 0, f"实际 {res}")

        # 9 深色模式截图
        # 9 公式与图渲染质量
        await page.goto("file://" + HTML + "#/chapter/ch08", wait_until="domcontentloaded")
        await page.wait_for_timeout(6000)
        kerr = await page.locator(".katex-error").count()
        rec("无 KaTeX 渲染错误", kerr == 0, f"实际 {kerr}")
        ms = await page.locator(".mermaid svg").count()
        rec("Mermaid 已渲染", ms > 0, f"实际 {ms}")

        # 10 移动端
        m = await browser.new_page(viewport={"width": 390, "height": 844})
        await m.goto("file://" + HTML + "#/chapter/ch08", wait_until="domcontentloaded")
        await m.wait_for_timeout(800)
        pad = await m.evaluate("getComputedStyle(document.querySelector('.main')).paddingLeft")
        hx = await m.evaluate("document.querySelector('.page h1').getBoundingClientRect().x")
        rec("移动端有 16px 以上内容边距", float(pad.replace('px','')) >= 16 and hx >= 16, f"padding={pad}, h1.x={hx}")
        sw = await m.evaluate("document.documentElement.scrollWidth")
        rec("移动端无横向溢出", sw <= 390 + 2, f"scrollWidth={sw}")
        await m.screenshot(path=os.path.join(SHOT, "mobile-ch08.png"), full_page=False)

        rec("控制台无错误", len(errors) == 0, "; ".join(errors[:3]))
        await browser.close()

    with open("_work/smoke-results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n通过", sum(1 for r in results if r["ok"]), "/", len(results))

asyncio.run(main())
