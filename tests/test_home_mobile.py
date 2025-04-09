import pytest
import allure
from pages.home_page_mobile import AsyncHomePage
from utils.constants import BASE_URL
from utils.mobile_devices import MOBILE_DEVICES
from utils.constants import DEFAULT_TIMEOUT

DEVICES = list(MOBILE_DEVICES.keys())


@pytest.mark.asyncio
@pytest.mark.parametrize("mobile_page", DEVICES, indirect=True)
@allure.title('Burger Menu Toggle')
@allure.description_html('Checking burger menu toggle functionality on mobile')
@allure.feature('Burger Menu')
@allure.story('Mobile navigation')
async def test_burger_menu_toggle(mobile_page, device):
    with allure.step(f'Открываем главную страницу на устройстве: {device}'):
        home_page = AsyncHomePage(mobile_page)
        await home_page.open()
        await mobile_page.wait_for_load_state("load", timeout=DEFAULT_TIMEOUT)

    with allure.step('Кликаем на бургер-меню, проверяем открытие'):
        is_system_links_active, is_top_links_active, is_burger_active = await home_page.toggle_burger_menu()
        assert is_system_links_active, "Класс .active не добавлен к .system-links после открытия"
        assert is_top_links_active, "Класс .active не добавлен к .top-links после открытия"
        assert is_burger_active, "Класс .active не добавлен к .burger после открытия"
        assert await home_page.is_burger_menu_visible(), "Меню (.system-links и .top-links) не видно на экране"

    with allure.step('Кликаем на бургер-меню снова, проверяем закрытие'):
        is_system_links_active, is_top_links_active, is_burger_active = await home_page.toggle_burger_menu()
        await mobile_page.wait_for_timeout(1000)
        assert not is_system_links_active, "Класс .active не удален из .system-links после закрытия"
        assert not is_top_links_active, "Класс .active не удален из .top-links после закрытия"
        assert not is_burger_active, "Класс .active не удален из .burger после закрытия"
        assert not await home_page.is_burger_menu_visible(), "Меню (.system-links и .top-links) все еще видно после закрытия"


@pytest.mark.asyncio
@pytest.mark.parametrize("mobile_page", DEVICES, indirect=True)
@allure.title('Switch Language Toggle')
@allure.description_html('Checking the mobile language switching operation')
@allure.feature('Switch Language')
@allure.story('General functionality of the site')
async def test_mobile_lang_switcher(mobile_page, device):
    with allure.step(f'Открываем главную страницу на устройстве: {device}'):
        home_page = AsyncHomePage(mobile_page)
        await home_page.open()
        await mobile_page.wait_for_load_state("load", timeout=DEFAULT_TIMEOUT)
    with allure.step('Кликаем на переключатель языков, проверяем открытие'):
        await home_page.switch_language_mobile()
        await mobile_page.wait_for_load_state("load", timeout=DEFAULT_TIMEOUT)
    with allure.step('Проверяем что язык переключился'):
        assert await home_page.get_current_url() == f"{BASE_URL}/ua", "Язык не переключился"


@pytest.mark.asyncio
@pytest.mark.parametrize("mobile_page", DEVICES, indirect=True)
@allure.title('Switching cities mobile')
@allure.description_html('Checking the operation of city switching mobile')
@allure.feature('City changes mobile')
@allure.story('General functionality of the site')
async def test_change_city_mobile(mobile_page, device):
    with allure.step(f'Открываем главную страницу на устройстве: {device}'):
        home_page = AsyncHomePage(mobile_page)
        await home_page.open()
        await mobile_page.wait_for_load_state("load", timeout=DEFAULT_TIMEOUT)
    with allure.step('Кликаем на выпадающий список и кликаем на город Одесса'):
        await home_page.change_city_mobile()
        await mobile_page.wait_for_load_state("load", timeout=DEFAULT_TIMEOUT)
    with allure.step('Проверяем что загрузилась страница Одесса и URL https://odessa.q-room.com/'):
        final_url = await home_page.get_current_url()
        assert final_url == 'https://odessa.q-room.com/', "Город не переключился"
