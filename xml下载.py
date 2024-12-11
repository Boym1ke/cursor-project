import os
import time
from functools import wraps

def lazy_import(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global webdriver, Options, By, WebDriverWait, EC, TimeoutException, NoSuchElementException
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        return func(*args, **kwargs)
    return wrapper

@lazy_import
def login_to_website(driver):
    driver.get("https://tracker.ligentix.com/ag_login.aspx")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMessage_userTextBox"))
    )
    username.clear()
    username.send_keys("yvonne.ding@ligentia.global")
    print("成功输入账号: yvonne.ding@ligentia.global")

    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMessage_passwordTextBox"))
    )
    password.clear()
    password.send_keys("Tracker2024.1")
    print(f"成功输入密码: {'*' * len('Tracker2024.1')}")

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMessage_loginButton"))
    )
    driver.execute_script("arguments[0].click();", login_button)
    print("成功点击登录按钮")
    WebDriverWait(driver, 10).until(EC.url_changes("https://tracker.ligentix.com/ag_login.aspx"))
    print("登录成功")

@lazy_import
def download_files_from_text(driver, text_file_path):
    print(f"Reading URLs from: {text_file_path}")
    with open(text_file_path, 'r') as file:
        urls = [url.strip() for url in file.readlines()]
    print(f"Found {len(urls)} URLs")

    for url in urls:
        print(f"Navigating to URL: {url}")
        driver.get(url)
        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderContent_downloadButton"))
            )
            download_button.click()
            print(f"Clicked download button for URL: {url}")
            time.sleep(2)  # 减少等待时间
        except Exception as e:
            print(f"Error downloading file from {url}: {e}")

@lazy_import
def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")  # 添加无头模式，加快启动速度

    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(current_dir, "1")
    os.makedirs(download_folder, exist_ok=True)

    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def preload():
    # 在这里执行一些耗时的初始化操作
    # 例如，提前下载和设置 ChromeDriver
    from webdriver_manager.chrome import ChromeDriverManager
    ChromeDriverManager().install()

def main():
    text_file_path = r"C:\data\readurl.txt"
    driver = setup_chrome_driver()

    try:
        login_to_website(driver)
        download_files_from_text(driver, text_file_path)
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()