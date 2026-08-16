from selenium.webdriver.common.by import By

class OrdersPageLocators:
    ORDERS_LIST_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    ORDER_STRUCTURE = (By.XPATH, "//p[text()='Cостав']")
    ORDER_LINK = (By.XPATH, "//*[contains(@class, 'OrderHistory_link')]")
    ALL_ORDERS_AT_HISTORY = (By.XPATH, "//div[contains(@class, 'OrderHistory_textBox')]/p[contains(@class, 'text_type_digits-default')]")
    ALL_ORDERS_AT_FEED = (By.XPATH, "//div[contains(@class, 'OrderHistory_textBox')]//p[@class='text text_type_digits-default']")
    TOTAL_ORDER_COUNT = (By.XPATH, "//p[contains(normalize-space(.), 'Выполнено за все время:')]/following-sibling::*[1]")
    DAILY_ORDER_COUNT = (By.XPATH, "//p[contains(normalize-space(.), 'Выполнено за сегодня:')]/following-sibling::*[1]")
    NUMBER_IN_PROGRESS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li[contains(@class, 'text_type_digits-default')]")
