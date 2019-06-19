#!/usr/bin/env python3

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import loft_hvac  # noqa: E402

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../modules')

env_path = Path('..') / '.env'
load_dotenv()

if os.getenv('TRAVIS') in [None, False]:
    SELENIUM_HUB = 'http://localhost:4444/wd/hub'

    chrome_driver = webdriver.Remote(
      command_executor=SELENIUM_HUB,
      desired_capabilities=DesiredCapabilities.CHROME,
    )

    firefox_driver = webdriver.Remote(
      command_executor=SELENIUM_HUB,
      desired_capabilities=DesiredCapabilities.FIREFOX,
    )
    app_url = 'http://10.0.0.1:8200'
else:
    chrome_driver = webdriver.Chrome()
    firefox_driver = webdriver.Firefox()
    app_url = 'http://localhost:8200'

try:
    for driver in [chrome_driver, firefox_driver]:

        print("==== " + str(driver.name) + " ====")
        driver.get(app_url)

        print("Checking Title...")
        assert driver.title == "Vault"

        loft_hvac.seal()
        time.sleep(10)

        print("Checking Unseal...key=1/3")
        driver.find_element_by_name('key').send_keys(loft_hvac.get_key(0))
        driver.find_element_by_css_selector('button.button.is-primary').click()
        element = driver.find_element_by_css_selector(
            "span.has-text-grey.is-size-8.shamir-progress-progress"
        )
        assert element.text == "1/3 keys provided"

        print("Checking Unseal...key=2/3")
        driver.find_element_by_name('key').send_keys(loft_hvac.get_key(1))
        driver.find_element_by_css_selector('button.button.is-primary').click()
        element = driver.find_element_by_css_selector(
            'span.has-text-grey.is-size-8.shamir-progress-progress'
        )
        assert element.text == "2/3 keys provided"

        print("Checking Unseal...key=3/3")
        driver.find_element_by_name('key').send_keys(loft_hvac.get_key(2))
        driver.find_element_by_css_selector('button.button.is-primary').click()
        element = driver.find_element_by_css_selector(
            'button#auth-submit.button.is-primary'
        )
        assert element.text == "Sign In"
        time.sleep(10)

        print("Checking Unseal...Token")
        driver.find_element_by_name('token').send_keys(
            loft_hvac.get_root_token()
        )
        driver.find_element_by_css_selector(
            "button#auth-submit.button.is-primary"
        ).click()
        element = driver.find_element_by_css_selector(
            'h1.title.is-3'
        )
        assert element.text == "Secrets Engines"

    print("Tests Passed Successfully")
finally:
    for driver in [chrome_driver, firefox_driver]:
        driver.quit()
