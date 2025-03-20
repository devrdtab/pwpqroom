from pages.home_page import HomePage
from utils.constants import BASE_URL
from utils.date_utils import get_current_year


# @pytest.mark.skip('Default title test')
def test_home_page_title_test(page, tests_iteration):
    """Проверка заголовка главной страницы"""
    home_page = HomePage(page)
    home_page.open()
    assert home_page.get_title() == "Квест комнаты Киев, независимый рейтинг квестов - реальные отзывы, обзоры на портале | Q-ROOM", "ЗАГОЛОВОК title НЕ СОВПАДАЕТ"


def test_switch_language_test(page):
    """Проверка переключения языка"""
    home_page = HomePage(page)
    home_page.open()
    home_page.switch_language()
    assert home_page.get_current_url() == f"{BASE_URL}/ua", "Язык не переключился"

# @pytest.mark.regression
def test_change_city_test(page):
    """Проверка переключения города"""
    home_page = HomePage(page)
    home_page.open()
    home_page.change_city()
    assert home_page.get_current_url() == 'https://lvov.q-room.com/', "Город не переключился"

def test_copyright_test(page, request):
    # test_name = request.node.name
    home_page = HomePage(page)
    home_page.open()
    datecopyright = home_page.check_copyright()
    assert datecopyright == (f"© 2015—{get_current_year()} Q-ROOM"), "Copyright не соответствует"