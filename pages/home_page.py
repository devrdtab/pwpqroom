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

    # def searchfield(self):
    #     return self.page.locator("")

