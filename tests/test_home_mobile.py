import pytest
import allure
from pages.home_page_mobile import AsyncHomePage
from utils.constants import BASE_URL
from utils.mobile_devices import MOBILE_DEVICES

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
        await mobile_page.wait_for_load_state("load", timeout=10000)

    with allure.step('Кликаем на бургер-меню, проверяем открытие'):
        is_system_links_active, is_top_links_active, is_burger_active = await home_page.toggle_burger_menu()
        assert is_system_links_active
        assert is_top_links_active
        assert is_burger_active
        assert await home_page.is_burger_menu_visible(), "Меню (.system-links и .top-links) не видно на экране"

    with allure.step('Кликаем на бургер-меню снова, проверяем закрытие'):
        is_system_links_active, is_top_links_active, is_burger_active = await home_page.toggle_burger_menu()
        await mobile_page.wait_for_timeout(1000)
        assert not is_system_links_active
        assert not is_top_links_active
        assert not is_burger_active
        assert not await home_page.is_burger_menu_visible(), "Меню (.system-links и .top-links) все еще видно после закрытия"
