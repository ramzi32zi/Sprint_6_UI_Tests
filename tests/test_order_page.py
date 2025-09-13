import pytest
import allure
from utils.urls import Urls
from pages.home_page import YaScooterHomePage
from pages.order_page import YaScooterOrderPage
from utils.locators import YaScooterOrderPageLocator as Loc
from utils.test_data import YaScooterOrderPageData as order_data


@allure.epic("Создание заказа")
@allure.parent_suite("Домашняя страница → Заказ")
class TestOrderPage:

    @pytest.fixture
    def order_page(self, driver):
        """Открывает страницу заказа и принимает куки."""
        home = YaScooterHomePage(driver)
        order = YaScooterOrderPage(driver)
        order.go_to_site(Urls.ORDER_PAGE)
        home.click_cookie_accept()
        return order

    # --- Негативные проверки этапа "Для кого самокат" ---

    @allure.feature("Этап 'Для кого самокат'")
    @allure.story("Некорректные данные")
    @pytest.mark.parametrize("field,value,locator", [
        ("input_first_name", "Вqw", Loc.INCORRECT_FIRST_NAME_MESSAGE),
        ("input_last_name", "Вqw", Loc.INCORRECT_LAST_NAME_MESSAGE),
        ("input_address", "Вqw", Loc.INCORRECT_ADDRESS_MESSAGE),
        ("input_telephone_number", "Вqw", Loc.INCORRECT_TELEPHONE_NUMBER_MESSAGE),
    ])
    def test_incorrect_user_fields_show_error(self, order_page, field, value, locator):
        getattr(order_page, field)(value)
        order_page.go_next()
        assert order_page.find_element(locator).is_displayed(), \
            f"Поле {field} не показало сообщение об ошибке"

    @allure.feature("Этап 'Для кого самокат'")
    @allure.story("Пустое метро")
    def test_empty_subway_shows_error(self, order_page):
        order_page.go_next()
        assert order_page.find_element(Loc.INCORRECT_SUBWAY_MESSAGE).is_displayed(), \
            "При пустом поле метро ошибка не отображается"

    @allure.feature("Этап 'Для кого самокат'")
    @allure.story("Корректные данные")
    def test_correct_user_data_opens_rent_step(self, order_page):
        order_page.fill_user_data(order_data.data_sets["data_set1"])
        order_page.go_next()
        assert order_page.find_elements(Loc.ORDER_BUTTON), \
            "После корректного ввода не открылся этап 'Про аренду'"

    # --- Этап "Про аренду" ---

    @allure.feature("Этап 'Про аренду'")
    @allure.story("Оформление заказа")
    @pytest.mark.parametrize("data_set", ["data_set1", "data_set2"])
    def test_fill_rent_and_order_success(self, order_page, data_set):
        order_page.fill_user_data(order_data.data_sets[data_set])
        order_page.go_next()
        order_page.fill_rent_data(order_data.data_sets[data_set])
        order_page.click_order()
        order_page.click_accept_order()
        assert order_page.find_elements(Loc.ORDER_COMPLETED_INFO), \
            "Заказ не был успешно создан"

    # --- Полный путь заказа ---

    @allure.feature("Полный путь")
    @allure.story("Статус заказа")
    @pytest.mark.parametrize("data_set", ["data_set1", "data_set2"])
    def test_create_order_and_check_status(self, order_page, data_set):
        order_page.fill_user_data(order_data.data_sets[data_set])
        order_page.go_next()
        order_page.fill_rent_data(order_data.data_sets[data_set])
        order_page.click_order()
        order_page.click_accept_order()

        order_number = order_page.get_order_number()
        order_page.click_go_to_status()
        current_url = order_page.current_url()

        assert Urls.ORDER_STATUS_PAGE in current_url and order_number in current_url, \
            f"URL статуса заказа некорректный: {current_url}"

