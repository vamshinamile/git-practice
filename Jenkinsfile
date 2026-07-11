pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Program Files\\Python314\\python.exe'
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                "%PYTHON%" --version
                "%PYTHON%" -m pip --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                if exist venv rmdir /s /q venv
                "%PYTHON%" -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate.bat
                pytest -v --alluredir=allure-results
                '''
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
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            echo 'Pipeline execution completed.'
        }

        success {
            echo 'Build Successful.'
        }

        failure {
            echo 'Build Failed.'
        }
    }
}