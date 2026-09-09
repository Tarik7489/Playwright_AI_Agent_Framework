from test_pages.login_flow import LoginMistTests


def test_user_can_login_and_sign_out(test_env_set_up) -> None:
    driver, trace, data, environ = test_env_set_up
    email = data["Login"].get("Email")[0]
    password = data["Login"].get("Password")[0]
    LoginMistTests().login_and_sign_out(email, password, test_env_set_up)
