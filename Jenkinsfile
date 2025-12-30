pipeline {
    agent any
    
    environment {
        REPO_URL = 'https://github.com/Asad-Khurshid1585/SSD-Final.git'
        DEPLOYMENT_DIR = '/var/www/ssd-app'
        PYTHON_VERSION = '3.10'
    }
    
    options {
        timestamps()
        timeout(time: 1, unit: 'HOURS')
    }
    
    stages {
        stage('1. Clone Repository') {
            steps {
                script {
                    echo '====== Cloning Repository ======'
                    deleteDir()
                    git branch: 'master', url: "${REPO_URL}"
                    echo "Repository cloned successfully from ${REPO_URL}"
                }
            }
        }
        
        stage('2. Install Dependencies') {
            steps {
                script {
                    echo '====== Installing Dependencies ======'
                    sh '''
                        # Show Python version
                        python3 --version
                        
                        # Install pip packages with --break-system-packages to bypass PEP 668
                        python3 -m pip install --upgrade pip setuptools wheel --break-system-packages
                        python3 -m pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 SQLAlchemy==2.0.23 pytest==9.0.2 --break-system-packages
                        
                        # Verify installation
                        python3 -m pip list | grep -E "Flask|SQLAlchemy|pytest"
                        echo "Dependencies installed successfully"
                    '''
                }
            }
        }
        
        stage('3. Run Unit Tests') {
            steps {
                script {
                    echo '====== Running Unit Tests ======'
                    sh '''
                        echo "Running pytest tests..."
                        python3 -m pytest test_app.py -v --tb=short
                        echo "Unit tests completed"
                    '''
                }
            }
        }
        
        stage('4. Build Application') {
            steps {
                script {
                    echo '====== Building Application ======'
                    sh '''
                        echo "Application structure verified"
                        ls -la
                        echo "Build artifacts prepared"
                    '''
                }
            }
        }
        
        stage('5. Deploy Application (Simulation)') {
            steps {
                script {
                    echo '====== Deploying Application ======'
                    sh '''
                        # Create deployment directory
                        mkdir -p ${DEPLOYMENT_DIR}
                        
                        # Copy application files (excluding virtual environment and git)
                        cp -r app.py requirements.txt templates ${DEPLOYMENT_DIR}/ || true
                        cp -r test_app.py ${DEPLOYMENT_DIR}/ || true
                        
                        # Set permissions
                        chmod -R 755 ${DEPLOYMENT_DIR}
                        
                        # Create deployment manifest
                        cat > ${DEPLOYMENT_DIR}/DEPLOYMENT_INFO.txt << EOF
Deployment Date: $(date)
Deployment Directory: ${DEPLOYMENT_DIR}
Git Commit: $(git rev-parse HEAD)
Branch: $(git rev-parse --abbrev-ref HEAD)
Build Number: ${BUILD_NUMBER}
Build URL: ${BUILD_URL}
Python Version: $(python3 --version)
EOF
                        
                        echo "Application deployed to: ${DEPLOYMENT_DIR}"
                        echo "Deployment manifest created"
                        ls -la ${DEPLOYMENT_DIR}
                    '''
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo '====== Pipeline Execution Successful ======'
                echo 'All stages completed successfully!'
                echo 'Application is ready for use at: ${DEPLOYMENT_DIR}'
            }
        }
        failure {
            script {
                echo '====== Pipeline Execution Failed ======'
                echo 'One or more stages failed. Check logs above for details.'
            }
        }
        always {
            script {
                echo '====== Pipeline Summary ======'
                echo "Build Duration: ${currentBuild.durationString}"
                echo "Build Number: ${env.BUILD_NUMBER}"
            }
        }
    }
}
