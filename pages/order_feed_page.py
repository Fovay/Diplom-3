import allure
from locators.orders_page_locators import OrdersPageLocators
from pages.base_page import BasePage

class OrderFeedPage(BasePage):
    @allure.step('Дождаться открытия «Ленты заказов»')
    def wait_until_page_opened(self):
        self.wait_for_element(OrdersPageLocators.ORDERS_LIST_TITLE)

    @allure.step('Получить количество заказов за всё время')
    def get_total_order_count(self):
        return self.get_counter_value(OrdersPageLocators.TOTAL_ORDER_COUNT)

    @allure.step('Получить количество заказов за сегодня')
    def get_daily_order_count(self):
        return self.get_counter_value(OrdersPageLocators.DAILY_ORDER_COUNT)

    @allure.step('Дождаться увеличения количества заказов за всё время')
    def wait_until_total_orders_increased(self, old_value):
        return self.wait_for_counter_increase(OrdersPageLocators.TOTAL_ORDER_COUNT, old_value)

    @allure.step('Дождаться увеличения количества заказов за сегодня')
    def wait_until_daily_orders_increased(self, old_value):
        return self.wait_for_counter_increase(OrdersPageLocators.DAILY_ORDER_COUNT, old_value)

    @allure.step('Дождаться появления заказа в разделе «В работе»')
    def wait_for_order_in_progress(self, order_number):
        self.wait_for_text_in_elements(OrdersPageLocators.NUMBER_IN_PROGRESS, order_number, timeout=40)
        return order_number

    @allure.step('Получить номер заказа в разделе «В работе»')
    def get_order_in_progress(self):
        return self.get_first_element_text(OrdersPageLocators.NUMBER_IN_PROGRESS)