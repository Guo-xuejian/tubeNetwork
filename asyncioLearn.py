# import asyncio
# import time
#
#
# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)
#
#
# async def main():
#     task1 = asyncio.create_task(
#         say_after(1, "hello")
#     )
#     task2 = asyncio.create_task(
#         say_after(2, "world")
#     )
#     print(f"started at {time.strftime('%X')}")
#
#     # await say_after(1, 'hello')
#     # await say_after(2, 'world')
#     await task1
#     await task2
#
#     print(f"finished at {time.strftime('%X')}")
#
#
# asyncio.run(main())


import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto('http://quotes.toscrape.com/js/')
    await page.screenshot(path='example.png')
    await page.pdf(path='example.pdf')
    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
