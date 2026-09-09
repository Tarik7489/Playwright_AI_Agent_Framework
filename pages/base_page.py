from playwright.sync_api import Page

from utils.web_runner import WebRunner


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.runner = WebRunner(page)

    def open(self) -> None:
        self.runner.navigate_to_url(self.base_url)
