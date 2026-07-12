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

                def result = currentBuild.rawBuild.getAction(hudson.tasks.junit.TestResultAction.class)

                int total = 0
                int failed = 0
                int skipped = 0
                int passed = 0

                if(result != null){
                    total = result.totalCount
                    failed = result.failCount
                    skipped = result.skipCount
                    passed = total - failed - skipped
                }

                emailext(

                    to: 'vamshinamile18@gmail.com',

                    subject: "Automation Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",

                    mimeType: 'text/html',

                    body: """
                    <html>

                    <body>

                    <h2>Automation Execution Report</h2>

                    <table border="1" cellpadding="8" cellspacing="0">

                    <tr>
                    <td><b>Job Name</b></td>
                    <td>${env.JOB_NAME}</td>
                    </tr>

                    <tr>
                    <td><b>Build Number</b></td>
                    <td>${env.BUILD_NUMBER}</td>
                    </tr>

                    <tr>
                    <td><b>Status</b></td>
                    <td>${currentBuild.currentResult}</td>
                    </tr>

                    <tr>
                    <td><b>Total Tests</b></td>
                    <td>${total}</td>
                    </tr>

                    <tr>
                    <td><b>Passed</b></td>
                    <td>${passed}</td>
                    </tr>

                    <tr>
                    <td><b>Failed</b></td>
                    <td>${failed}</td>
                    </tr>

                    <tr>
                    <td><b>Skipped</b></td>
                    <td>${skipped}</td>
                    </tr>

                    </table>

                    <br>

                    <b>Build URL:</b><br>

                    <a href="${env.BUILD_URL}">
                    ${env.BUILD_URL}
                    </a>

                    <br><br>

                    <b>Allure Report:</b><br>

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