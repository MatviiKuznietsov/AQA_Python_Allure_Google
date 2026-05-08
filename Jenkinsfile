pipeline {
    agent any

    tools {
        // Предполагаем, что в Jenkins настроен Allure Commandline с именем 'allure'
        // Если имя другое, его нужно будет поправить в настройках Jenkins или здесь
        allure 'allure'
    }

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
                    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Установка зависимостей...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\python -m pip install --upgrade pip
                    venv\\Scripts\\python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запуск автотестов...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\python -m pytest --alluredir=allure-results --junitxml=results.xml -v || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            echo '📋 Сбор результатов...'

            junit testResults: 'results.xml', allowEmptyResults: true

            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']], commandline: 'allure'

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