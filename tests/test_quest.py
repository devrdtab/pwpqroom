from pages.home_page import HomePage
from constants import BASE_URL
from utils.date_utils import get_current_year

from playwright.sync_api import expect


def test_quest_page_title_test(page):
    """Проверка заголовка главной страницы"""
    home_page = HomePage(page)
    home_page.open()
    assert home_page.get_title() == "Квест комнаты Киев, независимый рейтинг квестов - реальные отзывы, обзоры на портале | Q-ROOM", "ЗАГОЛОВОК title НЕ СОВПАДАЕТ"
