import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    @allure.step("Открыть страницу")
    def open_link(self, url):
        self.driver.get(url)

    @allure.step("Убрать перекрывающий overlay модального окна")
    def close_modal_overlay_if_present(self):
        overlay_locator = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")
        try:
            overlay = self.driver.find_element(*overlay_locator)
            if overlay.is_displayed():
                self.driver.execute_script("arguments[0].style.display='none'; arguments[0].style.pointerEvents='none';",overlay,)
        except Exception:
            pass

    @allure.step("Кликнуть по элементу")
    def click_on_element(self, locator):
        self.close_modal_overlay_if_present()
        element = self.wait_for_clickable(locator)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",element,)

    @allure.step("Кликнуть по элементу через JavaScript")
    def click_with_js(self, locator):
        self.close_modal_overlay_if_present()
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",element,)

    @allure.step("Ввести текст")
    def set_text_to_element(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента")
    def get_actual_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    @allure.step("Дождаться видимости элемента")
    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Дождаться кликабельности элемента")
    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Дождаться исчезновения элемента")
    def wait_for_element_invisibility(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Перетащить элемент в область")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.wait.until(EC.presence_of_element_located(source_locator))
        target = self.wait.until(EC.presence_of_element_located(target_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});"
            "arguments[1].scrollIntoView({block: 'center'});",
            source,
            target,)

        script = """
            const source = arguments[0];
            const target = arguments[1];
            const transfer = new DataTransfer();
            source.dispatchEvent(new DragEvent('dragstart', { bubbles: true, cancelable: true, dataTransfer: transfer }));
            target.dispatchEvent(new DragEvent('dragenter', { bubbles: true, cancelable: true, dataTransfer: transfer }));
            target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer: transfer }));
            target.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer: transfer }));
            target.dispatchEvent(new DragEvent('dragover', { bubbles: true, cancelable: true, dataTransfer: transfer }));
            source.dispatchEvent(new DragEvent('dragend', { bubbles: true, cancelable: true, dataTransfer: transfer }));
        """

        try:
            self.driver.execute_script(script, source, target)
        except Exception:
            pass

        browser_name = (self.driver.capabilities.get("browserName") or "").lower()
        if browser_name == "firefox":
            try:
                ActionChains(self.driver).drag_and_drop(source, target).perform()
            except Exception:
                pass
            return

        try:
            ActionChains(self.driver).click_and_hold(source).move_to_element(target).release(target).perform()
        except Exception:
            pass

        try:
            ActionChains(self.driver).drag_and_drop(source, target).perform()
        except Exception:
            pass

    @allure.step("Получить значение счётчика")
    def get_counter_value(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        text = element.text.strip()
        if not text:
            raise TimeoutException(f"Счётчик пустой для локатора: {locator}")
        try:
            return int(text)
        except ValueError as exc:
            raise TimeoutException(f"Счётчик содержит нечисловое значение: {text}") from exc

    @allure.step("Дождаться увеличения счётчика")
    def wait_for_counter_increase(self, locator, old_value):
        def counter_increased(driver):
            try:
                elements = driver.find_elements(*locator)
                if not elements:
                    return False
                text = elements[0].text.strip()
                if not text or not text.isdigit():
                    return False
                value = int(text)
                return value if value > int(old_value) else False
            except StaleElementReferenceException:
                return False
        return self.wait.until(counter_increased)

    @allure.step("Дождаться появления текста среди элементов")
    def wait_for_text_in_elements(self, locator, expected_text, timeout=30):
        wait = WebDriverWait(self.driver, timeout)
        def text_present(driver):
            elements = driver.find_elements(*locator)
            return any(expected_text in element.text.strip() for element in elements)
        return wait.until(text_present)

    @allure.step("Получить текст первого элемента")
    def get_first_element_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    @allure.step("Дождаться кликабельности и кликнуть")
    def wait_and_click(self, locator):
        self.close_modal_overlay_if_present()
        element = self.wait_for_clickable(locator)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",element,)

    @allure.step("Дождаться появления реального номера заказа")
    def wait_for_order_number(self, locator, placeholder="9999"):
        def order_number_appeared(driver):
            try:
                element = driver.find_element(*locator)
                text = element.text.strip()
                return text if text and text != placeholder and text.isdigit() else False
            except Exception:
                return False
        return self.wait.until(order_number_appeared)