# @pytest.mark.parametrize("mobile_page", ["iPhone 13"], indirect=True)
# @pytest.mark.parametrize("mobile_page", ["iPhone 13", "Galaxy S21"], indirect=True)
import pytest
import allure
from pages.home_page import HomePage
from utils.mobile_devices import MOBILE_DEVICES

# Список всех устройств из MOBILE_DEVICES
DEVICES = list(MOBILE_DEVICES.keys())

@pytest.mark.parametrize("mobile_page", DEVICES, indirect=True)
@allure.title('Burger Menu Toggle')
@allure.description_html('Checking burger menu toggle functionality on mobile')
@allure.feature('Burger Menu')
@allure.story('Mobile navigation')
def test_burger_menu_toggle(mobile_page):
    # Определяем имя устройства по viewport
    device = [d for d in MOBILE_DEVICES if MOBILE_DEVICES[d]["viewport"] == mobile_page.viewport_size][0]
    print(f"Размер окна: {mobile_page.viewport_size}, устройство: {device}")
    with allure.step(f'Открываем главную страницу на устройстве: {device}'):
        home_page = HomePage(mobile_page)
        home_page.open()
        # Ждем полной загрузки страницы
        mobile_page.wait_for_load_state("load", timeout=10000)

    with allure.step('Кликаем на бургер-меню, проверяем открытие'):
        is_system_links_active, is_top_links_active, is_burger_active = home_page.toggle_burger_menu()
        print(f"После открытия: .system-links active: {is_system_links_active}, .top-links active: {is_top_links_active}, .burger active: {is_burger_active}, меню видимо: {home_page.is_burger_menu_visible()}")
        assert is_system_links_active, "Класс .active не добавлен к .system-links после открытия"
        assert is_top_links_active, "Класс .active не добавлен к .top-links после открытия"
        assert is_burger_active, "Класс .active не добавлен к .burger после открытия"
        assert home_page.is_burger_menu_visible(), "Меню (.system-links и .top-links) не видно на экране"

    with allure.step('Кликаем на бургер-меню снова, проверяем закрытие'):
        is_system_links_active, is_top_links_active, is_burger_active = home_page.toggle_burger_menu()
        # Ждем завершения анимации, если есть
        mobile_page.wait_for_timeout(1000)
        print(f"После закрытия: .system-links active: {is_system_links_active}, .top-links active: {is_top_links_active}, .burger active: {is_burger_active}, меню видимо: {home_page.is_burger_menu_visible()}")
        assert not is_system_links_active, "Класс .active не удален из .system-links после закрытия"
        assert not is_top_links_active, "Класс .active не удален из .top-links после закрытия"
        assert not is_burger_active, "Класс .active не удален из .burger после закрытия"
        assert not home_page.is_burger_menu_visible(), "Меню (.system-links и .top-links) все еще видно после закрытия"