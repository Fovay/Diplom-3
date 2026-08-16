import allure
from data.urls import Urls
from locators.main_page_locators import MainPageLocators

class TestMainFunctionality:
    @allure.title('Переход по клику на «Конструктор»')
    def test_click_constructor(self, main_page):
        main_page.click_orders_list_button()
        main_page.click_constructor_button()
        
        assert main_page.get_current_url() == Urls.URL_MAIN

    @allure.title('Переход по клику на «Лента заказов»')
    def test_click_order_feed(self, main_page):
        main_page.click_orders_list_button()

        assert main_page.get_current_url() == Urls.URL_FEED

    @allure.title('Открытие модального окна с деталями ингредиента')
    def test_open_ingredient_details(self, main_page):
        main_page.click_on_ingredient()
        actual_title = (main_page.get_ingredient_details_title())

        assert actual_title == "Детали ингредиента"

    @allure.title('Закрытие модального окна кликом по крестику')
    def test_close_ingredient_details(self, main_page):
        main_page.click_on_ingredient()
        main_page.click_cross_button()

        assert not main_page.is_element_visible(MainPageLocators.INGREDIENT_MODAL,timeout=5)

    @allure.title('Увеличение счетчика ингредиента при добавлении в заказ')
    def test_ingredient_counter_increases(self, main_page):
        old_value = main_page.get_ingredient_counter()
        main_page.add_filling_to_order()
        main_page.wait_for_ingredient_counter_increase(old_value)
        actual_counter = (main_page.get_ingredient_counter())

        assert actual_counter > old_value