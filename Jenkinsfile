pipeline {

    agent any

    environment {
        PYTHON = "C:\\Program Files\\Python314\\python.exe"
        VENV = "venv"
    }

    stages {

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

            post {
                always {
                    echo "Test execution completed"
                }
            }
        }


        stage('Generate Allure Report') {
            steps {
                script {

                    allure([
                        includeProperties: false,
                        jdk: '',
                        results: [
                            [
                                path: 'allure-results'
                            ]
                        ]
                    ])

                }
            }
        }

    }


    post {

        always {

            echo "Publishing Allure results..."

            allure([
                includeProperties: false,
                jdk: '',
                results: [
                    [
                        path: 'allure-results'
                    ]
                ]
            ])
        }


        success {
            echo "Build Passed Successfully"
        }


        failure {
            echo "Build Failed. Check Allure Report"
        }

    }

}