from pages.base_page import BasePage
import allure


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page, "/")  # Главная страница

    def switch_language(self):
        with allure.step('нажимаем на переключатель языков'):
            """Нажимает на переключатель языка"""
            self.page.locator(".switcher-inner").click()

    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.page.url

    def change_city(self):
        """Нажимает на переключатель языка"""
        self.page.locator(".city").click()
        self.page.locator(".city .dropdown-select-list ul li:nth-of-type(5) a").click()

    def check_copyright(self):
        """проверяет текущий год"""
        return self.page.locator(".copyright > div:first-child").inner_text()
        # self.page.wait_for_load_state('load')

    def search_field(self):
        """Ищет 'ужасы' и выбирает категорию"""
        search_input = self.page.locator(
            "body > main > div.home-search > div > div > div > div > div:nth-child(2) > div > div > form > input[type=text]")
        search_input.fill("ужасы")

        # Ожидание появления результатов поиска
        self.page.wait_for_selector(".ajax-search.active .ajax-search__result ul li a", timeout=10000)

        # Клик по найденной категории "Ужасы"
        self.page.locator(".ajax-search.active .ajax-search__result ul li a >> text=Ужасы").click()

        # Ожидание загрузки новой страницы после клика
        self.page.wait_for_load_state("domcontentloaded")

    def get_result_count(self):
        """Ожидает загрузку страницы, проверяет количество div внутри .filter_result
           и проверяет, содержит ли первый div ссылку с текстом VENOM."""

        self.page.wait_for_load_state("networkidle")  # Дождаться полной загрузки
        self.page.wait_for_selector(".filter-result .row", state="visible", timeout=15000)  # Ждем появления блока

        # Подсчет div внутри .filter_result
        div_count = self.page.locator(".filter-result .row > div").count()

        # Проверка, содержит ли первый div в .filter_result элемент .quest-name a с текстом VENOM
        first_quest = self.page.locator(".filter-result > div").first
        has_venom = first_quest.locator(".quest-name a", has_text="VENOM").count() > 0

        return div_count, has_venom

    def click_read_more(self):
        self.page.locator(".readmore__link").click()

    def is_element_active(self) -> bool:
        element = self.page.locator(".readmore__hide")
        return "active" in element.get_attribute("class")

    def goto_category(self):
        self.page.locator(".home-search .top-search-gender .quest-category a").nth(3).click()
        # self.page.wait_for_selector(".home-search .top-search-gender .quest-category a", state="visible", timeout=10000")
        # self.page.locator(".home-search .top-search-gender .quest-category a:nth-of-type(3)").click()

    def category_title(self):
        return self.page.locator(".home-search .top-search-gender .search-title").inner_text()







    def go_to_quest(self):
        quest_locator = "#filtertab-1 .filter-result .row .col-xl-4.col-lg-4.col-md-4.col-sm-12:nth-child(3)"
        link_locator = f"{quest_locator} a.full-link"
        name_locator = f"{quest_locator} .quest-name > div a"

        # Дожидаемся появления элементов
        self.page.wait_for_selector(name_locator, state="visible", timeout=10000)
        self.page.wait_for_selector(link_locator, state="attached", timeout=10000)

        # Получаем название и ссылку
        element_name = self.page.locator(name_locator).inner_text()
        element_link = self.page.locator(link_locator).get_attribute("href")

        # Кликаем по элементу
        self.page.locator(quest_locator).click(timeout=10000)

        # Ждем загрузки новой страницы
        self.page.wait_for_load_state("networkidle")

        return element_name, element_link

        # print(f"LINK: {element_link}")
        # print(f"CURRENT URL: {self.page.url}")
























    # def quest_title(self):
    #     return self.page.locator(".top-quest-info__name").inner_text().strip()
        # self.page.wait_for_selector(".top-quest-info__name", state="visible", timeout=10000)
        # return self.page.locator(".top-quest-info__name").text_content().strip()

    # def filter_open(self):
    #     self.page.locator('#wrap_toggle').click()
