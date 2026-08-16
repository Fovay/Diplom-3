from selenium.webdriver.common.by import By

class UserProfileLocators:
    PROFILE_BUTTON = (By.LINK_TEXT, "Профиль")
    ORDER_HISTORY_BUTTON = (By.LINK_TEXT, "История заказов")
    ENABLED_ORDER_HISTORY_BUTTON = (By.XPATH, "//ul/li[2]/a[contains(@class, 'Account_link_active')]")
    LOGOUT_BUTTON = (By.XPATH, ".//button[text()='Выход']")
    LK_INFO_MESSAGE = (By.XPATH, ".//p[contains(text(),'персональные данные')]")
