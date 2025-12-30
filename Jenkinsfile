pipeline {
    agent any
    
    environment {
        REPO_URL = 'https://github.com/Asad-Khurshid1585/SSD-Final.git'
        DEPLOYMENT_DIR = 'C:\\SSD-App-Deployment'
        PYTHON_VERSION = '3.10'
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
                    bat '''
                        python -m venv venv
                        call venv\\Scripts\\activate.bat
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        echo Dependencies installed successfully
                    '''
                }
            }
        }
        
        stage('3. Run Unit Tests') {
            steps {
                script {
                    echo '====== Running Unit Tests ======'
                    bat '''
                        call venv\\Scripts\\activate.bat
                        pytest test_app.py -v --tb=short
                        echo Unit tests completed
                    '''
                }
            }
        }
        
        stage('4. Build Application') {
            steps {
                script {
                    echo '====== Building Application ======'
                    bat '''
                        call venv\\Scripts\\activate.bat
                        echo Application structure verified
                        dir /s
                        echo Build artifacts prepared
                    '''
                }
            }
        }
        
        stage('5. Deploy Application (Simulation)') {
            steps {
                script {
                    echo '====== Deploying Application ======'
                    bat '''
                        REM Create deployment directory
                        if not exist "%DEPLOYMENT_DIR%" mkdir "%DEPLOYMENT_DIR%"
                        
                        REM Copy application files
                        xcopy /E /Y /I . "%DEPLOYMENT_DIR%"
                        
                        REM Create deployment manifest
                        (
                            echo Deployment Date: %date% %time%
                            echo Deployment Directory: %DEPLOYMENT_DIR%
                            echo Git Commit: 
                            for /f "tokens=*" %%a in ('git rev-parse HEAD') do echo %%a
                            echo Branch: 
                            for /f "tokens=*" %%a in ('git rev-parse --abbrev-ref HEAD') do echo %%a
                        ) > "%DEPLOYMENT_DIR%\\DEPLOYMENT_INFO.txt"
                        
                        echo Application deployed to: %DEPLOYMENT_DIR%
                        echo Deployment manifest created
                        dir "%DEPLOYMENT_DIR%"
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
