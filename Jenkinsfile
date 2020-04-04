pipeline {
    agent {
        docker {
            image 'python:3.7'
            args '--user 0:0'
        }
    }
    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python -m unittest tests/test_*.py'
            }
        }
        stage('Build and push Docker image') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    sh 'git rev-parse --short HEAD > commit-id'
                    tag = readFile('commit-id').replace('\n', '').replace('\r', '')
                    appName = 'aws_dms_task_status_reporter'
                    imageName = 'sponda/${appName}:${tag}'

                    def customImage = docker.build('${imageName}')
                    customImage.push() 

                }
            }
        }
        stage('Deploy to kubernetes') {
            when {
                branch 'develop'
            }
            steps {
                input 'You want to deploy?'

                script {

                    sh 'kubectl apply -f kubernetes/app.yaml'
                    sh 'kubectl set image deployment aws_dms_task_status_reporter aws_dms_task_status_reporter=${imageName} --record'
                    sh 'kubectl rollout status deployment/aws_dms_task_status_reporter'

                    customImage.push('latest')
                }
            }
        }
    }
}