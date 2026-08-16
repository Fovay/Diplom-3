import allure

class TestOrderFeed:
    @allure.title('Увеличение счетчика "Выполнено за всё время" ''при создании заказа')
    def test_total_orders_counter_increases(self, main_page, login, order_feed_page):
        main_page.click_orders_list_button()
        previous_count = order_feed_page.get_total_order_count()
        main_page.click_constructor_button()
        main_page.add_filling_to_order()
        main_page.click_order_button()
        main_page.wait_for_real_order_number()
        main_page.click_close_modal_order()
        main_page.click_orders_list_button()
        current_count = order_feed_page.wait_until_total_orders_increased(previous_count)
        assert current_count > previous_count

    @allure.title('Увеличение счетчика "Выполнено за сегодня" ''при создании заказа')
    def test_today_orders_counter_increases(self, main_page, login, order_feed_page):
        main_page.click_orders_list_button()
        previous_count = order_feed_page.get_daily_order_count()
        main_page.click_constructor_button()
        main_page.add_filling_to_order()
        main_page.click_order_button()
        main_page.wait_for_real_order_number()
        main_page.click_close_modal_order()
        main_page.click_orders_list_button()
        current_count = order_feed_page.wait_until_daily_orders_increased(previous_count)
        assert current_count > previous_count

    @allure.title('Появление номера заказа в разделе "В работе"')
    def test_order_number_in_progress(self, main_page, login, order_feed_page):
        main_page.click_orders_list_button()
        main_page.click_constructor_button()
        main_page.add_filling_to_order()
        main_page.click_order_button()
        main_page.wait_for_real_order_number()
        order_number = main_page.get_order_id()
        main_page.click_close_modal_order()
        main_page.click_orders_list_button()
        order_in_progress = order_feed_page.wait_for_order_in_progress(order_number)
        assert order_number == order_in_progress