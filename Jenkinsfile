pipeline {
    agent any

    environment {
        DOCKER_USERNAME = "kanishkajain1411"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                bat 'docker build -t %DOCKER_USERNAME%/inventory-backend:latest backend'
            }
        }

        stage('Build Frontend Image') {
            steps {
                bat 'docker build -t %DOCKER_USERNAME%/inventory-frontend:latest frontend'
            }
        }

        stage('Push Backend Image') {
            steps {
                bat 'docker push %DOCKER_USERNAME%/inventory-backend:latest'
            }
        }

        stage('Push Frontend Image') {
            steps {
                bat 'docker push %DOCKER_USERNAME%/inventory-frontend:latest'
            }
        }
    }

    post {
        success {
            echo 'Build Successful!'
        }

        failure {
            echo 'Build Failed!'
        }
    }
}