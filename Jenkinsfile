pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "kanishkajain1411"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }


        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }


        stage('Build Backend Image') {
            steps {
                sh '''
                docker build -t $DOCKERHUB_USERNAME/inventory-backend:latest ./backend
                '''
            }
        }


        stage('Build Frontend Image') {
            steps {
                sh '''
                docker build -t $DOCKERHUB_USERNAME/inventory-frontend:latest ./frontend
                '''
            }
        }


        stage('Push Backend Image') {
            steps {
                sh '''
                docker push $DOCKERHUB_USERNAME/inventory-backend:latest
                '''
            }
        }


        stage('Push Frontend Image') {
            steps {
                sh '''
                docker push $DOCKERHUB_USERNAME/inventory-frontend:latest
                '''
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