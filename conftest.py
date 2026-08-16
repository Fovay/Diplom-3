import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from data.urls import Urls
from pages.login_page import AuthUserPage
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        browser = webdriver.Firefox(options=options)

    browser.implicitly_wait(10)
    browser.get(Urls.URL_MAIN)
    yield browser
    browser.quit()

@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@pytest.fixture
def auth_user_page(driver):
    return AuthUserPage(driver)

@pytest.fixture
def order_feed_page(driver):
    return OrderFeedPage(driver)

@pytest.fixture
def login(auth_user_page):
    auth_user_page.login()
    return auth_user_page