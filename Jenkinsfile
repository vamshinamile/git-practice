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

        emailext(
            subject: "Regression Build #${BUILD_NUMBER} ${BUILD_STATUS}",

            body: """
<html>
<body>

<h2>Regression Execution Completed</h2>

<p><b>Build Number:</b> ${BUILD_NUMBER}</p>

<p><b>Status:</b> ${BUILD_STATUS}</p>

<p>
<b>Jenkins Build:</b>
<a href="${BUILD_URL}">
Open Build
</a>
</p>

<p>
<b>Allure Report:</b>
<a href="${BUILD_URL}allure">
Open Allure Report
</a>
</p>

<br>

Regards,<br>
Jenkins Automation Team

</body>
</html>
""",

            mimeType: 'text/html',

            to: "your-developer-email@gmail.com"
        )

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