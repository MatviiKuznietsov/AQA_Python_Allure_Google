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
                echo '� Настройка Python окружения...'
                bat '''
                    python -m venv venv
                    venv\\Scripts\\activate.bat
                    python --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Установка зависимостей...'
                bat '''
                    venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install pytest pytest-html allure-pytest playwright
                    playwright install
                    pip install -r requirements.txt || echo "requirements.txt not found, continuing..."
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Запуск автотестов...'
                bat '''
                    venv\\Scripts\\activate.bat
                    pytest --junitxml=results.xml --alluredir=allure-results -v --html=report.html --self-contained-html
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo '📊 Генерация Allure отчета...'
                script {
                    try {
                        bat '''
                            allure generate allure-results --clean -o allure-report
                        '''
                    } catch (Exception e) {
                        echo "Allure отчет не сгенерирован: ${e.getMessage()}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo '📋 Сбор артефактов...'
            
            // JUnit результаты
            junit testResults: 'results.xml', allowEmptyResults: true
            
            // HTML отчет
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Test HTML Report'
            ])
            
            // Allure отчет
            script {
                try {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                } catch (Exception e) {
                    echo "Allure plugin not available or error: ${e.getMessage()}"
                    // Fallback: архивируем allure-results
                    archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
                }
            }
            
            // Архивируем все артефакты
            archiveArtifacts artifacts: 'report.html,results.xml,allure-results/**/*,allure-report/**/*', allowEmptyArchive: true

            // Email уведомление
            emailext (
                subject: "Jenkins Build ${currentBuild.fullDisplayName} — ${currentBuild.currentResult}",
                body: """
                    <h2>🔍 Результат сборки: ${BUILD_STATUS}</h2>
                    <p><strong>Проект:</strong> ${JOB_NAME}</p>
                    <p><strong>Build:</strong> ${BUILD_NUMBER}</p>
                    <p><strong>Ссылка на сборку:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <p><strong>Ссылка на Allure отчет:</strong> <a href="${BUILD_URL}allure">${BUILD_URL}allure</a></p>
                    <p><strong>Ссылка на HTML отчет:</strong> <a href="${BUILD_URL}HTML_20Report/">${BUILD_URL}HTML_20Report/</a></p>
                """,
                to: 'InsertYour@Mail.Here',
                attachLog: true,
                mimeType: 'text/html'
            )
        }

        success { 
            echo '✅ Тесты успешно выполнены!'
            echo '📊 Allure отчет доступен по ссылке: ${BUILD_URL}allure'
        }
        
        failure { 
            echo '❌ Ошибка в выполнении тестов.'
            echo '📋 Проверьте логи для детальной информации.'
        }
        
        unstable { 
            echo '⚠️ Некоторые тесты не прошли.'
            echo '📊 Проверьте Allure отчет для деталей.'
        }
    }
}