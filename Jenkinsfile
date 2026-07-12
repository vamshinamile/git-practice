pipeline {

    agent any

    environment {
        PYTHON = "C:\\Program Files\\Python314\\python.exe"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat """
                "%PYTHON%" --version
                "%PYTHON%" -m pip --version
                """
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat """
                if exist venv rmdir /s /q venv
                "%PYTHON%" -m venv venv
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                call venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat """
                if not exist reports mkdir reports
                if not exist allure-results mkdir allure-results

                call venv\\Scripts\\activate.bat

                pytest tests ^
                -v ^
                --junitxml=reports/results.xml ^
                --alluredir=allure-results
                """
            }
        }

        stage('Publish JUnit Report') {
            steps {
                junit 'reports/results.xml'
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure(
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                )
            }
        }
    }

post {
    always {
        script {

            def action = currentBuild.rawBuild.getAction(hudson.tasks.junit.TestResultAction)

            int total = action?.totalCount ?: 0
            int failed = action?.failCount ?: 0
            int skipped = action?.skipCount ?: 0
            int passed = total - failed - skipped

            emailext(
                to: 'vamshinamile18@gmail.com',
                subject: "Automation Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                mimeType: 'text/html',
                body: """
<html>
<head>
<style>
table{
    border-collapse:collapse;
    font-family:Arial;
}
th,td{
    border:1px solid black;
    padding:8px;
}
th{
    background:#4CAF50;
    color:white;
}
</style>
</head>

<body>

<h2>Automation Execution Report</h2>

<table>

<tr>
<th>Item</th>
<th>Value</th>
</tr>

<tr>
<td>Job Name</td>
<td>${env.JOB_NAME}</td>
</tr>

<tr>
<td>Build Number</td>
<td>${env.BUILD_NUMBER}</td>
</tr>

<tr>
<td>Status</td>
<td>${currentBuild.currentResult}</td>
</tr>

<tr>
<td>Total Tests</td>
<td>${total}</td>
</tr>

<tr>
<td>Passed</td>
<td style="color:green;"><b>${passed}</b></td>
</tr>

<tr>
<td>Failed</td>
<td style="color:red;"><b>${failed}</b></td>
</tr>

<tr>
<td>Skipped</td>
<td>${skipped}</td>
</tr>

</table>

<br>

<b>Build URL</b><br>
<a href="${env.BUILD_URL}">
${env.BUILD_URL}
</a>

<br><br>

<b>Allure Report</b><br>
<a href="${env.BUILD_URL}allure">
${env.BUILD_URL}allure
</a>

<br><br>

Regards,<br>
Jenkins

</body>
</html>
"""
            )
        }
    }
}


}