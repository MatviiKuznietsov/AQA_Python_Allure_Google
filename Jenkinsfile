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
                    "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" -m venv venv
                    venv\\Scripts\\activate.bat
                    venv\\Scripts\\pip install --upgrade pip
                    venv\\Scripts\\pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запуск автотестов...'
                bat '''
                    venv\\Scripts\\activate.bat
                    venv\\Scripts\\pytest --junitxml=results.xml -v --html=report.html --self-contained-html || exit /b 0
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'results.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

            emailext (
                subject: "Jenkins Build ${currentBuild.fullDisplayName} — ${currentBuild.currentResult}",
                body: '''
                    <h2>Результат: ${BUILD_STATUS}</h2>
                    <p>Проект: ${JOB_NAME}</p>
                    <p>Build: ${BUILD_NUMBER}</p>
                    <p>Ссылка: <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                ''',
                to: 'InsertYour@Mail.Here',
                attachLog: true,
                mimeType: 'text/html'
            )
        }

        success { echo '✅ Успешно!' }
        failure { echo '❌ Ошибка в сборке.' }
    }
}