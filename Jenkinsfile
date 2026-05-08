pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *') // Poll SCM every 5 minutes
    }

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
            
            script {
                try {
                    junit testResults: 'results.xml', allowEmptyResults: true
                } catch (Exception e) {
                    echo "JUnit archiving failed: ${e.message}"
                }
                
                try {
                    allure includeProperties: false, jdk: '', results: [[path: 'allure-results']], commandline: 'Allure'
                } catch (Exception e) {
                    echo "Allure report generation failed: ${e.message}"
                }

                try {
                    archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'report.html',
                        reportName: 'Test HTML Report'
                    ])
                } catch (Exception e) {
                    echo "HTML Report publishing failed: ${e.message}"
                }
            }
        }

        fixed { echo '✅ Build Fixed' }
        regression { echo '❌ Regression detected' }

        always {
            echo '📧 Sending email notification...'
            emailext (
                subject: "Jenkins Build ${currentBuild.fullDisplayName} — ${currentBuild.currentResult}",
                body: """
                    <h2>Result: ${currentBuild.currentResult}</h2>
                    <p>Project: ${JOB_NAME}</p>
                    <p>Build: ${BUILD_NUMBER}</p>
                    <p>Check the details here: <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p>Allure Report: <a href="${BUILD_URL}allure/">${BUILD_URL}allure/</a></p>
                """,
                to: 'matveimtvcool@gmail.com',
                attachLog: true,
                mimeType: 'text/html',
                recipientProviders: [culprits(), developers(), requestor(), upstreamDevelopers()]
            )
        }

        success { echo '✅ Success!' }
        failure { echo '❌ Build Error' }
    }
}