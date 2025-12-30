# Jenkins Pipeline Configuration for SSD-Final Flask Application

## Pipeline Overview
This Jenkins pipeline automates the build, test, and deployment process for the SSD-Final Flask application.

## Pipeline Stages

### Stage 1: Clone Repository
- **Description**: Clones the GitHub repository containing the Flask application
- **Actions**:
  - Cleans workspace
  - Clones `master` branch from the repository
  - Verifies successful clone

### Stage 2: Install Dependencies
- **Description**: Sets up Python virtual environment and installs required packages
- **Actions**:
  - Creates Python virtual environment
  - Upgrades pip package manager
  - Installs packages from `requirements.txt`
  - Packages: Flask, Flask-SQLAlchemy, SQLAlchemy, pytest

### Stage 3: Run Unit Tests
- **Description**: Executes comprehensive unit tests using pytest
- **Actions**:
  - Activates virtual environment
  - Runs pytest with verbose output
  - Tests include:
    - User model creation and validation
    - CRUD operations (Create, Read, Update, Delete)
    - Route functionality
    - Data validation constraints
  - Test file: `test_app.py`
  - Expected result: 12 tests passed

### Stage 4: Build Application
- **Description**: Prepares the application for deployment
- **Actions**:
  - Verifies application structure
  - Lists build artifacts
  - Ensures all necessary files are present

### Stage 5: Deploy Application (Simulation)
- **Description**: Simulates deployment to production environment
- **Actions**:
  - Creates deployment directory
  - Copies all application files
  - Sets proper file permissions
  - Creates deployment manifest with metadata
  - Deployment includes:
    - Application code (app.py)
    - Requirements file (requirements.txt)
    - Template files
    - Static assets
    - Deployment info file with timestamp and git metadata

## Environment Variables

```
REPO_URL = https://github.com/Asad-Khurshid1585/SSD-Final.git
DEPLOYMENT_DIR = /var/www/ssd-app (Linux) or C:\SSD-App-Deployment (Windows)
PYTHON_VERSION = 3.10
```

## Post-Build Actions

### Success
- Displays success message
- Provides deployment directory path
- Confirms all stages completed

### Failure
- Displays failure message
- Directs user to check logs

### Always
- Displays pipeline execution summary
- Shows build duration and build number

## Usage

### For Linux/Mac Systems
```bash
# Run the pipeline with default Jenkinsfile
# In Jenkins UI, select "Jenkinsfile" as pipeline definition
```

### For Windows Systems
```bash
# Run the pipeline with Windows Jenkinsfile
# In Jenkins UI, select "Jenkinsfile.windows" as pipeline definition
```

## Prerequisites

- Jenkins server installed and running
- Git installed on Jenkins agent
- Python 3.10+ installed on Jenkins agent
- Internet access to clone repository
- Sufficient disk space for deployment

## Test Coverage

The pipeline includes comprehensive unit tests covering:
- Model validation
- Route functionality
- CRUD operations
- Data constraints
- HTTP status codes

All 12 tests pass successfully before deployment.

## Application Details

- **Framework**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Testing Framework**: pytest
- **Features**:
  - User management system
  - CRUD operations
  - Form handling
  - Database persistence

## Deployment Artifacts

After successful deployment:
- Application files copied to deployment directory
- `DEPLOYMENT_INFO.txt` created with metadata
- Git commit hash and branch information recorded
- Timestamp of deployment recorded
