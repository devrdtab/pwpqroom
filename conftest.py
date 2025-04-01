import pytest
import allure
import os
import asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from utils.date_utils import get_current_date
from utils.mobile_devices import MOBILE_DEVICES

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "qroom"))
SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "artifacts", "screenshots")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


# Создаёт экземпляр браузера с помощью Playwright (в данном случае только для Chromium).
# Предоставляет этот браузер тестам, которые от него зависят.
# Закрывает браузер после завершения теста.
# @pytest.fixture(scope="function", params=["chromium", "firefox", "webkit"])
@pytest.fixture(scope="function", params=["chromium"])
def browser(request):
    with sync_playwright() as playwright:
        browser = getattr(playwright, request.param).launch(headless=True)
        yield browser
        browser.close()


# Создаёт новую страницу (вкладку) в браузере для каждого теста.
# Предоставляет эту страницу тестам, которые от неё зависят.
# Закрывает страницу после завершения теста.
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()


# Фикстура асинхронного режима и эмуляции мобильных устройств
@pytest.fixture(scope="function")
async def mobile_page(request):
    device = request.param
    browser_type = MOBILE_DEVICES[device]["default_browser_type"] if device in MOBILE_DEVICES else "chromium"
    async with async_playwright() as playwright:
        print(f"Запускаем {browser_type} для устройства {device} с headless=False")
        browser = await getattr(playwright, browser_type).launch(headless=True)
        if device in MOBILE_DEVICES:
            context = await browser.new_context(**MOBILE_DEVICES[device])
        else:
            raise ValueError(f"Неизвестное устройство: {device}")
        page = await context.new_page()
        print(f"Браузер открыт, контекст создан для {device}")
        await page.wait_for_timeout(2000)
        yield page
        print(f"Закрываем страницу и браузер для {device}")
        await page.close()
        await context.close()
        await browser.close()


# Определяет имя устройства (например, "iPhone 15 Pro Max") на основе viewport_size страницы и используется в тесте, например, для логирования в Allure:
@pytest.fixture(scope="function")
async def device(mobile_page):
    """Фикстура для определения устройства на основе viewport_size."""
    device = [d for d in MOBILE_DEVICES if MOBILE_DEVICES[d]["viewport"] == mobile_page.viewport_size][0]
    print(f"Размер окна: {mobile_page.viewport_size}, устройство: {device}")
    return device


# Хук pytest_runtest_makereport, который автоматически создаёт скриншоты при падении теста, без необходимости передавать его в тест.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("mobile_page")
        browser_name = item.callspec.params.get("browser", "unknown") if "browser" in item.callspec.params else "mobile"

        if page:
            test_name = item.name
            timestamp = get_current_date().replace(":", "-")
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{browser_name}_{timestamp}.png")
            try:
                print(f"Попытка сохранить скриншот в: {screenshot_path}")
                if "page" in item.funcargs:  # Синхронный page из sync_playwright
                    print("Используется синхронный API для скриншота")
                    page.screenshot(path=screenshot_path, full_page=True)
                elif "mobile_page" in item.funcargs:  # Асинхронный mobile_page из async_playwright
                    print("Используется асинхронный API для скриншота")
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(page.screenshot(path=screenshot_path, full_page=True))
                print(f"✅ Скриншот сохранен: {screenshot_path}")
                allure.attach.file(screenshot_path, name=f"{test_name}_{browser_name}",
                                   attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"❌ Ошибка при сохранении скриншота: {e}")


# ???? фикстура предоставляет функцию для создания скриншотов по запросу
@pytest.fixture(scope="function")
def screenshot_on_demand(request):
    async def _save_screenshot(page, suffix=""):
        test_name = request.node.name
        timestamp = get_current_date().replace(":", "-")
        filename = f"{test_name}{'_' + suffix if suffix else ''}_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, filename)

        if "page" in request.node.fixturenames:  # Синхронный page из sync_playwright
            print(f"Сохранение скриншота (синхронный API): {screenshot_path}")
            page.screenshot(path=screenshot_path, full_page=True)
        else:  # Асинхронный mobile_page из async_playwright
            print(f"Сохранение скриншота (асинхронный API): {screenshot_path}")
            await page.screenshot(path=screenshot_path, full_page=True)

        print(f"Скриншот сохранен: {screenshot_path}")
        return screenshot_path

    return _save_screenshot


# Фикстура определяет начало работы тестов
@pytest.fixture(scope="session")
def tests_iteration():
    print('\n= = = = = Iteration Started = = = = = ')
    yield
    print('\n= = = = = Iteration Finished = = = = = ')


@pytest.mark.regression
def tests_regression():
    yield
