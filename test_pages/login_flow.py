from pages.login_page import Login


class LoginMistTests:
    """Reusable business flows, kept outside test_scenarios."""

    def login_mist(self, email: str, password: str, test_env_set_up) -> None:
        page, trace, data, environ = test_env_set_up
        trace.logger.info("Logging in with email - %s", email)
        Login().email_input(page, email, trace, None)
        Login().password_input(page, password, trace, None)
        Login().sign_in(page, trace, None)

    def login_and_sign_out(self, email: str, password: str, test_env_set_up) -> None:
        page, trace, data, environ = test_env_set_up
        self.login_mist(email, password, test_env_set_up)
        Login().sign_out(page, trace, None)
