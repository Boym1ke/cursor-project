from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

def login_to_website(driver):
    driver.get("https://tracker.ligentix.com/ag_login.aspx")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMessage_userTextBox"))
    )
    username.clear()
    username.send_keys("yvonne.ding@ligentia.global")
    print(f"成功输入账号: yvonne.ding@ligentia.global")

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
    time.sleep(3)

    print("尝试登录完成")

def download_files_from_text(driver, text_file_path):
    print(f"Reading URLs from: {text_file_path}")
    with open(text_file_path, 'r') as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]
    print(f"Found URLs: {urls}")

    for url in urls:
        print(f"Navigating to URL: {url}")
        driver.get(url)
        time.sleep(2)

        try:
            download_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolderContent_downloadButton")
            download_button.click()
            print(f"Clicked download button for URL: {url}")
            time.sleep(5)
        except Exception as e:
            print(f"Error downloading file from {url}: {e}")

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(current_dir, "1")
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(options=chrome_options)

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