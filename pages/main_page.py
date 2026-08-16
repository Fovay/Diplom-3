import allure
from data.urls import Urls
from locators.main_page_locators import MainPageLocators
from locators.orders_page_locators import OrdersPageLocators
from pages.base_page import BasePage

class MainPage(BasePage):
    @allure.step('Перейти в «Ленту заказов»')
    def click_orders_list_button(self):
        if self.get_current_url() != Urls.URL_FEED:
            self.open_link(Urls.URL_FEED)
        self.wait_for_element(OrdersPageLocators.ORDERS_LIST_TITLE)

    @allure.step('Перейти в «Конструктор»')
    def click_constructor_button(self):
        if self.get_current_url() != Urls.URL_MAIN:
            self.open_link(Urls.URL_MAIN)
        self.wait_for_element(MainPageLocators.MAIN_LIST_TITLE)

    @allure.step('Кликнуть на ингредиент')
    def click_on_ingredient(self):
        self.wait_and_click(MainPageLocators.BUN_INGREDIENT)

    @allure.step('Получить заголовок окна деталей ингредиента')
    def get_ingredient_details_title(self):
        return self.get_actual_text(MainPageLocators.INGREDIENT_DETAILS_POPUP)

    @allure.step('Закрыть окно деталей ингредиента')
    def click_cross_button(self):
        self.wait_and_click(MainPageLocators.CROSS_BUTTON)
        self.wait_for_element_invisibility(MainPageLocators.INGREDIENT_MODAL)

    @allure.step('Получить счётчик ингредиента')
    def get_ingredient_counter(self):
        return self.get_counter_value(MainPageLocators.INGREDIENT_COUNTER)

    @allure.step('Добавить булку в заказ')
    def add_filling_to_order(self):
        try:
            self.drag_and_drop(MainPageLocators.BUN_INGREDIENT,MainPageLocators.ORDER_BASKET)
        except Exception:
            pass
        if not self.is_element_visible(MainPageLocators.BUN_TOP_IN_ORDER, timeout=3):
            self.click_with_js(MainPageLocators.BUN_INGREDIENT)
        self.wait_for_element(MainPageLocators.BUN_TOP_IN_ORDER)

    @allure.step('Дождаться увеличения счётчика ингредиента')
    def wait_for_ingredient_counter_increase(self, old_value):
        self.wait_for_counter_increase(MainPageLocators.INGREDIENT_COUNTER,old_value)

    @allure.step('Нажать «Оформить заказ»')
    def click_order_button(self):
        self.wait_and_click(MainPageLocators.CREATE_ORDER_BUTTON)
        self.wait_for_element(MainPageLocators.ORDER_IDENTIFICATE)

    @allure.step('Дождаться появления реального номера заказа')
    def wait_for_real_order_number(self):
        self.wait_for_order_number(MainPageLocators.ORDER_ID,placeholder="9999")

    @allure.step('Получить номер заказа')
    def get_order_id(self):
        self.wait_for_real_order_number()
        return self.get_actual_text(MainPageLocators.ORDER_ID)

    @allure.step('Закрыть окно после оформления заказа')
    def click_close_modal_order(self):
        self.wait_for_element(MainPageLocators.CLOSE_MODAL_ORDER)
        self.click_with_js(MainPageLocators.CLOSE_MODAL_ORDER)
        self.wait_for_element_invisibility(MainPageLocators.ORDER_MODAL)

    @allure.step('Получить статус заказа')
    def get_order_status_text(self):
        return self.get_actual_text(MainPageLocators.ORDER_STATUS_TEXT)