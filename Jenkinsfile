pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Получение кода из репозитория...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Настройка Python окружения...'
                bat '''
                    "C:\\Users\\Matvii\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Установка зависимостей...'
                bat '''
                    venv\\Scripts\\activate.bat
                    venv\\Scripts\\python -m pip install --upgrade pip
                    venv\\Scripts\\python -m pip install -r requirements.txt pytest pytest-html
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запуск автотестов...'
                bat '''
                    venv\\Scripts\\activate.bat
                    venv\\Scripts\\python -m pytest --junitxml=results.xml --html=report.html --self-contained-html -v || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            echo '📋 Сбор результатов...'

            junit testResults: 'results.xml', allowEmptyResults: true

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
                    <h2>Результат: ${BUILD_STATUS}</h2>
                    <p>Проект: ${JOB_NAME}</p>
                    <p>Build: ${BUILD_NUMBER}</p>
                    <p><a href="${BUILD_URL}">Открыть сборку в Jenkins</a></p>
                ''',
                to: 'InsertYour@Mail.Here',
                attachLog: true,
                mimeType: 'text/html'
            )
        }

        success { echo '✅ Успешно!' }
        failure { echo '❌ Ошибка сборки' }
    }
}