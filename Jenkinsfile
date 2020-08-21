pipeline {
    environment {
        registry = "wjloh91/jenkins-flask-redis"
        registryCredential = 'wjloh_dockerhub_creds'
        dockerImage = ''
    }
    agent any

    stages {
        stage('Cloning git') {
            steps {
                git branch: 'master', url: 'https://github.com/Physium/CICDChallenge.git'
            }
        }

        stage('Build image') {
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

        stage('Deploy image') {
            steps {
                script {
                    docker.withRegistry( '',registryCredential ){
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Cleaning up') {
            steps {
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }


        stage('get pod') {
            steps {
                 sh "cat flask-redis-lb-deploy-template.yaml | sed \"s/{{IMAGE_TAG}}/$BUILD_NUMBER/g\" | kubectl apply -f -"
            }
        }
    }
}