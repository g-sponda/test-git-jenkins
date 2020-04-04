pipeline {
    agent {
        docker {
            image 'python:3.7'
            args '--user 0:0'
        }
    }

    environment 
    {
        ECR_URL = '476023098245.dkr.ecr.us-east-1.amazonaws.com'
        ECR_CRED = 'ecr:us-east-1:ecr_credentials'
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh 'apt update && apt install docker'
                sh 'pip install awscli'
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
                    imageName = '${appName}:${tag}'

                    def customImage = docker.build('${imageName}')
                    docker.withRegistry(ECR_URL, ECR_CRED)
                    {
                        docker.image(imageName).push()
                    }
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
                    docker.withRegistry(ECR_URL, ECR_CRED)
                    {
                        docker.image('${appName}:latest').push()
                    }

                    sh 'kubectl apply -f kubernetes/app.yaml'
                    sh 'kubectl set image deployment aws_dms_task_status_reporter aws_dms_task_status_reporter=${imageName} --record'
                    sh 'kubectl rollout status deployment/aws_dms_task_status_reporter'
                }
            }
        }
    }
}