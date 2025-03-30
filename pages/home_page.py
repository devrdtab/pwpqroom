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

    # def filter_select_params(self):
    #     filter_open_btn = "#expand-btn-container"
    #     filter_genres = "#filter_genres .filter-toggle__section"
    #     filter_genre_select = "#filter_genres .filter-toggle-title .filter-checker:nth-of-type(2)"
    #     count_players = "#count_players .filter-toggle__section"
    #     count_players_select = "#count_players .filter-toggle__section #players-2"
    #     filter_age = "#filter_age .filter-toggle__section"
    #     filter_age_select = '#filter_age .filter-toggle__section input[name="options5"]'
    #     filter_price = "#filter_price .filter-toggle__section"
    #     filter_price_select = '#filter_price .filter-toggle__section input[name="options650-850"]'
    #     apply_filter = ".apply-filter"
    #
    #     # Открываем фильтр сначала
    #     self.page.wait_for_selector(filter_open_btn, state="visible", timeout=10000)
    #     self.page.locator(filter_open_btn).click()
    #
    #     # Ждем, пока секции фильтра станут видимыми после открытия
    #     self.page.wait_for_selector(filter_genres, state="visible", timeout=10000)
    #     self.page.locator(filter_genres).click()
    #
    #     # Ждем конкретный элемент фильтра жанров
    #     self.page.wait_for_selector(filter_genre_select, state="visible", timeout=10000)
    #     self.page.locator(filter_genre_select).click()
    #
    #     self.page.wait_for_selector(count_players, state="visible", timeout=10000)
    #     self.page.locator(count_players).click()
    #     self.page.wait_for_selector(count_players_select, state="visible", timeout=10000)
    #     self.page.locator(count_players_select).check()
    #
    #     self.page.wait_for_selector(filter_age, state="visible", timeout=10000)
    #     self.page.locator(filter_age).click()
    #     self.page.wait_for_selector(filter_age_select, state="visible", timeout=10000)
    #     self.page.locator(filter_age_select).check()
    #
    #     self.page.wait_for_selector(filter_price, state="visible", timeout=10000)
    #     self.page.locator(filter_price).click()
    #     self.page.wait_for_selector(filter_price_select, state="visible", timeout=10000)
    #     self.page.locator(filter_price_select).click()
    #
    #     # Применяем фильтр
    #     self.page.wait_for_selector(apply_filter, state="visible", timeout=10000)
    #     self.page.locator(apply_filter).click()  # Предполагается, что это кнопка, а не чекбокс
    #
    #     # Ждем загрузки страницы после применения фильтра
    #     self.page.wait_for_load_state("networkidle")
    #
    # def get_current_url(self):
    #     return self.page.url

    def filter_open_close(self):
        # Открываем фильтр
        filter_open = self.page.wait_for_selector("#expand-btn-container", state="visible", timeout=10000)
        filter_open.click()
        print("Filter opened")

        # Проверяем кнопку закрытия
        filter_close = self.page.wait_for_selector(".close-filter", state="visible", timeout=10000)
        print(f"Close button visible: {filter_close.is_visible()}, enabled: {filter_close.is_enabled()}")
        filter_close.click()
        print("Filter closed")



    def filter_select_params(self):
        # Открываем фильтр
        self.page.wait_for_selector("#wrap_toggle", state="visible", timeout=10000)
        self.page.locator("#wrap_toggle").click()

        # Выбираем вид квеста (жанр "Ужасы")
        self.page.wait_for_selector('text="Выберите вид квеста"', state="visible", timeout=10000)
        self.page.get_by_text("Выберите вид квеста").click()
        self.page.wait_for_selector('#filter_genres >> text="Ужасы"', state="visible", timeout=10000)
        self.page.locator("#filter_genres").get_by_text("Ужасы").click()

        # Выбираем количество игроков (2)
        self.page.wait_for_selector('text="Выберите количество игроков"', state="visible", timeout=10000)
        self.page.get_by_text("Выберите количество игроков").click()
        self.page.wait_for_selector('#count_players >> text="2"', state="visible", timeout=10000)
        self.page.locator("#count_players").get_by_text("2").click()

        # Выбираем возраст (От 7 лет)
        self.page.wait_for_selector('text="От 7 лет"', state="visible", timeout=10000)
        self.page.get_by_text("От 7 лет", exact=True).click()

        # Выбираем цену (650-850 грн.)
        self.page.wait_for_selector('text="650-850 грн."', state="visible", timeout=10000)
        self.page.get_by_text("650-850 грн.").click()

        # Применяем фильтр
        self.page.wait_for_selector('button:has-text("Применить")', state="visible", timeout=10000)
        self.page.get_by_role("button", name="Применить").click()

        # Проверяем, что произошло после клика
        self.page.wait_for_load_state("networkidle", timeout=20000)  # Ждем завершения загрузки
        print(f"URL after apply (immediate): {self.page.url}")

        # Ждем конкретный URL
        try:
            self.page.wait_for_url("https://q-room.com/?age=7&genre=horror&players=2&price=650,850", timeout=20000)
            print("URL updated successfully to expected value")
        except Exception as e:
            print(f"Failed to reach expected URL: {e}")
            print(f"Final URL after filters: {self.page.url}")
            self.page.screenshot(path="after_apply_failure.png")  # Скриншот для отладки
            raise  # Повторно выбрасываем исключение, чтобы тест упал






















    # def quest_title(self):
    #     return self.page.locator(".top-quest-info__name").inner_text().strip()
        # self.page.wait_for_selector(".top-quest-info__name", state="visible", timeout=10000)
        # return self.page.locator(".top-quest-info__name").text_content().strip()

    # def filter_open(self):
    #     self.page.locator('#wrap_toggle').click()
