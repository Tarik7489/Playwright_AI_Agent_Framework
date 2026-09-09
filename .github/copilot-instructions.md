# Repository instructions for Copilot review

## Project

This is a Python Playwright UI automation framework using a company-style POM structure.

## Required boundaries

- Keep selectors and browser actions in `pages/`.
- Keep reusable business flows in `test_pages/`.
- Keep test intent and data selection in `test_scenarios/`.
- Keep browser lifecycle and shared actions in `utils/`.
- Read environment data from `test_data/<ENV>_Test_Data.xlsx` through `ReadExcel`.
- Preserve the fixture contract: `page, trace, data, environ = test_env_set_up`.
- Use Playwright auto-waiting and web-first assertions. Do not add fixed sleeps.
- Do not commit passwords, tokens, cookies, or other secrets to Excel or source files.

## Review priorities

1. Correctness and test isolation.
2. Reliable Playwright locators and waits.
3. Preservation of the POM and Excel-data conventions.
4. Useful failure diagnostics and maintainable code.
5. Focused tests with no unrelated refactoring.
