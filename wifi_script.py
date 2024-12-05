import subprocess
import asyncio
import json
import os
from playwright.async_api import async_playwright
import socket

CONFIG_FILE = 'wifi_config.json'

def create_config_file():
    print('Конфигурационный файл не найден. Создание нового файла "wifi_config.json". Пожалуйста, введите данные для конфигурации:')
    target_ssid = input('Введите имя Wi-Fi сети (Exemple_WIFI): ')
    login_page_url = input('Введите URL страницы логина (http://123.456.7.8/login): ')
    username = input('Введите логин пользователя (login): ')
    password = input('Введите пароль (password): ')

    config_data = {
        "target_ssid": target_ssid,
        "login_page_url": login_page_url,
        "username": username,
        "password": password
    }

    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print('Конфигурационный файл "wifi_config.json" успешно создан.')

def load_config():
    if not os.path.exists(CONFIG_FILE):
        create_config_file()
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

def check_internet_connection():
    print("\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0438\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u0441\u043e\u0435\u0434\u0438\u043d\u0435\u043d\u0438\u044f...")
    try:
        socket.setdefaulttimeout(1.5)
        socket.create_connection(("8.8.8.8", 53))
        print("\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d.")
        return True
    except OSError:
        print("\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d.")
        return False

def check_current_connection():
    print("\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0442\u0435\u043a\u0443\u0449\u0435\u0433\u043e \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f...")
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='cp866')
        ssid_match = next((line for line in result.splitlines() if "SSID" in line and "BSSID" not in line), None)
        if ssid_match:
            current_ssid = ssid_match.split(':')[1].strip()
            print(f"\u0422\u0435\u043a\u0443\u0449\u0435\u0435 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435: {current_ssid}")
            return current_ssid
        else:
            print("\u041d\u0435\u0442 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0433\u043e \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f: {e}")
        return None

def connect_to_wifi(ssid):
    print(f"\u041f\u043e\u043f\u044b\u0442\u043a\u0430 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f \u043a Wi-Fi \u0441\u0435\u0442\u0438: {ssid}...")
    try:
        subprocess.check_output(['netsh', 'wlan', 'connect', f'name={ssid}'], encoding='cp866')
        print(f"\u0423\u0441\u043f\u0435\u0448\u043d\u043e\u0435 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a Wi-Fi \u0441\u0435\u0442\u0438: {ssid}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f: {e}")
        return False

async def login_to_portal(url, username, password):
    print(f"\u041e\u0442\u043a\u0440\u044b\u0442\u0438\u0435 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0430 \u0434\u043b\u044f \u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u0438 \u043d\u0430 {url}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(url)

        print("\u0417\u0430\u043f\u043e\u043b\u043d\u044f\u0435\u043c \u043b\u043e\u0433\u0438\u043d...")
        await page.fill('input[name="username"]', username)

        print("\u041f\u0435\u0440\u0435\u0448\u043b\u0438 \u043a \u043f\u043e\u043b\u044e \u043f\u0430\u0440\u043e\u043b\u044f...")
        await page.fill('input[name="password"]', password)

        print("\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u043c \u0444\u043e\u0440\u043c\u0443...")
        await page.click('button[type="submit"]')

        await page.wait_for_load_state('networkidle')
        current_url = page.url

        if current_url.startswith('http://10.5.50.1/status'):
            print('Уже залогинено.')
            await browser.close()
            return

        if current_url != url:
            print("\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f \u0443\u0441\u043f\u0435\u0448\u043d\u0430, \u043f\u0440\u043e\u0438\u0437\u043e\u0448\u0435\u043b \u0440\u0435\u0434\u0438\u0440\u0435\u043a\u0442.")
        else:
            print("\u0410\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044f \u043d\u0435 \u043f\u0440\u043e\u0448\u043b\u0430 \u0438\u043b\u0438 \u0440\u0435\u0434\u0438\u0440\u0435\u043a\u0442\u0430 \u043d\u0435 \u043f\u0440\u043e\u0438\u0437\u043e\u0448\u043b\u043e.")

        await browser.close()

async def main():
    config = load_config()
    target_ssid = config['target_ssid']
    login_page_url = config['login_page_url']
    username = config['username']
    password = config['password']

    internet_available = check_internet_connection()
    if internet_available:
        print("\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d. \u041a\u043e\u0434 \u043d\u0435 \u0431\u0443\u0434\u0435\u0442 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d.")
        return

    current_ssid = check_current_connection()
    if current_ssid == target_ssid:
        print(f"\u0412\u044b \u0443\u0436\u0435 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u044b \u043a Wi-Fi \u0441\u0435\u0442\u0438: {target_ssid}")
        await login_to_portal(login_page_url, username, password)
    else:
        print(f"\u0412\u044b \u043d\u0435 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u044b \u043a \u0441\u0435\u0442\u0438 {target_ssid}. \u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a \u0441\u0435\u0442\u0438 {target_ssid}...")
        connected = connect_to_wifi(target_ssid)
        if connected:
            await login_to_portal(login_page_url, username, password)

if __name__ == "__main__":
    asyncio.run(main())
    input("\n\u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u043b\u044e\u0431\u0443\u044e \u043a\u043d\u043e\u043f\u043a\u0443 \u0434\u043b\u044f \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u043a\u043e\u043d\u0441\u043e\u043b\u0438...")
