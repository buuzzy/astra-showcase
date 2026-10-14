"""Astra 星系页面动画验收：连拍四个场景 + 读取粒子/帧率数据"""
import asyncio
from playwright.async_api import async_playwright

OUT = "/Users/nakocai/Documents/Projects/astra-review"

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto("file:///Users/nakocai/Documents/Projects/astra-review/index.html")
        await page.wait_for_timeout(4500)  # 等星系成形
        await page.screenshot(path=f"{OUT}/s1-开场静态.png")

        # 场景2：鼠标移到星系中心，引力扰动
        await page.mouse.move(720, 500)
        for i in range(12):  # 模拟鼠标滑动
            await page.mouse.move(720 + i * 8, 500 - i * 5, steps=2)
            await page.wait_for_timeout(60)
        await page.wait_for_timeout(700)
        await page.screenshot(path=f"{OUT}/s2-鼠标引力扰动.png")

        # 场景3：点击释放冲击波，抓爆炸瞬间和回归后
        await page.mouse.click(720, 500)
        await page.wait_for_timeout(350)
        await page.screenshot(path=f"{OUT}/s3-冲击波爆炸瞬间.png")
        await page.wait_for_timeout(2600)
        await page.screenshot(path=f"{OUT}/s4-粒子回归后.png")

        # 场景4：滚动到章节，镜头推近 + 标题逐字入场
        await page.mouse.wheel(0, 3000)
        await page.wait_for_timeout(2500)
        await page.screenshot(path=f"{OUT}/s5-滚动推近后.png")

        # 性能数据：帧率采样 + 页面状态
        fps = await page.evaluate("""() => new Promise(res => {
            let n = 0; const t0 = performance.now();
            function tick() { n++; if (performance.now() - t0 < 2000) requestAnimationFrame(tick); else res(Math.round(n / 2)); }
            requestAnimationFrame(tick);
        })""")
        info = await page.evaluate("() => ({w: innerWidth, dpr: devicePixelRatio, title: document.title})")
        print(f"实测帧率: {fps} fps | 视口: {info['w']}px | DPR: {info['dpr']} | 标题: {info['title']}")
        print(f"JS 报错: {errors if errors else '无'}")
        await browser.close()

asyncio.run(main())
