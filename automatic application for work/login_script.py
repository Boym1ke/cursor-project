from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Function to login to the website
def login_to_website(driver):
    driver.get("https://tracker.ligentix.com/ag_login.aspx")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Enter username
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMessage_userTextBox"))
    )
    username.clear()
    username.send_keys("yvonne.ding@ligentia.global")
    print(f"成功输入账号: yvonne.ding@ligentia.global")

    # Enter password
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMessage_passwordTextBox"))
    )
    password.clear()
    password.send_keys("Tracker2024.1")
    print(f"成功输入密码: {'*' * len('Tracker2024.1')}")

    # Click login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMessage_loginButton"))
    )
    driver.execute_script("arguments[0].click();", login_button)
    print("成功点击登录按钮")
    time.sleep(6)  # 增加登录后的等待时间到6秒

    print("尝试登录完成")

# Function to navigate to a specific page and export Excel
def export_excel(driver):
    # Navigate to the specific page
    driver.get("https://tracker.ligentix.com/TOPS/TOPS_Finance_CW_Unconfirmed.aspx")
    print("Navigated to the finance page.")

    # Wait for the page to load and find the Excel button
    excel_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "excelButtonId"))  # Replace with the actual ID of the Excel button
    )
    excel_button.click()
    print("Excel export initiated.")
    time.sleep(5)  # Wait for the download to complete

# Function to download files from URLs in the text file
def download_files_from_text(driver, text_file_path):
    # Read the text file
    print(f"Reading URLs from: {text_file_path}")
    with open(text_file_path, 'r') as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]
    print(f"Found URLs: {urls}")

    for url in urls:
        print(f"Navigating to URL: {url}")
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        try:
            # Click the download button
            print(f"Attempting to click download button for URL: {url}")
            download_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolderContent_downloadButton")
            download_button.click()
            print(f"Clicked download button for URL: {url}")
            time.sleep(5)  # Wait for the download to complete
        except Exception as e:
            print(f"Error downloading file from {url}: {e}")

# Main function
def main():
    print("Starting script...")
    # Path to the text file
    text_file_path = r"C:\data\readurl.txt"

    # Set up the Chrome driver with options
    print("Setting up Chrome driver...")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Create download folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    download_folder = os.path.join(current_dir, "1")
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    print(f"Download folder set to: {download_folder}")

    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Login to the website
        login_to_website(driver)

        # Export Excel from the specific page
        export_excel(driver)

        # Download files from URLs in the text file
        download_files_from_text(driver, text_file_path)
    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()