import datetime
import json
import random
import string
import zipfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, BrowserContext, FrameLocator, Locator, Page, Playwright, expect


class WebRunner:
    """Common Playwright browser actions using the company WebRunner style."""

    DEFAULT_TIMEOUT_MS = 30_000

    def open_browser(self, playwright: Playwright, browser: str = "chromium", headless: bool = True) -> Browser:
        browser_type = {
            "chrome": playwright.chromium,
            "chromium": playwright.chromium,
            "firefox": playwright.firefox,
            "webkit": playwright.webkit,
        }.get(browser.lower())
        if browser_type is None:
            raise ValueError(f"Unsupported browser: {browser}")
        return browser_type.launch(headless=headless)

    def tear_down(self, browser: Browser | None = None, context: BrowserContext | None = None) -> None:
        if context is not None:
            context.close()
        if browser is not None:
            browser.close()

    def navigate_to_url(self, page: Page, base_url: str, trace=None) -> None:
        page.set_default_timeout(self.DEFAULT_TIMEOUT_MS)
        page.goto(base_url, wait_until="domcontentloaded")
        self._log(trace, f"Navigated to {base_url}")

    def web_locator(self, page: Page, element_value: str, mode: str = "css", function_name: str = "", trace=None, report=None) -> Locator:
        selectors = {
            "css": element_value,
            "xpath": f"xpath={element_value}",
            "id": f"#{element_value}",
            "text": f"text={element_value}",
        }
        if mode.lower() not in selectors:
            raise ValueError(f"Unsupported locator mode: {mode}")
        locator = page.locator(selectors[mode.lower()])
        self._step(report, f"Located element for {function_name or 'action'}")
        return locator

    def web_locators_list(self, page: Page, element_value: str, mode: str = "css", function_name: str = "", trace=None, report=None) -> list[Locator]:
        return self.web_locator(page, element_value, mode, function_name, trace, report).all()

    def explicit_wait_presence_of_element(self, page: Page, element_value: str, mode: str = "css", function_name: str = "", trace=None, report=None) -> Locator:
        locator = self.web_locator(page, element_value, mode, function_name, trace, report)
        expect(locator).to_be_visible()
        return locator

    def explicit_wait_element_clickable(self, page: Page, element_value: str, mode: str = "css", function_name: str = "", trace=None, report=None) -> Locator:
        locator = self.explicit_wait_presence_of_element(page, element_value, mode, function_name, trace, report)
        expect(locator).to_be_enabled()
        return locator

    def is_element_present(self, page: Page, element_value: str, mode: str = "css", timeout: int = 0) -> bool:
        try:
            self.web_locator(page, element_value, mode).wait_for(state="attached", timeout=timeout or 1)
            return True
        except Exception:
            return False

    def click(self, page: Page, locator: Locator, function_name: str = "", trace=None, report=None) -> None:
        locator.click()
        self._log(trace, f"Element clicked: {function_name}")
        self._step(report, f"Element clicked: {function_name}")

    def javascript_click(self, page: Page, locator: Locator, function_name: str = "", trace=None, report=None) -> None:
        locator.evaluate("element => element.click()")
        self._log(trace, f"JavaScript click completed: {function_name}")

    def input_clear(self, page: Page, locator: Locator, input_value: str, function_name: str = "", trace=None, report=None) -> None:
        locator.fill(input_value)
        self._log(trace, f"Input supplied: {function_name}")
        self._step(report, f"Input supplied: {function_name}")

    def input(self, page: Page, locator: Locator, input_value: str, function_name: str = "", trace=None, report=None) -> None:
        locator.type(input_value)

    def clear_value(self, page: Page, locator: Locator, function_name: str = "", trace=None, report=None) -> None:
        locator.clear()

    def press_enter(self, page: Page, locator: Locator, function_name: str = "", trace=None, report=None) -> None:
        locator.press("Enter")

    def press_esc_key(self, page: Page, function_name: str = "", trace=None, report=None) -> None:
        page.keyboard.press("Escape")

    def assert_element_text(self, page: Page, locator: Locator, element_text: str, function_name: str = "", trace=None, report=None) -> None:
        expect(locator).to_have_text(element_text)

    def is_visible(self, page: Page, locator: Locator) -> bool:
        return locator.is_visible()

    def is_enabled(self, page: Page, locator: Locator) -> bool:
        return locator.is_enabled()

    def is_selected(self, page: Page, locator: Locator) -> bool:
        return locator.is_checked()

    def hover_to(self, page: Page, locator: Locator, function_name: str = "", trace=None, report=None) -> None:
        locator.hover()

    def scroll_to_element(self, page: Page, locator: Locator, function_name: str = "", trace=None, report=None) -> None:
        locator.scroll_into_view_if_needed()

    def select_dropdown(self, page: Page, locator: Locator, value: str, mode: str = "value", function_name: str = "", trace=None, report=None) -> None:
        if mode == "visible_text":
            locator.select_option(label=value)
        elif mode == "index":
            locator.select_option(index=int(value))
        else:
            locator.select_option(value=value)

    def find_frame_by_selector(self, page: Page, frame_selector: str) -> FrameLocator:
        return page.frame_locator(frame_selector)

    def close_all_windows_except_current(self, context: BrowserContext, current_page: Page) -> None:
        for page in context.pages:
            if page != current_page:
                page.close()

    def switch_next_window(self, context: BrowserContext) -> Page:
        if len(context.pages) < 2:
            raise RuntimeError("No additional page is available")
        return context.pages[-1]

    def screenshot(self, page: Page, name: str | Path, directory: str | Path = "artifacts/screenshots") -> Path:
        path = Path(directory) / f"{name}.png" if Path(name).suffix == "" else Path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(path), full_page=True)
        return path

    def set_local_storage(self, page: Page, key: str, value: str, trace=None) -> None:
        page.evaluate("([storage_key, storage_value]) => localStorage.setItem(storage_key, storage_value)", [key, value])
        self._log(trace, f"Set localStorage key: {key}")

    def get_local_storage(self, page: Page, key: str) -> Any:
        return page.evaluate("storage_key => localStorage.getItem(storage_key)", key)

    def json_file_reader(self, file_path: str | Path) -> Any:
        with Path(file_path).open(encoding="utf-8") as data_file:
            return json.load(data_file)

    def generate_password(self, length: int, function_name: str = "", trace=None, report=None) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))

    def generate_word(self, prefix: str = "", function_name: str = "", trace=None, report=None) -> str:
        return prefix + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def zip_dir(self, directory: str | Path, zipname: str | Path) -> None:
        root = Path(directory)
        with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as archive:
            for file_path in root.rglob("*"):
                if file_path.is_file():
                    archive.write(file_path, file_path.relative_to(root))

    @staticmethod
    def _log(trace, message: str) -> None:
        if trace is not None:
            trace.logger.info(message)

    @staticmethod
    def _step(report, message: str) -> None:
        if report is not None and hasattr(report, "step"):
            report.step(message)
