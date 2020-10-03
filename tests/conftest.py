import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def driver_init_1(request):
    options = webdriver.chrome.options.Options()
    options.headless = True
    options.set_capability("acceptInsecureCerts", True)
    web_driver = webdriver.Chrome(options=options)
    web_driver.set_page_load_timeout(30)
    request.cls.driver = web_driver
    yield
    web_driver.close()


@pytest.fixture(scope="class")
def driver_init_2(request):
    options = webdriver.firefox.options.Options()
    options.headless = True
    options.set_capability("acceptInsecureCerts", True)
    web_driver = webdriver.Firefox(options=options)
    web_driver.set_page_load_timeout(30)
    request.cls.driver = web_driver
    yield
    web_driver.close()
