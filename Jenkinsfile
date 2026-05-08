pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')  // проверка изменений каждые 5 минут
        // или GitHub webhook для мгновенного запуска
    }

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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запуск автотестов...'
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=results.xml -v --html=report.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            // Публикация результатов тестов
            junit 'results.xml'
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true

            // Отправка email
            emailext (
                subject: "Jenkins Build ${currentBuild.fullDisplayName} — ${currentBuild.currentResult}",
                body: '''
                    <h2>Результаты сборки: ${BUILD_STATUS}</h2>
                    <p>Проект: ${JOB_NAME}</p>
                    <p>Номер сборки: ${BUILD_NUMBER}</p>
                    <p>Время: ${BUILD_TIMESTAMP}</p>
                    <p>Подробнее: <a href="${BUILD_URL}">${BUILD_URL}</a></p>

                    <h3>Последние изменения:</h3>
                    ${CHANGES_SINCE_LAST_SUCCESS}
                ''',
                to: 'InsertYour@Mail.Here',
                from: 'jenkins@yourcompany.com',
                attachLog: true,
                attachmentsPattern: 'report.html',
                mimeType: 'text/html'
            )
        }

        success {
            echo '✅ Тесты прошли успешно!'
        }

        failure {
            echo '❌ Тесты упали. Проверьте логи.'
        }
    }
}