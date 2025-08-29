import subprocess
import asyncio
import json
import os
from playwright.async_api import async_playwright
from ping3 import ping
import sys


# Определяем путь к браузеру Playwright
if getattr(sys, 'frozen', False):  # Если скрипт собран
    base_path = sys._MEIPASS  # Путь временного извлечения PyInstaller
    browser_path = os.path.join(base_path, 'ms-playwright', 'chromium-1148', 'chrome-win', 'chrome.exe')
else:
    browser_path = "C:\\Users\\SERG\\AppData\\Local\\ms-playwright\\chromium-1148\\chrome-win\\chrome.exe"

CONFIG_FILE = 'wifi_config.json'

def prompt_non_empty(prompt_message):
    """Prompt user input and ensure it is not empty."""
    while True:
        value = input(prompt_message).strip()
        if value:
            return value
        print("This field is required. Please enter a valid value.")

def create_config_file():
    print('Configuration file not found. Creating a new "wifi_config.json" file. Please enter configuration details:')

    target_ssid = prompt_non_empty('Enter Wi-Fi network name (Example_WIFI): ')
    login_page_url = prompt_non_empty('Enter login page URL (http://123.456.7.8/login): ')
    username = prompt_non_empty('Enter username (login): ')
    password = prompt_non_empty('Enter password (password): ')
    status_url = input('Enter status check URL (http://123.456.7.8/status (not required)): ').strip()
    debug_mode = input('Enable debug mode? (yes/no): ').strip().lower() == 'yes'

    config_data = {
        "target_ssid": target_ssid,
        "login_page_url": login_page_url,
        "username": username,
        "password": password,
        "status_url": status_url if status_url else None,
        "debug_mode": debug_mode
    }

    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print('Configuration file "wifi_config.json" successfully created.')

def load_config():
    if not os.path.exists(CONFIG_FILE):
        create_config_file()
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

def check_internet_connection():
    print("Checking internet connection with ping...")
    try:
        response = ping("8.8.8.8", timeout=1.5)
        if response is not None:
            print("Internet is available.")
            return True
        else:
            print("Internet is not available.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def check_current_connection():
    print("Checking current connection...")
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='cp866')
        ssid_match = next((line for line in result.splitlines() if "SSID" in line and "BSSID" not in line), None)
        if ssid_match:
            current_ssid = ssid_match.split(':')[1].strip()
            print(f"Current connection: {current_ssid}")
            return current_ssid
        else:
            print("No active connection.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error checking connection: {e}")
        return None

def connect_to_wifi(ssid):
    print(f"Attempting to connect to Wi-Fi network: {ssid}...")
    try:
        subprocess.check_output(['netsh', 'wlan', 'connect', f'name={ssid}'], encoding='cp866')
        print(f"Successfully connected to Wi-Fi network: {ssid}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error connecting: {e}")
        return False

async def login_to_portal(url, username, password, status_url=None, debug_mode=False):
    print(f"Opening browser for login at {url}...")

    if check_internet_connection():
        print("Internet is available. No login required.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=browser_path, headless=not debug_mode)
        # browser = await p.chromium.launch(
        #     executable_path="browsers\\chrome-win\\chrome.exe",
        #     headless=not debug_mode
        # )
        page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        current_url = page.url

        if status_url and current_url.startswith(status_url):
            print("Already logged in. No further actions required.")
            await browser.close()
            return

        print("Filling in username...")
        await page.wait_for_selector('input[name="username"]:not([type="hidden"])', state='visible')
        await page.fill('input[name="username"]:not([type="hidden"])', username)

        print("Filling in password...")
        await page.wait_for_selector('input[name="password"]:not([type="hidden"])', state='visible')
        await page.fill('input[name="password"]:not([type="hidden"])', password)

        print("Submitting form...")
        try:

            if await page.query_selector('input[type="submit"]'):
                await page.click('input[type="submit"]')
                print("Clicked on input")

            elif await page.query_selector('button[type="submit"]'):
                await page.click('button[type="submit"]')
                print("Clicked on button")
            else:
                print("No submit button found on the page.")
        except Exception as e:
            print(f"Failed to click the submit button: {e}")

        await page.wait_for_load_state('networkidle')
        current_url = page.url


        if status_url and current_url.startswith(status_url):
            print("Login successful; redirected to status page.")
        elif check_internet_connection():
            print("Login successful; internet is now available.")
        else:
            print("Login failed; internet is still unavailable or no redirect occurred.")

        await browser.close()


async def main():
    config = load_config()
    target_ssid = config['target_ssid']
    login_page_url = config['login_page_url']
    username = config['username']
    password = config['password']
    status_url = config.get('status_url')
    debug_mode = config.get('debug_mode', False)

    internet_available = check_internet_connection()
    if internet_available:
        print("Internet is available. Code will not be executed.")
        return

    current_ssid = check_current_connection()
    if current_ssid == target_ssid:
        print(f"You are already connected to the Wi-Fi network: {target_ssid}")
        await login_to_portal(login_page_url, username, password, status_url, debug_mode)
    else:
        print(f"You are not connected to the network {target_ssid}. Connecting to network {target_ssid}...")
        connected = connect_to_wifi(target_ssid)
        if connected:
            await login_to_portal(login_page_url, username, password, status_url, debug_mode)

if __name__ == "__main__":
    config = load_config()
    debug_mode = config.get('debug_mode', False)

    asyncio.run(main())
    
    if debug_mode:
        input("\nPress any key to close the console...") 
