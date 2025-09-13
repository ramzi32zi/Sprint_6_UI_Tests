import allure
import pytest
from utils.urls import Urls
from pages.home_page import YaScooterHomePage


@allure.epic("Главная страница: переходы")
@allure.suite("Header и основные кнопки")
class TestHomePageNavigation:

    @pytest.fixture
    def home_page(self, driver):
        """Открывает домашнюю страницу и принимает куки."""
        page = YaScooterHomePage(driver)
        page.go_to_site()
        page.click_cookie_accept()
        return page

    @allure.feature("Кнопки заказа")
    @allure.story("Заказ через кнопку в шапке")
    def test_order_from_header_opens_order_page(self, home_page):
        home_page.click_top_order_button()
        assert home_page.current_url() == Urls.ORDER_PAGE, \
            "Кнопка в шапке не ведёт на страницу оформления заказа"

    @allure.feature("Кнопки заказа")
    @allure.story("Заказ через кнопку в блоке 'Как это работает'")
    def test_order_from_bottom_opens_order_page(self, home_page):
        home_page.click_bottom_order_button()
        assert home_page.current_url() == Urls.ORDER_PAGE, \
            "Кнопка снизу не ведёт на страницу оформления заказа"

    @allure.feature("Редиректы")
    @allure.story("Переход по лого ЯндексСамокат")
    def test_logo_redirects_to_yandex(self, home_page):
        home_page.click_yandex_button()
        home_page.switch_window(1)
        home_page.wait_url_until_not_about_blank()

        current_url = home_page.current_url()
        assert (
            Urls.YANDEX_HOME_PAGE in current_url
            or Urls.DZEN_HOME_PAGE in current_url
            or Urls.YANDEX_CAPTCHA_PAGE in current_url
        ), f"Редирект по лого не сработал, URL: {current_url}"
