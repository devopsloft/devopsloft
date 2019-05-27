#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import yaml
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

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
        driver.get(app_url)
        assert driver.title == "DevOps Loft"

        driver.find_element_by_link_text('Home').click()
        assert driver.current_url == app_url + "/home"

        stats_url = "https://statcounter.com/p" + str(project) + "/?guest=1"
        driver.find_element_by_partial_link_text('Stats').click()
        print(stats_url)
        assert driver.current_url == stats_url

        driver.find_element_by_link_text('Resources').click()
        assert driver.current_url == app_url + "/resources"

        driver.find_element_by_link_text('Documents').click()
        assert driver.current_url == app_url + "/docslist"

        driver.find_element_by_link_text('Statistics').click()
        assert driver.current_url == app_url + "/statistics"

        driver.find_element_by_link_text('Contact Us').click()
        assert driver.current_url == app_url + "/contact"

        driver.find_element_by_link_text('Sign Up').click()
        assert driver.current_url == app_url + "/signup"
    print("Tests Passed Successfully")
except NoSuchElementException as exception:
    print("Element not found and test failed: " + exception)
finally:
    for driver in [chrome_driver, firefox_driver]:
        driver.quit()
