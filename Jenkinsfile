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

        junit 'reports/results.xml'

        emailext(
            to: 'vamshinamile18@gmail.com',
            subject: "Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
            mimeType: 'text/html',
            body: """
<h2>Automation Build</h2>

<b>Job:</b> ${env.JOB_NAME}<br>
<b>Build:</b> ${env.BUILD_NUMBER}<br>
<b>Status:</b> ${currentBuild.currentResult}<br><br>

<b>Build URL:</b><br>
<a href="${env.BUILD_URL}">
${env.BUILD_URL}
</a><br><br>

<b>Allure Report:</b><br>
<a href="${env.BUILD_URL}allure">
${env.BUILD_URL}allure
</a>
"""
        )
    }
}
}