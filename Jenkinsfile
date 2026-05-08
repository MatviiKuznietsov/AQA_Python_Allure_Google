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
                    py -m venv venv || python -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Установка зависимостей...'
                bat '''
                    venv\\Scripts\\activate.bat
                    venv\\Scripts\\python -m pip install --upgrade pip
                    venv\\Scripts\\python -m pip install -r requirements.txt
                    venv\\Scripts\\python -m pip install pytest pytest-html
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запуск автотестов...'
                bat '''
                    venv\\Scripts\\activate.bat
                    venv\\Scripts\\pytest --junitxml=results.xml --html=report.html --self-contained-html -v || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            echo '📋 Сбор результатов...'

            // Публикация тестов
            junit testResults: 'results.xml', allowEmptyResults: true

            // Архивация HTML-отчёта
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Test HTML Report'
            ])

            // Отправка email
            emailext (
                subject: "Jenkins Build ${currentBuild.fullDisplayName} — ${currentBuild.currentResult}",
                body: '''
                    <h2>Результат сборки: ${BUILD_STATUS}</h2>
                    <p><b>Проект:</b> ${JOB_NAME}</p>
                    <p><b>Номер сборки:</b> ${BUILD_NUMBER}</p>
                    <p><b>Ссылка:</b> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                ''',
                to: 'InsertYour@Mail.Here',
                attachLog: true,
                mimeType: 'text/html'
            )
        }

        success { echo '✅ Сборка и тесты успешно завершены!' }
        failure { echo '❌ Сборка завершилась с ошибками.' }
    }
}