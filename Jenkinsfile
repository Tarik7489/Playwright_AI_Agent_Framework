pipeline {
    agent any

    parameters {
        string(name: 'TEST_ENV', defaultValue: 'AWS', description: 'Workbook environment prefix')
        string(name: 'GITHUB_REPOSITORY', defaultValue: 'Tarik7489/Playwright_AI_Agent_Framework', description: 'GitHub owner/repository')
    }

    environment {
        CI = 'true'
    }

    stages {
        stage('Install') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
                sh '.venv/bin/python -m playwright install --with-deps chromium'
            }
        }

        stage('Test') {
            steps {
                sh 'mkdir -p reports artifacts'
                sh '.venv/bin/python -m pytest --env "${TEST_ENV}" --junitxml=reports/junit.xml'
            }
        }

        stage('Create PR and Merge') {
            when {
                not { branch 'main' }
            }
            steps {
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    sh '''.venv/bin/python - <<'PY'
import json
import os
import urllib.error
import urllib.request

repository = os.environ['GITHUB_REPOSITORY']
branch = os.environ.get('BRANCH_NAME', '')
token = os.environ['GITHUB_TOKEN']
api = f'https://api.github.com/repos/{repository}'
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
    'X-GitHub-Api-Version': '2022-11-28',
}


def request(method, path, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    request_obj = urllib.request.Request(f'{api}{path}', data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request_obj) as response:
            return response.status, json.loads(response.read() or b'{}')
    except urllib.error.HTTPError as error:
        detail = error.read().decode()
        raise RuntimeError(f'GitHub API {method} {path} failed ({error.code}): {detail}') from error

if not branch or branch == 'main':
    raise SystemExit('Skipping PR merge for main')

_, open_prs = request('GET', f'/pulls?state=open&head={repository.split("/")[0]}:{branch}&base=main')
if open_prs:
    pull_request = open_prs[0]
else:
    _, pull_request = request('POST', '/pulls', {
        'title': f'Jenkins: {branch}',
        'head': branch,
        'base': 'main',
        'body': 'Created automatically by Jenkins after successful Playwright tests.'
    })

number = pull_request['number']
request('POST', f'/issues/{number}/comments', {
    'body': '<!-- jenkins-playwright -->\\nJenkins Playwright tests passed. Requesting review and automatic squash merge.'
})
status, merge_result = request('PUT', f'/pulls/{number}/merge', {
    'sha': pull_request['head']['sha'],
    'merge_method': 'squash'
})
if not merge_result.get('merged'):
    raise RuntimeError(f'PR #{number} was not merged: {merge_result}')
print(f'PR #{number} merged successfully')
PY'''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**, artifacts/**', allowEmptyArchive: true
        }
    }
}
