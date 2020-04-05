pipeline {
    agent {
        docker {
            image 'python:3.7'
            args '--user 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment 
    {
        ECR_URL = "${env.ECR_URL}"
        ECR_CRED = "${env.ECR_CRED}"
        APP_NAME = 'aws_dms_task_status_reporter'
        DEPLOY_NAME = 'aws-dms-task-status-exporter'
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
                    sh 'apt update && apt install docker.io -y && service docker start'
                    sh 'pip install awscli'
                    sh 'git rev-parse --short HEAD > commit-id'
                    tag = readFile('commit-id').replace('\n', '').replace('\r', '')
                    imageName = "${APP_NAME}:${tag}"

                    def customImage = docker.build(imageName)
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
                // input 'You want to deploy?'

                script {
                    sh 'curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl'
                    sh 'chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl'
                    sh "sed 's/IMAGE_TAG/${tag}/g' kubernetes/app.yml > app.yml"

                    withKubeConfig([credentialsId: 'kube_config',]) {
                        sh 'kubectl apply -f app.yml'
                        try {
                            // Verify the status during 5 min
                            sh "kubectl rollout status deployment/${DEPLOY_NAME} --timeout 300s"

                            docker.withRegistry(ECR_URL, ECR_CRED)
                            {
                                docker.image("${APP_NAME}:latest").push()
                            }
                        } catch(e) {
                            // If non return zero do the rollback
                            sh "kubectl rollout undo deployment/${DEPLOY_NAME}"
                        }
                    }
                }
            }
        }
    }
}