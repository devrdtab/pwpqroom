from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page, "/")  # Главная страница

    def switch_language(self):
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
        search_input = self.page.locator("body > main > div.home-search > div > div > div > div > div:nth-child(2) > div > div > form > input[type=text]")
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

