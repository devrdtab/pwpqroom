import allure
import pytest

from pages.home_page import HomePage
from utils.constants import BASE_URL
from utils.date_utils import get_current_year

def test_start(page, tests_iteration):
    pass

# @pytest.mark.skip('Default title test')
@allure.title('Title страницы')
@allure.description_html('Проверка заголовка главной страницы')
@allure.issue('https://example.com/browse/BUG-001', name='BUG-001')
@allure.feature('Заголовое главной страницы')
@allure.story('story Общий функционал работы сайта')
def test_home_page_title(page):
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        home_page.open()
    with allure.step('Сверяем title'):
        assert home_page.get_title() == "Квест комнаты Киев, независимый рейтинг квестов - реальные отзывы, обзоры на портале | Q-ROOM", "ЗАГОЛОВОК title НЕ СОВПАДАЕТ"

@allure.title('Переключение языка')
@allure.description_html('Проверка работы переключения языка')
@allure.issue('https://example.com/browse/BUG-002', name='BUG-002')
@allure.feature('Languages')
@allure.story('story Общий функционал работы сайта')
def test_switch_language(page):
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        home_page.open()
    with allure.step('Нажимаем на переключатель языков'):
        home_page.switch_language()
    with allure.step('Проверяем перфикс в url на наличие нужного языка'):
        assert home_page.get_current_url() == f"{BASE_URL}/ua", "Язык не переключился"

# @pytest.mark.regression
@allure.title('Переключение города')
@allure.description_html('Проверка работы переключения городов')
@allure.issue('https://example.com/browse/BUG-003', name='BUG-003')
@allure.feature('City changes')
@allure.story('story Общий функционал работы сайта')
def test_change_city(page):
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        home_page.open()
    with allure.step('Кликаем на выпадающий список и кликаем на город Львов'):
        home_page.change_city()
    with allure.step('Проверяем что загрузилась страница Львов и URL https://lvov.q-room.com/'):
        assert home_page.get_current_url() == 'https://lvov.q-room.com/', "Город не переключился"


@allure.title('Копирайтинг')
@allure.description_html('Проверка даты копирайтинга')
@allure.issue('https://example.com/browse/BUG-04', name='BUG-004')
@allure.feature('Copyright date')
@allure.story('story Общий функционал работы сайта')
def test_copyright(page, request):
    # test_name = request.node.name
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        home_page.open()
    with allure.step('Считываем даты в поле Copyright'):
        datecopyright = home_page.check_copyright()
    with allure.step('Сравниваем год в поле Copyright с текущим годом'):
        assert datecopyright == (f"© 2015—{get_current_year()} Q-ROOM"), "Copyright не соответствует"

@allure.title('Поле поиск')
@allure.description_html('Проверяем работу поля поиска квестов')
@allure.issue('https://example.com/browse/BUG-05', name='BUG-005')
@allure.feature('Поиск')
@allure.story('story Поле поиска квестов')
def test_search_field(page):
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        # Открыть главную страницу
        home_page.open()
    with allure.step('Вводим запрос в поле поиска'):
        # Выполнить поиск
        home_page.search_field()
    # Проверить URL
    with allure.step('Проверяем результыт поиска согласно запросу'):
        assert home_page.get_current_url() == "https://q-room.com/category/horror", "URL поиска не совпадает!"
        # Проверить количество результатов и наличие VENOM в первом элементе
        result_count, has_venom = home_page.get_result_count()
        assert result_count >= 3, f"Ожидалось хотя бы 3 результата, но найдено {result_count}"
        assert has_venom, "Первый результат не содержит 'VENOM'"
        # print(f"✅ Найдено {result_count} результатов. Первый результат содержит 'VENOM': {has_venom}")


@allure.title('Отобразить/скрыть seo текст')
@allure.description_html('Проверяем работу функционала отображения/скрытия')
@allure.issue('https://example.com/browse/BUG-06', name='BUG-005')
@allure.feature('Toggle (Show/hide)')
@allure.story('story Общий функционал работы сайта')
def test_read_more_active(page):
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        home_page.open()
    with allure.step('Клик на "Раскрыть"'):
        home_page.click_read_more()
    with allure.step('Проверяем что текст полностью раскрылся'):
        assert home_page.is_element_active(), "Элемент .readmore__hide не получил класс 'active'"

@allure.title('Перехода на страницу категории')
@allure.description_html('Проверяем работу перехода на страницу категории при клике на ссылку')
@allure.issue('https://example.com/browse/BUG-07', name='BUG-007')
@allure.feature('Category change')
@allure.story('story Общий функционал работы сайта')
def test_change_category(page):
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        home_page.open()
    with allure.step('В меню категорий кликаем на категорию "детские"'):
        home_page.goto_category()
    with allure.step('Проверяем что отобразиласьs страница с дескими квестами и url /category/children'):
        assert home_page.get_current_url() == f"{BASE_URL}/category/children", "Категория не переключилась"
        assert home_page.category_title() == "Все детские квесты Киева", "Заголовок категория не актуальный"

@allure.title('Переход на страницу квеста')
@allure.description_html('Проверяем работу перехода на страницу квеста при клике на ссылку')
@allure.issue('https://example.com/browse/BUG-08', name='BUG-008')
@allure.feature('Quest change')
@allure.story('story Общий функционал работы сайта')
def test_go_to_quest(page):
    with allure.step('Открываем главную страницу'):
        home_page = HomePage(page)
        home_page.open()

    with allure.step('В списке квестов кликаем на квест и получаем данные'):
        element_name, element_link = home_page.go_to_quest()

    with allure.step('Проверяем что отобразилась страница и имеет те же имя и ссылку'):
        current_url = home_page.get_current_url()
        expected_url = "https://q-room.com/quests/maetok-monstriv"

        assert current_url == expected_url, f"Ожидаемый URL: {expected_url}, получен: {current_url}"

        displayed_name = page.locator(".top-quest-info__name").inner_text().strip()
        # Убираем "Квест", ", Киев" и кавычки
        cleaned_displayed_name = displayed_name.replace("Квест", "", 1).rstrip(", Киев").replace("«", "").replace("»",
                                                                                                                  "").strip()

        # Нормализуем element_name, убирая кавычки, если они есть
        cleaned_element_name = element_name.replace("«", "").replace("»", "").strip()

        assert cleaned_element_name == cleaned_displayed_name, \
            f"Ожидаемое название '{cleaned_element_name}', получено '{cleaned_displayed_name}'"

        # print(f"*****CURRENT URL: {current_url}")
        # print(f"*****ORIGINAL QUEST NAME: {element_name}")
        # print(f"*****CLEANED QUEST NAME: {cleaned_element_name}")
        # print(f"*****DISPLAYED NAME: {displayed_name}")
        # print(f"*****CLEANED DISPLAYED NAME: {cleaned_displayed_name}")


































# def test_open_filter(page):
#     """Проверка открытия фильтра"""
#     pass
#
# def test_filter_params(page):
#     """Проверка выбора параметров фильтра"""
#     pass