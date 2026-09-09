# Playwright Python POM Framework

A Playwright Python framework modeled on the company-style POM structure:

1. Read environment and login data from `test_data/AWS_Test_Data.xlsx`.
2. Start the configured Playwright browser.
3. Log in and sign out through page and business-flow layers.

## Project layout

```text
pages/                 Page objects, selectors, and page-specific behavior
test_pages/            Reusable business flows
test_scenarios/        Test cases only
test_data/             Environment Excel workbooks
utils/                 Shared WebRunner browser actions
utils/set_up/          Environment/browser setup
utils/common_utils/    Excel reader and logging helpers
conftest.py            Shared pytest fixtures
```

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Run

```powershell
python -m pytest --env AWS
```

Run headed for local debugging:

```powershell
python -m pytest --env AWS --headed
```

The HTML report is written to `reports/report.html`.

## GitHub automation

The repository includes two workflows:

- `.github/workflows/branch-pr.yml`: on every non-`main` branch push, installs the
  framework, runs the Excel-driven tests, creates or updates a PR to `main`, adds
	`automation` and `copilot-review` labels, and requests a Copilot review.
- `.github/workflows/ci.yml`: validates pushes to `main` and uploads the HTML
	report and failure artifacts.

One-time repository setup:

1. Push this project to GitHub and enable **Allow auto-merge** in repository settings.
2. Protect `main` and require the `Playwright tests` status check plus at least one
	approving review before merging.
3. Enable Copilot code review or coding agent for the repository and allow it to
	participate in pull requests.
4. Add `AWS_Test_Data.xlsx` only if it contains non-sensitive test data. Move real
	passwords and tokens to GitHub Actions secrets before publishing the repository.

After setup, use:

```powershell
git checkout -b feature/my-change
git add .
git commit -m "Add my change"
git push -u origin feature/my-change
```

The branch workflow then creates the PR automatically. Auto-merge waits for the
required checks and branch-protection approval; it does not bypass review.

## Jenkins CI/CD

The root `Jenkinsfile` provides the same flow for Jenkins:

```text
checkout branch -> install Python/Playwright -> run tests -> create/update PR -> squash-merge
```

Configure a Jenkins Pipeline or Multibranch Pipeline with a Linux agent that has
Python 3 and Git. Add a Jenkins **Secret text** credential with ID
`github-token`; its value must be a GitHub token with permission to create and
merge pull requests. The Jenkins job also needs the repository checkout
credentials configured.

For a Multibranch Pipeline, configure GitHub Branch Source webhooks and point it
at this repository. Every branch push will run the `Jenkinsfile`. The `main`
branch runs tests and archives reports; non-`main` branches also create/update a
PR and squash-merge it after tests pass.

## Framework conventions

- Keep selectors and page-specific actions in `pages/`.
- Keep reusable business flows in `test_pages/`.
- Keep test intent only in `test_scenarios/`.
- Use `utils/web_runner.py` for common browser actions.
- Prefer Playwright auto-waiting and web-first assertions; do not add fixed sleeps.
- Failed tests automatically capture a screenshot in `artifacts/screenshots/`.

The session fixture exposes the company-style tuple:

```python
page, trace, data, environ = test_env_set_up
```

To add another environment, add `<ENV>_Test_Data.xlsx` under `test_data/` with
`EnvironmentSetUp` (`Browser`, `Url`) and `Login` (`Email`, `Password`) sheets,
then run with `--env <ENV>`.
