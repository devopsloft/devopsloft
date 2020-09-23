#!/usr/bin/env python3

import os

import yaml
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def main():
    load_dotenv(dotenv_path=".env.ci")

    # load statcounter variables for current environment
    STATCODES = yaml.load(os.getenv('STATCODES'), Loader=yaml.FullLoader)
    project = STATCODES[os.getenv('ENVIRONMENT')]['project']

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
            url = "https://statcounter.com/p" + str(project) + "/summary/"
            driver.find_element_by_partial_link_text('Stats').click()
            assert url in driver.current_url

        print("Tests Passed Successfully")
    except AssertionError as error:
        print(str(error))
    except NoSuchElementException as exception:
        print("Error: Element not found and test failed: " + exception)
    finally:
        for driver in [chrome_driver, firefox_driver]:
            driver.quit()


if __name__ == '__main__':
    main()
