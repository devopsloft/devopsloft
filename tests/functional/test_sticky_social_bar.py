#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def test_sticky_social_bar_exists():

    load_dotenv(dotenv_path=".env.ci")

    chrome_options = webdriver.chrome.options.Options()
    chrome_options.headless = True
    chrome_options.set_capability("acceptInsecureCerts", True)
    chrome_driver = webdriver.Chrome(options=chrome_options)

    firefox_options = webdriver.firefox.options.Options()
    firefox_options.headless = True
    firefox_options.set_capability("acceptInsecureCerts", True)
    firefox_driver = webdriver.Firefox(options=firefox_options)

    app_url = "https://localhost:{0}".format(os.getenv("WEB_SECURE_PORT"))

    try:

        for driver in [chrome_driver, firefox_driver]:
            driver.set_page_load_timeout(30)
            driver.get(app_url)
            driver.find_element_by_class_name('icon-bar')

    except NoSuchElementException:
        return False
    finally:
        for driver in [chrome_driver, firefox_driver]:
            driver.quit()
