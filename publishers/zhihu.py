# publishers/zhihu.py
from playwright.sync_api import sync_playwright
import os
import time

def publish_zhihu(content: str):
    lines = content.strip().split("\n", 1)
    title = lines[0].replace("标题：", "").strip() if lines[0].startswith("标题：") else lines[0]
    body = lines[1] if len(lines) > 1 else ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context_path = "cookies/zhihu.json"
        context = browser.new_context(storage_state=context_path) if os.path.exists(context_path) else browser.new_context()
        page = context.new_page()

        page.goto("https://zhuanlan.zhihu.com/write")
        page.wait_for_load_state("networkidle")

        if "signin" in page.url or "login" in page.url:
            raise Exception("未登录知乎，请先手动登录并保存状态")

        page.fill('input[placeholder="请输入专栏文章标题"]', title)
        time.sleep(1)

        editor = page.locator('div[contenteditable="true"]').first
        if editor.is_visible():
            editor.click()
            page.keyboard.type(body, delay=50)

        page.click('button.Button--blue:has-text("发布")')
        time.sleep(3)

        context.storage_state(path=context_path)
        browser.close()
