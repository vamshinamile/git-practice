pipeline {

    agent any

    options {
        timestamps()
    }

    environment {
        PYTHON = "C:\\Program Files\\Python314\\python.exe"
        VENV = "venv"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat """
                "${PYTHON}" --version
                "${PYTHON}" -m pip --version
                """
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat """
                if exist ${VENV} rmdir /s /q ${VENV}
                "${PYTHON}" -m venv ${VENV}
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                call ${VENV}\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat """
                call ${VENV}\\Scripts\\activate.bat
                pytest -v --alluredir=allure-results
                """
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

            emailext(
                subject: "Automation Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                mimeType: 'text/html',
                body: """
                <html>
                <body>

                <h2>Automation Execution Report</h2>

                <table border="1" cellpadding="8">
                    <tr>
                        <th>Job Name</th>
                        <td>${env.JOB_NAME}</td>
                    </tr>
                    <tr>
                        <th>Build Number</th>
                        <td>${env.BUILD_NUMBER}</td>
                    </tr>
                    <tr>
                        <th>Status</th>
                        <td>${currentBuild.currentResult}</td>
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
                <b>Jenkins Automation Team</b>

                </body>
                </html>
                """,
                to: "vamshinamile18@gmail.com"
            )
        }

        success {
            echo "Automation execution completed successfully."
        }

        failure {
            echo "Automation execution failed."
        }

        cleanup {
            echo "Pipeline execution completed."
        }
    }
}