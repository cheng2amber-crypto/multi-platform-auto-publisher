# publishers/netease.py
from playwright.sync_api import sync_playwright
import os
import time

def publish_netease(content: str):
    lines = content.strip().split("\n", 1)
    title = lines[0].replace("标题：", "").strip() if lines[0].startswith("标题：") else lines[0]
    body = lines[1] if len(lines) > 1 else ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context_path = "cookies/netease.json"
        context = browser.new_context(storage_state=context_path) if os.path.exists(context_path) else browser.new_context()
        page = context.new_page()

        page.goto("https://mp.163.com/subscribe_v4/index.html#/article-publish")
        page.wait_for_load_state("networkidle")

        if "login" in page.url:
            raise Exception("未登录网易号，请先手动登录")

        page.fill('input[placeholder="请输入文章标题"]', title)
        time.sleep(2)

        # 网易使用 UEditor，需进入 iframe
        iframe = page.frame_locator("#ueditor_0").locator("body")
        if iframe.is_visible():
            iframe.click()
            page.keyboard.type(body, delay=50)

        page.click('button:has-text("发布")')
        time.sleep(3)

        context.storage_state(path=context_path)
        browser.close()
