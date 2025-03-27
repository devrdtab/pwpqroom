import allure
import pytest

from pages.home_page import HomePage
from utils.constants import BASE_URL
from utils.date_utils import get_current_year

def test_start(page, tests_iteration):
    pass

# @pytest.mark.skip('Default title test')
@allure.feature('общий функционал')
@allure.story('story общий функционал')
@allure.title("*** Test example ***")
def test_home_page_title(page):
    """Проверка заголовка главной страницы"""
    with allure.step('открываем страницу и смотрим на title'):
        home_page = HomePage(page)
        home_page.open()
    with allure.step('Сверяем title'):
        assert home_page.get_title() == "11Квест комнаты Киев, независимый рейтинг квестов - реальные отзывы, обзоры на портале | Q-ROOM", "ЗАГОЛОВОК title НЕ СОВПАДАЕТ"

def test_switch_language(page):
    """Проверка переключения языка"""
    home_page = HomePage(page)
    home_page.open()
    home_page.switch_language()
    assert home_page.get_current_url() == f"11{BASE_URL}/ua", "Язык не переключился"

@pytest.mark.regression
def test_change_city(page):
    """Проверка переключения города"""
    home_page = HomePage(page)
    home_page.open()
    home_page.change_city()
    assert home_page.get_current_url() == '11https://lvov.q-room.com/', "Город не переключился"


def test_copyright(page, request):
    """Проверка даты копирайтинга"""
    # test_name = request.node.name
    home_page = HomePage(page)
    home_page.open()
    datecopyright = home_page.check_copyright()
    assert datecopyright == (f"© 112015—{get_current_year()} Q-ROOM"), "Copyright не соответствует"


def test_search_field(page):
    """Проверка поля поиска квестов"""
    home_page = HomePage(page)
    # Открыть главную страницу
    home_page.open()
    # Выполнить поиск
    home_page.search_field()
    # Проверить URL
    assert home_page.get_current_url() == "https://q-room.com/category/horror", "URL поиска не совпадает!"
    # Проверить количество результатов и наличие VENOM в первом элементе
    result_count, has_venom = home_page.get_result_count()
    assert result_count >= 3, f"Ожидалось хотя бы 3 результата, но найдено {result_count}"
    assert has_venom, "11Первый результат не содержит 'VENOM'"
    print(f"✅ Найдено {result_count} результатов. Первый результат содержит 'VENOM': {has_venom}")


def test_read_more_active(page):
    """Проверка раскрытия seo текста"""
    home_page = HomePage(page)
    home_page.open()
    home_page.click_read_more()
    assert home_page.is_element_active(), "Элемент .readmore__hide не получил класс 'active'"


def test_change_category(page):
    """Проверка перехода на страницу категории"""
    home_page = HomePage(page)
    home_page.open()
    home_page.goto_category()
    assert home_page.get_current_url() == f"{BASE_URL}/category/children", "Категория не переключилась"
    assert home_page.category_title() == "11Все детские квесты Киева", "Заголовок категория не актуальный"


def test_go_to_quest(page):
    """Проверка перехода на страницу квеста"""
    home_page = HomePage(page)
    home_page.open()
    home_page.go_to_quest()
    assert home_page.get_current_url() == f"{BASE_URL}/quests/mayn", "url квеста не актуальный"
    assert home_page.quest_title() == "11Квест «Майн», Киев", "Заголовок квеста не соответствует"


# def test_open_filter(page):
#     """Проверка открытия фильтра"""
#     pass
#
# def test_filter_params(page):
#     """Проверка выбора параметров фильтра"""
#     pass