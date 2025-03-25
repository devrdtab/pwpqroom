import pytest
import allure
import os
from playwright.sync_api import sync_playwright
from utils.date_utils import get_current_date

# Определяем корневую папку проекта (qroom)
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))  # Путь к tests/
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "qroom"))  # Явно указываем qroom/
SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "artifacts", "screenshots")

# Создаём папку для скриншотов, если её нет
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Отладка
# print(f"📂 Корневая папка проекта: {PROJECT_DIR}")
# print(f"📸 Скриншоты будут сохраняться в: {SCREENSHOT_DIR}")

# @pytest.fixture(scope="function", params=["chromium", "firefox", "webkit"])
@pytest.fixture(scope="function", params=["chromium"])
def browser(request):
    """Фикстура для запуска тестов в Chrome, Firefox, WebKit"""
    with sync_playwright() as playwright:
        browser = getattr(playwright, request.param).launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function", autouse=True)
def page(browser):
    """Фикстура для создания страницы"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет скриншот при ошибке и добавляет в Allure"""
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        page = item.funcargs.get("page")
        browser_name = item.callspec.params["browser"]

        if page:
            test_name = item.name
            timestamp = get_current_date().replace(":", "-")
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{browser_name}_{timestamp}.png")

            # Отладка
            # print(f"🔍 Текущий каталог: {os.getcwd()}")
            # print(f"📸 Путь сохранения: {screenshot_path}")

            # Делаем скриншот и сохраняем
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"✅ Скриншот сохранен: {screenshot_path}")
                allure.attach.file(screenshot_path, name=f"{test_name}_{browser_name}",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"❌ Ошибка при сохранении скриншота: {e}")

@pytest.fixture(scope='session')
def tests_iteration():
    print('\n= = = = = Iteration Started = = = = = ')
    yield
    print('\n= = = = = Iteration Finished = = = = = ')

@pytest.mark.regression
def tests_regression():
    yield
