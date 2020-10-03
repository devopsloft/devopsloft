import os

import pytest
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException


@pytest.mark.usefixtures("driver_init_1")
class TestBrowser:

    def test_sticky_social_bar_exists(self):

        load_dotenv(dotenv_path=".env.ci")
        app_url = "https://localhost:{0}".format(os.getenv("WEB_SECURE_PORT"))

        try:

            self.driver.get(app_url)
            self.driver.find_element_by_class_name('icon-bar')

        except NoSuchElementException:
            return False

    def test_contact_us(self):

        load_dotenv(dotenv_path=".env.ci")
        app_url = "https://localhost:{0}".format(os.getenv("WEB_SECURE_PORT"))

        try:

            self.driver.get(app_url)
            self.driver.find_element_by_link_text('Contact Us').click()
            assert self.driver.current_url == app_url + "/contact_us"

            self.driver.find_element_by_id('name').send_keys('John Doe')
            self.driver.find_element_by_id('email').send_keys('fake@fake.com')
            self.driver.find_element_by_id(
                'subject'
            ).send_keys('You talking to me?')
            self.driver.find_element_by_id(
                'message'
            ).send_keys('stam stam stam')
            self.driver.find_element_by_partial_link_text('Send').click()
            assert app_url + '/home' in self.driver.current_url

        except NoSuchElementException:
            return False
