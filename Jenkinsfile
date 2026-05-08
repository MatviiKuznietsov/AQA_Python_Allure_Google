pipeline {
    agent any

    tools {
        python 'Python'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/username/my_project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest tests --junitxml=report.xml --html=report.html'
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'report.xml'

                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ])
            }
        }
    }

    post {

        always {
            emailext(
                subject: "Jenkins Build: ${currentBuild.currentResult}",
                body: """
                    Build Status: ${currentBuild.currentResult}

                    Project: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}

                    Check console output at:
                    ${env.BUILD_URL}
                """,
                to: 'InsertYour@Mail.Here'
            )
        }
    }
}