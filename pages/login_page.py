from playwright.sync_api import Page

from utils.web_runner import WebRunner


class Login:
    """Login page actions using the company page-object method convention."""

    EMAIL_INPUT = "#userEmail"
    PASSWORD_INPUT = "#userPassword"
    LOGIN_BUTTON = "#login"
    SIGN_OUT_BUTTON = "button:has-text('Sign Out')"

    def email_input(self, page: Page, email: str, trace=None, report=None) -> None:
        function_name = self.email_input.__name__
        email_locator = WebRunner().web_locator(page, self.EMAIL_INPUT, "css", function_name, trace, report)
        WebRunner().input_clear(page, email_locator, email, function_name, trace, report)

    def password_input(self, page: Page, password: str, trace=None, report=None) -> None:
        function_name = self.password_input.__name__
        password_locator = WebRunner().web_locator(page, self.PASSWORD_INPUT, "css", function_name, trace, report)
        WebRunner().input_clear(page, password_locator, password, function_name, trace, report)

    def sign_in(self, page: Page, trace=None, report=None) -> None:
        function_name = self.sign_in.__name__
        sign_in_locator = WebRunner().web_locator(page, self.LOGIN_BUTTON, "css", function_name, trace, report)
        WebRunner().click(page, sign_in_locator, function_name, trace, report)
        page.wait_for_load_state("domcontentloaded")

    def sign_out(self, page: Page, trace=None, report=None) -> None:
        function_name = self.sign_out.__name__
        sign_out_locator = WebRunner().explicit_wait_element_clickable(
            page, self.SIGN_OUT_BUTTON, "css", function_name, trace, report
        )
        WebRunner().click(page, sign_out_locator, function_name, trace, report)
        WebRunner().explicit_wait_presence_of_element(page, self.EMAIL_INPUT, "css", function_name, trace, report)
