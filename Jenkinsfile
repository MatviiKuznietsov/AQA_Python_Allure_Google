pipeline {
    agent any

    tools {
        // Assume Allure Commandline is configured in Jenkins with the name 'Allure'
        // If the name is different, it will need to be adjusted in Jenkins settings or here
        allure 'Allure'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Fetching code from repository...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python environment...'
                bat '''
                    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing dependencies...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\python -m pip install --upgrade pip
                    venv\\Scripts\\python -m pip install -r requirements.txt
                    venv\\Scripts\\python -m playwright install --with-deps
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running auto-tests...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\python -m pytest --alluredir=allure-results --junitxml=results.xml -v || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            echo '📋 Collecting results...'

            junit testResults: 'results.xml', allowEmptyResults: true

            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']], commandline: 'Allure'

            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Test HTML Report'
            ])

            emailext (
                subject: "Jenkins Build ${currentBuild.fullDisplayName} — ${currentBuild.currentResult}",
                body: '''
                    <h2>Result: ${BUILD_STATUS}</h2>
                    <p>Project: ${JOB_NAME}</p>
                    <p>Build: ${BUILD_NUMBER}</p>
                    <p>Status: ${currentBuild.currentResult}</p>
                    <p><a href="${BUILD_URL}">Open build in Jenkins</a></p>
                    <p><a href="${BUILD_URL}allure/">Open Allure Report</a></p>
                ''',
                to: 'matveimtvcool@gmail.com',
                attachLog: true,
                mimeType: 'text/html'
            )
        }

        success { echo '✅ Success!' }
        failure { echo '❌ Build Error' }
    }
}