from pages.home_page import HomePage
from utils.constants import BASE_URL
from utils.date_utils import get_current_year


# @pytest.mark.skip('Default title test')
def test_home_page_title(page, tests_iteration):
    """Проверка заголовка главной страницы"""
    home_page = HomePage(page)
    home_page.open()
    assert home_page.get_title() == "Квест комнаты Киев, независимый рейтинг квестов - реальные отзывы, обзоры на портале | Q-ROOM", "ЗАГОЛОВОК title НЕ СОВПАДАЕТ"


def test_switch_language(page):
    """Проверка переключения языка"""
    home_page = HomePage(page)
    home_page.open()
    home_page.switch_language()
    assert home_page.get_current_url() == f"{BASE_URL}/ua", "Язык не переключился"


# @pytest.mark.regression
def test_change_city(page):
    """Проверка переключения города"""
    home_page = HomePage(page)
    home_page.open()
    home_page.change_city()
    assert home_page.get_current_url() == 'https://lvov.q-room.com/', "Город не переключился"


def test_copyright(page, request):
    # test_name = request.node.name
    home_page = HomePage(page)
    home_page.open()
    datecopyright = home_page.check_copyright()
    assert datecopyright == (f"© 2015—{get_current_year()} Q-ROOM"), "Copyright не соответствует"


def test_search_field(page):
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
    assert has_venom, "Первый результат не содержит 'VENOM'"
    print(f"✅ Найдено {result_count} результатов. Первый результат содержит 'VENOM': {has_venom}")


def test_seo_readmore(page):
    """Проверка переключения языка"""
    home_page = HomePage(page)
    home_page.open()
    home_page.show_seo_text()
    assert "active" in page.locator(".readmore__hide").get_attribute("active"), "Элемент не имеет класс .active"


def test_read_more_active(page):
    home_page = HomePage(page)
    home_page.open()
    home_page.click_read_more()
    assert home_page.is_element_active(), "Элемент .readmore__hide не получил класс 'active'"
