from __future__ import annotations

import re
import allure

from pages.base_page import BasePage
from utils.locators import YaScooterOrderPageLocator as Loc


class YaScooterOrderPage(BasePage):
    """Страница оформления заказа самоката."""

    # --- Этап 1: Для кого самокат ---
    @allure.step("Заполнить поле 'Фамилия'")
    def set_last_name(self, last_name: str) -> None:
        self.find_element(Loc.LAST_NAME_INPUT).send_keys(last_name)

    @allure.step("Заполнить поле 'Имя'")
    def set_first_name(self, first_name: str) -> None:
        self.find_element(Loc.FIRST_NAME_INPUT).send_keys(first_name)

    @allure.step("Заполнить поле 'Адрес'")
    def set_address(self, address: str) -> None:
        self.find_element(Loc.ADDRESS_INPUT).send_keys(address)

    @allure.step("Выбрать метро: {station}")
    def select_subway(self, station: str) -> None:
        self.find_element(Loc.SUBWAY_FIELD).click()
        self.find_element(Loc.SUBWAY_HINT_BUTTON(station)).click()

    @allure.step("Ввести номер телефона")
    def set_phone(self, phone: str) -> None:
        self.find_element(Loc.TELEPHONE_NUMBER_FIELD).send_keys(phone)

    @allure.step("Перейти к следующему шагу")
    def next_step(self) -> None:
        self.find_element(Loc.NEXT_BUTTON).click()

    # --- Этап 2: Про аренду ---
    @allure.step("Указать дату аренды: {date}")
    def set_date(self, date: str) -> None:
        self.find_element(Loc.DATE_FIELD).send_keys(date)

    @allure.step("Выбрать срок аренды (индекс {index})")
    def set_rental_period(self, index: int) -> None:
        self.find_element(Loc.RENTAL_PERIOD_FIELD).click()
        self.find_elements(Loc.RENTAL_PERIOD_LIST)[index].click()

    @allure.step("Отметить цвет по индексу {index}")
    def choose_color(self, index: int) -> None:
        self.find_elements(Loc.COLOR_CHECKBOXES)[index].click()

    @allure.step("Добавить комментарий для курьера")
    def set_comment(self, comment: str) -> None:
        self.find_element(Loc.COMMENT_FOR_COURIER_FIELD).send_keys(comment)

    # --- Завершение заказа ---
    @allure.step("Кликнуть 'Заказать'")
    def submit_order(self) -> None:
        self.find_element(Loc.ORDER_BUTTON).click()

    @allure.step("Подтвердить заказ")
    def confirm_order(self) -> None:
        self.find_element(Loc.ACCEPT_ORDER_BUTTON).click()

    @allure.step("Прочитать номер заказа")
    def fetch_order_number(self) -> str:
        text = self.find_element(Loc.ORDER_COMPLETED_INFO).text
        return "".join(re.findall(r"\d", text))

    @allure.step("Перейти к статусу заказа")
    def go_to_status(self) -> None:
        self.find_element(Loc.SHOW_STATUS_BUTTON).click()

    # --- Групповые шаги ---
    @allure.step("Заполнить форму 'Для кого самокат'")
    def fill_customer_info(self, data: dict) -> None:
        self.set_first_name(data["first_name"])
        self.set_last_name(data["last_name"])
        self.set_address(data["address"])
        self.select_subway(data["subway_name"])
        # ключ оставлен намеренно как в тестовых данных (с опечаткой)
        self.set_phone(data["telepthone_number"])

    @allure.step("Заполнить форму 'Про аренду'")
    def fill_rent_info(self, data: dict) -> None:
        self.set_date(data["date"])
        self.set_rental_period(data["rental_period"])
        for idx in data["color"]:
            self.choose_color(idx)
        self.set_comment(data["comment_for_courier"])

    # --- АЛИАСЫ для совместимости со старыми тестами ---
    # «Для кого самокат»
    def input_first_name(self, v: str): return self.set_first_name(v)
    def input_last_name(self, v: str): return self.set_last_name(v)
    def input_address(self, v: str): return self.set_address(v)
    def input_telephone_number(self, v: str): return self.set_phone(v)
    def choose_subway(self, name: str): return self.select_subway(name)

    # навигация
    def go_next(self): return self.next_step()

    # «Про аренду»
    def input_date(self, v: str): return self.set_date(v)
    def choose_rental_period(self, idx: int): return self.set_rental_period(idx)
    def input_comment(self, v: str): return self.set_comment(v)

    # оформление
    def click_order(self): return self.submit_order()
    def click_accept_order(self): return self.confirm_order()
    def get_order_number(self): return self.fetch_order_number()
    def click_go_to_status(self): return self.go_to_status()

    # групповые
    def fill_user_data(self, data: dict): return self.fill_customer_info(data)
    def fill_rent_data(self, data: dict): return self.fill_rent_info(data)
