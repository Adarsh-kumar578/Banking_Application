pipeline {
    agent any

    environment {
        
        IMAGE_TAG     = "${GIT_COMMIT.take(7)}"
        DOCKER_USER   = 'adarsh578' // Change to your actual Docker Hub username
        IMAGE_NAME    = "${adarsh578}/banking-app:${IMAGE_TAG}"
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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest test_app.py
                '''
            }
        }

        
        stage('Build & Push Docker Image') {
            steps {
                echo "Stage 4: Packaging application into Docker image: ${IMAGE_NAME}"
                script {
                    
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_REGISTRY_USER', passwordVariable: 'DOCKER_REGISTRY_PASS')]) {
                        sh "echo '${DOCKER_REGISTRY_PASS}' | docker login -u '${DOCKER_REGISTRY_USER}' --password-stdin"
                        
                        
                        sh "docker build -t ${IMAGE_NAME} ."
                        sh "docker push ${IMAGE_NAME}"
                    }
                }
            }
        }

        
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Stage 5: Orchestrating deployment to cluster...'
                script {
                    
                    withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_PATH')]) {
                        sh """
                            export KUBECONFIG=${KUBECONFIG_PATH}
                            
                            
                            sed "s|DOCKER_IMAGE_PLACEHOLDER|${IMAGE_NAME}|g" k8s/deployment.tmpl > k8s/deployment.yaml
                            
                            
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
            echo 'Pipeline Run Completed. Cleaning up workspace workspace...'
            sh 'docker logout || true'
        }
    }
}