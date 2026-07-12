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
                script {
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        bat """
                        call ${VENV}\\Scripts\\activate.bat
                        pytest -v --alluredir=allure-results
                        """
                    }
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                echo "Skipping Allure Report for now..."
            }
        }
    }

    post {

        always {

            echo "========== POST BLOCK STARTED =========="

            emailext(
                to: 'vamshinamile18@gmail.com',
                subject: "Automation Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
Hello Team,

Automation execution has completed.

Job Name : ${env.JOB_NAME}
Build No : ${env.BUILD_NUMBER}
Status   : ${currentBuild.currentResult}

Build URL:
${env.BUILD_URL}

Regards,
Jenkins Automation
"""
            )

            echo "========== EMAIL STEP COMPLETED =========="
        }

        success {
            echo "Build completed successfully."
        }

        failure {
            echo "Build completed with failures."
        }

        cleanup {
            echo "Pipeline execution finished."
        }
    }
}