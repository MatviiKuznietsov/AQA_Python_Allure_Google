pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Получение кода из репозитория...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Установка зависимостей...'
                bat '''
                    python -m venv venv
                    venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запуск автотестов...'
                bat '''
                    venv\\Scripts\\activate.bat
                    pytest --junitxml=results.xml -v --html=report.html --self-contained-html || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            // Публикация результатов тестов
            junit testResults: 'results.xml', allowEmptyResults: true

            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

            // Отправка email
            emailext (
                subject: "Jenkins Build ${currentBuild.fullDisplayName} — ${currentBuild.currentResult}",
                body: '''
                    <h2>Результат сборки: ${BUILD_STATUS}</h2>
                    <p>Проект: ${JOB_NAME}</p>
                    <p>Build №: ${BUILD_NUMBER}</p>
                    <p>Дата: ${BUILD_TIMESTAMP}</p>
                    <p>Ссылка: <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                ''',
                to: 'InsertYour@Mail.Here',
                from: 'jenkins@your-server.com',
                attachLog: true,
                attachmentsPattern: '**/*.html',
                mimeType: 'text/html'
            )
        }

        success {
            echo '✅ Тесты прошли успешно!'
        }
        failure {
            echo '❌ Сборка завершилась с ошибкой.'
        }
    }
}