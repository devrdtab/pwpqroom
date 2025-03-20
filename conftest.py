from dis import print_instructions

import pytest
import allure
from playwright.sync_api import sync_playwright
from utils.date_utils import get_current_date


# @pytest.fixture(scope="function", params=["chromium", "firefox", "webkit"])
@pytest.fixture(scope="function", params=["chromium"])
def browser(request):
    """Фикстура для запуска тестов в Chrome, Firefox, WebKit"""
    with sync_playwright() as playwright:
        browser = getattr(playwright, request.param).launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
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

    if report.failed:  # Если тест провален
        page = item.funcargs.get("page")  # Получаем страницу Playwright
        browser_name = item.callspec.params["browser"]  # Определяем браузер

        if page:
            test_name = item.name
            timestamp = get_current_date().replace(":", "-")  # Убираем двоеточия
            screenshot_path = f"screenshots/{test_name}_{browser_name}_{timestamp}.png"

            # Делаем скриншот и сохраняем
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Скриншот сохранен: {screenshot_path}")

            # Прикрепляем скриншот в Allure
            allure.attach.file(screenshot_path, name=f"{test_name}_{browser_name}",
                               attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope='session')
def tests_iteration():
    print('\n= = = = = Iteration Started = = = = = ')
    yield
    print('\n= = = = = Iteration Finished = = = = = ')

@pytest.mark.regression
def tests_regression():
    yield