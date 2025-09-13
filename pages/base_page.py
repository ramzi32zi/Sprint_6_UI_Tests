# pages/base_page.py
from __future__ import annotations

import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from utils.urls import Urls


class BasePage:
    """Базовый объект страницы: удобные ожидания, скролл и безопасные клики."""

    def __init__(self, driver):
        self.driver = driver

    # ---------- базовые ожидания ----------
    def _wait(self, timeout: int = 10) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout)

    def find_element(self, locator, timeout: int = 10):
        return self._wait(timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}",
        )

    def find_elements(self, locator, timeout: int = 10):
        return self._wait(timeout).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Can't find elements by locator {locator}",
        )

    def wait_visible(self, locator, timeout: int = 10):
        return self._wait(timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible: {locator}",
        )

    def wait_clickable(self, locator, timeout: int = 10):
        return self._wait(timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}",
        )

    # ---------- утилиты для кликов ----------
    def _scroll_into_view(self, element) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'center'});",
            element,
        )

    def _js_click(self, element) -> None:
        self.driver.execute_script("arguments[0].click();", element)

    def safe_click(self, locator, timeout: int = 10) -> None:
        """Клик с автоскроллом и запасным JS-кликом, если что-то перекрывает элемент."""
        elem = self.wait_clickable(locator, timeout)
        self._scroll_into_view(elem)
        try:
            elem.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            # ещё раз достанем элемент (вдруг DOM обновился) и кликнем JS’ом
            elem = self.find_element(locator, timeout)
            self._scroll_into_view(elem)
            self._js_click(elem)

    def safe_click_webelement(self, element) -> None:
        """Аналог safe_click, если уже есть сам элемент."""
        self._scroll_into_view(element)
        try:
            element.click()
        except (ElementClickInterceptedException, StaleElementReferenceException):
            self._scroll_into_view(element)
            self._js_click(element)

    # ---------- навигация ----------
    @allure.step("Перейти по адресу")
    def go_to_site(self, url: str | None = None) -> None:
        self.driver.get(url or Urls.MAIN_PAGE)

    @allure.step("Текущий URL")
    def current_url(self) -> str:
        return self.driver.current_url
