pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\hello\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
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
                bat """
                "${PYTHON}" --version
                "${PYTHON}" -m pip --version
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                "${PYTHON}" -m pip install --upgrade pip
                "${PYTHON}" -m pip install -r requirements.txt
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat """
                "${PYTHON}" -m pytest -v --alluredir=allure-results
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
            echo 'Pipeline execution completed.'
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }

        success {
            echo 'Build Successful.'
        }

        failure {
            echo 'Build Failed.'
        }
    }
}