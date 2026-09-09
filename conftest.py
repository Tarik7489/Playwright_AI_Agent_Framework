from pathlib import Path

import pytest
from playwright.sync_api import Page, sync_playwright

from utils.common_utils.excel_reader import ReadExcel
from utils.common_utils.logger import LoggerReports
from utils.set_up.env_set_up import EnvironmentSetUp
from utils.web_runner import WebRunner


SCREENSHOT_DIR = Path(__file__).parent / "artifacts" / "screenshots"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--env", action="store", default="AWS", help="Environment workbook prefix")


@pytest.fixture(scope="session")
def test_env_set_up(request: pytest.FixtureRequest):
    environment = request.config.getoption("--env")
    data = ReadExcel().excel_reader(environment)
    trace = LoggerReports()
    environment_setup = EnvironmentSetUp()

    with sync_playwright() as playwright:
        page = environment_setup.set_up(
            playwright,
            trace,
            data,
            headless=not request.config.getoption("--headed"),
        )
        yield page, trace, data, environment
        environment_setup.tear_down()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("test_env_set_up", (None,))[0]
    if page is None:
        return

    screenshot_name = item.nodeid.replace("/", "_").replace("\\", "_").replace("::", "_")
    WebRunner(page).screenshot(SCREENSHOT_DIR / f"{screenshot_name}.png")
