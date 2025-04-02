from pages.base_page import BasePage
from playwright.async_api import Page as AsyncPage


# Асинхронный класс для мобильных тестов
class AsyncHomePage(BasePage):
    def __init__(self, page: AsyncPage):
        super().__init__(page, "/")  # Главная страница, self.url = BASE_URL + "/"

    async def open(self):
        await self.page.goto(self.url)  # Используем self.url из BasePage

    async def toggle_burger_menu(self):
        burger = self.page.locator(".burger")
        system_links = self.page.locator(".system-links")
        top_links = self.page.locator(".top-links")

        await burger.wait_for(state="visible", timeout=10000)
        await burger.click()

        is_system_links_active = "active" in (await system_links.get_attribute("class") or "")
        is_top_links_active = "active" in (await top_links.get_attribute("class") or "")
        is_burger_active = "active" in (await burger.get_attribute("class") or "")
        return is_system_links_active, is_top_links_active, is_burger_active

    async def is_burger_menu_visible(self):
        system_links_visible = await self.page.locator(".system-links").is_visible()
        top_links_visible = await self.page.locator(".top-links").is_visible()
        return system_links_visible and top_links_visible
