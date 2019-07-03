#!/usr/bin/env python3

import logging
from dotenv import load_dotenv
from pathlib import Path
import os
import re
import yaml
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

env_path = Path('..') / '.env'
load_dotenv()

# load statcounter variables for current environment
STATCODES = yaml.load(os.getenv('STATCODES'), Loader=yaml.FullLoader)
project = STATCODES[os.getenv('ENVIRONMENT')]['project']

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
    app_url = 'http://10.0.0.1:5000'
else:
    chrome_driver = webdriver.Chrome()
    firefox_driver = webdriver.Firefox()
    app_url = 'http://localhost:5000'

try:
    for driver in [chrome_driver, firefox_driver]:
        driver.set_page_load_timeout(30)

        print("==== " + str(driver.name) + " ====")
        driver.get(app_url)

        print("Checking Title...")
        assert driver.title == "DevOps Loft"

        driver.find_element_by_link_text('Home').click()
        print("Checking Home...")
        assert driver.current_url == app_url + "/home"

        print("Checking Resources...")
        driver.find_element_by_link_text('Resources').click()
        assert driver.current_url == app_url + "/resources"

        print("Checking Documents...")
        driver.find_element_by_link_text('Documents').click()
        assert driver.current_url == app_url + "/docslist"

        print("Checking Statistics...")
        driver.find_element_by_link_text('Statistics').click()
        assert driver.current_url == app_url + "/statistics"

        print("Checking Contact Us...")
        driver.find_element_by_link_text('Contact Us').click()
        assert driver.current_url == app_url + "/contact"

        print("Checking Sign Up...")
        driver.find_element_by_link_text('Sign Up').click()
        assert driver.current_url == app_url + "/signup"

        print("Checking statcounter...")
        stats_url = "https://statcounter.com/p" + str(project) + "/summary/"
        driver.find_element_by_partial_link_text('Stats').click()
        pattern = r'(?P<url>https?://[^\s]+/)'
        parsed_url = re.search(pattern, driver.current_url).group("url")
        assert parsed_url == stats_url

    print("Tests Passed Successfully")
except AssertionError as error:
    logging.error("Error:" + str(error), exc_info=True)
except NoSuchElementException as exception:
    print("Element not found and test failed: " + exception)
    print(driver.current_url)
finally:
    for driver in [chrome_driver, firefox_driver]:
        driver.quit()
