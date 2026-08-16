import allure
from data.urls import Urls
from data.user_data import PersonData
from locators.auth_login_locators import AuthLoginLocators
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage

class AuthUserPage(BasePage):
    @allure.step('Перейти в «Личный кабинет»')
    def click_personal_account_button(self):
        self.click_on_element(MainPageLocators.LOGIN_PROFILE_BUTTON)

    @allure.step('Заполнить поле Email')
    def set_email_field(self, user_email):
        self.set_text_to_element(AuthLoginLocators.EMAIL_FIELD, user_email)

    @allure.step('Заполнить поле Пароль')
    def set_password_field(self, user_password):
        self.set_text_to_element(AuthLoginLocators.PASSWORD_FIELD, user_password)

    @allure.step('Дождаться главной страницы после входа')
    def wait_for_logged_in_main_page(self):
        return self.wait.until(
            lambda d: d.current_url == Urls.URL_MAIN and (self.is_element_visible(MainPageLocators.CONSTRUCTOR_BUTTON, timeout=1)
                or self.is_element_visible(MainPageLocators.CREATE_ORDER_BUTTON, timeout=1)))

    @allure.step('Нажать кнопку «Войти»')
    def click_login_button(self):
        self.wait_and_click(AuthLoginLocators.LOGIN_BUTTON_ANY_FORMS)
        self.wait.until(lambda d: d.current_url != Urls.URL_LOGIN)
        if self.get_current_url() == Urls.URL_LOGIN:
            self.open_link(Urls.URL_MAIN)
        self.wait_for_logged_in_main_page()

    @allure.step('Авторизоваться')
    def login(self):
        self.click_personal_account_button()
        self.set_email_field(PersonData.USER_LOGIN)
        self.set_password_field(PersonData.USER_PASSWORD)
        self.click_login_button()
        self.open_link(Urls.URL_MAIN)
        self.wait_for_logged_in_main_page()