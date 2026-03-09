pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/JAndre0119/finance-tracker-Ledgerly-'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ledgerly:latest .'
            }
        }

        stage('Load Image into Minikube') {
            steps {
                sh 'minikube image load ledgerly:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl rollout status deployment/ledgerly-deployment'
            }
        }
    }
}