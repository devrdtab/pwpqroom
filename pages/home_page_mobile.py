from pages.base_page import BasePage
from playwright.async_api import Page as AsyncPage
from utils.constants import DEFAULT_TIMEOUT
import allure


# Асинхронный класс для мобильных тестов
class AsyncHomePage(BasePage):
    def __init__(self, page: AsyncPage):
        super().__init__(page, '/')  # Главная страница, self.url = BASE_URL + '/'

    async def get_current_url(self):
        return self.page.url

    async def open(self):
        await self.page.goto(self.url)  # Используем self.url из BasePage

    async def toggle_burger_menu(self):
        burger = self.page.locator('.burger')
        system_links = self.page.locator('.system-links')
        top_links = self.page.locator('.top-links')

        await burger.wait_for(state='visible', timeout=DEFAULT_TIMEOUT)
        await burger.click()

        is_system_links_active = 'active' in (await system_links.get_attribute('class') or '')
        is_top_links_active = 'active' in (await top_links.get_attribute('class') or '')
        is_burger_active = 'active' in (await burger.get_attribute('class') or '')
        return is_system_links_active, is_top_links_active, is_burger_active

    async def is_burger_menu_visible(self):
        system_links_visible = await self.page.locator('.system-links').is_visible()
        top_links_visible = await self.page.locator('.top-links').is_visible()
        return system_links_visible and top_links_visible

    async def switch_language_mobile(self):
        switcher = self.page.locator('.switcher-inner')
        await switcher.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        print(f"Switcher found: {await switcher.count()} elements")
        await switcher.click()

    async def change_city_mobile(self):
        city_switcher = self.page.locator('.city')
        city_target = self.page.locator('.city .dropdown-select-list ul li:nth-of-type(2) a')
        await city_switcher.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        await city_switcher.click()
        await city_target.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)
        await city_target.click()
