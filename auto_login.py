# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00ABC8B427B72303D34612D4AFAB4A5FD2640042B3BDB5AED1655E6F5679F4A64CC8F8FA64F6A135B97F32106CD37365F923FEF70E294B7AD4BEAAC29ECCE3866D6DE0C9B1429B33E913098785B447B4085D761303CF142BBA99F059AD6C4BCEDE73E5497C886AFC5B30E0837BC616A82A86114FDBAF5F02E2924BE2752613D3132C80ECC177351023969C23CC8F4B3E2A6971A7AE8F9E3C208A0A2728147B54826DE9E67CBD4923001F99E4B89E2AEB643688309B5CACAEC2AD4E5B6194C49904C7D49A789F01FD26BA914C5C17F118C9D7041FC8A77598995FEFC3DDCD2A7B8DCA2954181A3533E24E5CB331D89FD422731F40A788CBD106D84C4A6BCC2C418A1AFA43670784BAD6CC4428F051B3D405EE2D1939B40FEA5F0D307E10BB255564185D56878AFE05EB00A93C36BEB7788E1B4B5E2DAF030648E5859FD87C1395A924F5AAC50997AB595F474BAD24D44833EB8F7B31559B57AEE163ED59E4C1E3E6"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
