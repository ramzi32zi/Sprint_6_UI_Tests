from __future__ import annotations

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.locators import BasePageLocator
from utils.locators import YaScooterHomePageLocator as Locators


class YaScooterHomePage(BasePage):
    @allure.step("Нажать на кнопку заказа вверху страницы")
    def click_top_order_button(self):
        self.safe_click(Locators.TOP_ORDER_BUTTON)

    @allure.step("Нажать на кнопку заказа внизу страницы")
    def click_bottom_order_button(self):
        self.safe_click(Locators.BOTTOM_ORDER_BUTTON)

    @allure.step("Нажать на вопрос №{question_number} в FAQ")
    def click_faq_question(self, question_number: int):
        buttons = self.find_elements(Locators.FAQ_BUTTONS, timeout=10)
        btn = buttons[question_number]
        # безопасный клик с прокруткой/JS на случай перекрытия картинкой
        self.safe_click_webelement(btn)
        # дождаться, что соответствующий ответ видим
        self.wait_visible(Locators.FAQ_ANSWER(answer_number=question_number), timeout=10)

    @allure.step("Переключиться на вкладку браузера")
    def switch_window(self, window_number: int = 1):
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def wait_url_until_not_about_blank(self, time=10):
        return WebDriverWait(self.driver, time).until_not(EC.url_to_be("about:blank"))

    @allure.step("Перейти на страницу Яндекса")
    def click_yandex_button(self):
        self.safe_click(BasePageLocator.YANDEX_SITE_BUTTON)

    @allure.step("Принять куки")
    def click_cookie_accept(self):
        try:
            by, sel = BasePageLocator.COOKIE_ACCEPT_BUTTON  
            elems = self.driver.find_elements(by, sel)   
            if elems:
                self.safe_click_webelement(elems[0])
        except Exception:
            
            pass
