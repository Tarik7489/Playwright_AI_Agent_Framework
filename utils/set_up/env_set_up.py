from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from utils.common_utils.excel_reader import ReadExcel
from utils.common_utils.logger import LoggerReports
from utils.web_runner import WebRunner


class EnvironmentSetUp:
    def __init__(self) -> None:
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None

    def set_up(
        self,
        playwright: Playwright,
        trace: LoggerReports,
        data: dict,
        headless: bool = True,
    ) -> Page:
        browser_name = str(ReadExcel.value(data, "EnvironmentSetUp", "Browser")).lower()
        url = str(ReadExcel.value(data, "EnvironmentSetUp", "Url"))
        runner = WebRunner()
        self.browser = runner.open_browser(playwright, browser_name, headless=headless)
        self.context = self.browser.new_context(viewport={"width": 1920, "height": 1080})
        page = self.context.new_page()
        runner.navigate_to_url(page, url, trace)
        runner.set_local_storage(page, "bypass_global", "true", trace)
        trace.logger.info("Started %s browser and navigated to %s", browser_name, url)
        return page

    def tear_down(self) -> None:
        if self.context is not None:
            self.context.close()
        if self.browser is not None:
            self.browser.close()
