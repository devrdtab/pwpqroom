import pytest
import allure
import os
from playwright.sync_api import sync_playwright
from utils.date_utils import get_current_date
from utils.mobile_devices import MOBILE_DEVICES

# Определяем корневую папку проекта (qroom)
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))  # Путь к tests/
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "qroom"))  # Явно указываем qroom/
SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "artifacts", "screenshots")

# Создаём папку для скриншотов, если её нет
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Фикстура для запуска тестов в Chrome, Firefox, WebKit
# @pytest.fixture(scope="function", params=["chromium"])
@pytest.fixture(scope="function", params=["chromium", "firefox", "webkit"])
def browser(request):
    with sync_playwright() as playwright:
        browser = getattr(playwright, request.param).launch(headless=False)
        yield browser
        browser.close()

# Фикстура для создания страницы
@pytest.fixture(scope="function", autouse=True)
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()

# Сохраняет скриншот при ошибке и добавляет в Allure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
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

# Отмечает начало и конец тестов
@pytest.fixture(scope='session')
def tests_iteration():
    print('\n= = = = = Iteration Started = = = = = ')
    yield
    print('\n= = = = = Iteration Finished = = = = = ')

# Фикстура для отметки "регрессия"
@pytest.mark.regression
def tests_regression():
    yield


# ----MOBILE_DEVICES SETTINGS---
# Фикстура для запуска тестов в указанном браузере
@pytest.fixture(scope="function")
def browser_mobile(request):
    device = request.getfixturevalue("mobile_page")._context._options.get("device")
    browser_type = MOBILE_DEVICES[device]["defaultBrowserType"] if device in MOBILE_DEVICES else "chromium"
    with sync_playwright() as playwright:
        browser = getattr(playwright, browser_type).launch(headless=False)
        yield browser
        browser.close()

# Фикстура для создания страницы на мобильных устройствах
@pytest.fixture(scope="function")
def mobile_page(browser_mobile, request):
    device = request.param
    if device in MOBILE_DEVICES:
        context = browser.new_context(**MOBILE_DEVICES[device])
    else:
        raise ValueError(f"Неизвестное устройство: {device}")

    page = context.new_page()
    yield page
    page.close()
