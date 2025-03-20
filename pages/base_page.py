from playwright.sync_api import Page
from utils.constants import BASE_URL

class BasePage:
    def __init__(self, page: Page, path: str = ""):
        self.page = page
        self.url = f"{BASE_URL}{path}"

    def open(self):
        """Открывает страницу в браузере"""
        self.page.goto(self.url)

    def get_title(self):
        """Возвращает заголовок страницы"""
        return self.page.title()