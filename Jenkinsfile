pipeline {
    agent any

    environment {

        IMAGE_TAG     = "${env.BUILD_NUMBER}" 
        DOCKER_USER   = 'adarsh578' 
        IMAGE_NAME    = "${DOCKER_USER}/banking-app:${IMAGE_TAG}"
    }

    stages {
        
        stage('Source & Checkout') {
            steps {
                echo 'Stage 1 & 2: Checking out code from Version Control...'
                checkout scm
            }
        }

        
        stage('Continuous Integration') {
            steps {
                echo 'Stage 3: Setting up python environment and running tests...'
                
                bat """
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest test_app.py
                """
            }
        }

        
        stage('Build & Push Docker Image') {
            steps {
                echo "Stage 4: Packaging application into Docker image: ${IMAGE_NAME}"
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_REGISTRY_USER', passwordVariable: 'DOCKER_REGISTRY_PASS')]) {
                        
                        bat "echo %DOCKER_REGISTRY_PASS% | docker login -u %DOCKER_REGISTRY_USER% --password-stdin"
                        bat "docker build -t ${IMAGE_NAME} ."
                        bat "docker push ${IMAGE_NAME}"
                    }
                }
            }
        }

        
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Stage 5: Orchestrating deployment to cluster...'
                script {
                    withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_PATH')]) {
                        
                        bat """
                            set KUBECONFIG=%KUBECONFIG_PATH%
                            
                            @echo off
                            powershell -Command "(Get-Content k8s/deployment.tmpl) -replace 'DOCKER_IMAGE_PLACEHOLDER', '${IMAGE_NAME}' | Set-Content k8s/deployment.yaml"
                            
                            kubectl apply -f k8s/deployment.yaml
                            kubectl rollout status deployment/banking-app --timeout=60s
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline Run Completed. Cleaning up workspace...'
            
            bat 'docker logout'
        }
    }
}