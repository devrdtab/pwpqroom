from pages.base_page import BasePage
from playwright.sync_api import Page as SyncPage
from utils.constants import DEFAULT_TIMEOUT
import allure


# Синхронный класс для десктопных тестов
class HomePage(BasePage):
    def __init__(self, page: SyncPage):
        super().__init__(page, "/")  # Главная страница

    def switch_language(self):
        with allure.step('Нажимаем на переключатель языков'):
            self.page.locator(".switcher-inner").click()

    def get_current_url(self):
        return self.page.url

    def change_city(self):
        self.page.locator(".city").click()
        self.page.locator(".city .dropdown-select-list ul li:nth-of-type(5) a").click()

    def check_copyright(self):
        return self.page.locator(".copyright > div:first-child").inner_text()

    def search_field(self):
        search_input = self.page.locator(
            "body > main > div.home-search > div > div > div > div > div:nth-child(2) > div > div > form > input[type=text]")
        search_input.fill("ужасы")
        self.page.wait_for_selector(".ajax-search.active .ajax-search__result ul li a", timeout=DEFAULT_TIMEOUT)
        self.page.locator(".ajax-search.active .ajax-search__result ul li a >> text=Ужасы").click()
        self.page.wait_for_load_state("domcontentloaded")

    def get_result_count(self):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(".filter-result .row", state="visible", timeout=15000)
        div_count = self.page.locator(".filter-result .row > div").count()
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

    def category_title(self):
        return self.page.locator(".home-search .top-search-gender .search-title").inner_text()

    def go_to_quest(self):
        quest_locator = "#filtertab-1 .filter-result .row .col-xl-4.col-lg-4.col-md-4.col-sm-12:nth-child(3)"
        link_locator = f"{quest_locator} a.full-link"
        name_locator = f"{quest_locator} .quest-name > div a"
        self.page.wait_for_selector(name_locator, state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.wait_for_selector(link_locator, state="attached", timeout=DEFAULT_TIMEOUT)
        element_name = self.page.locator(name_locator).inner_text()
        element_link = self.page.locator(link_locator).get_attribute("href")
        self.page.locator(quest_locator).click(timeout=DEFAULT_TIMEOUT)
        self.page.wait_for_load_state("networkidle")
        return element_name, element_link

    def filter_open_close(self):
        filter_open = self.page.wait_for_selector("#expand-btn-container", state="visible", timeout=DEFAULT_TIMEOUT)
        filter_open.click()
        print("Filter opened")
        filter_close = self.page.wait_for_selector(".close-filter", state="visible", timeout=DEFAULT_TIMEOUT)
        print(f"Close button visible: {filter_close.is_visible()}, enabled: {filter_close.is_enabled()}")
        filter_close.click()
        print("Filter closed")

    def filter_select_params(self):
        self.page.wait_for_selector("#wrap_toggle", state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.locator("#wrap_toggle").click()
        self.page.wait_for_selector('text="Выберите вид квеста"', state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.get_by_text("Выберите вид квеста").click()
        self.page.wait_for_selector('#filter_genres >> text="Ужасы"', state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.locator("#filter_genres").get_by_text("Ужасы").click()
        self.page.wait_for_selector('text="Выберите количество игроков"', state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.get_by_text("Выберите количество игроков").click()
        self.page.wait_for_selector('#count_players >> text="2"', state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.locator("#count_players").get_by_text("2").click()
        self.page.wait_for_selector('text="От 7 лет"', state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.get_by_text("От 7 лет", exact=True).click()
        self.page.wait_for_selector('text="650-850 грн."', state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.get_by_text("650-850 грн.").click()
        self.page.wait_for_selector('button:has-text("Применить")', state="visible", timeout=DEFAULT_TIMEOUT)
        self.page.get_by_role("button", name="Применить").click()
        self.page.wait_for_load_state("networkidle", timeout=20000)
        print(f"URL after apply (immediate): {self.page.url}")
        try:
            self.page.wait_for_url("https://q-room.com/?age=7&genre=horror&players=2&price=650,850", timeout=20000)
            print("URL updated successfully to expected value")
        except Exception as e:
            print(f"Failed to reach expected URL: {e}")
            print(f"Final URL after filters: {self.page.url}")
            self.page.screenshot(path="after_apply_failure.png")
            raise
