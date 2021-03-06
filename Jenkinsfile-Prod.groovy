pipeline {
    environment {
        registry = "wjloh91/jenkins-flask-redis"
        registryCredential = 'wjloh_dockerhub_creds'
        dockerImage = ''
    }
    agent any

    stages {

        stage('Cloning Git') {
            steps {
                git branch: 'master', url: 'https://github.com/Physium/CICDChallenge.git'
            }
        }

        stage('Build Image') {
            steps {
                script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }

        stage('Flask Unit Test') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'python -m unittest tests/app_test.py'
                    }
                }
            }
        }

        stage('Push Image to Dockerhub') {
            steps {
                script {
                    docker.withRegistry( '',registryCredential ){
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Clean up Image') {
            steps {
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }

        stage('Clean Up Test Deployment') {
            steps {
                sh "kubectl config set-context --current --namespace=development"
                sh "cat flask-redis-lb-deploy.yaml | kubectl delete -f -"
            }
        }

        stage('Deploy Image to EKS') {
            steps {
                sh "kubectl config set-context --current --namespace=production"
                sh "cat flask-redis-lb-deploy-template.yaml | sed \"s/{{IMAGE_TAG}}/$BUILD_NUMBER/g\" | kubectl apply -f -"
                sh "sleep 10"
                sh "kubectl get services -o=jsonpath=\"{.items[?(@.metadata.name=='counter-service')].status.loadBalancer.ingress[*].hostname}\""
            }
        }
    }
}