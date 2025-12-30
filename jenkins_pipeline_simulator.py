#!/usr/bin/env python3
"""
Jenkins Pipeline Simulation Script
Simulates the complete Jenkins pipeline locally for testing and validation
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

class JenkinsPipelineSimulator:
    def __init__(self):
        self.repo_url = 'https://github.com/Asad-Khurshid1585/SSD-Final.git'
        self.deployment_dir = os.path.join(os.getcwd(), 'simulated_deployment')
        self.workspace = os.path.join(os.getcwd(), 'jenkins_workspace')
        self.build_log = []
        
    def log(self, message, stage=None):
        """Log messages during pipeline execution"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        if stage:
            log_message = f"[{stage}] {log_message}"
        print(log_message)
        self.build_log.append(log_message)
    
    def run_command(self, command, stage=None):
        """Execute shell command and capture output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.workspace
            )
            if result.returncode != 0:
                self.log(f"Command failed: {command}", stage)
                self.log(f"Error: {result.stderr}", stage)
                return False
            self.log(f"Command executed successfully", stage)
            if result.stdout:
                self.log(f"Output: {result.stdout[:200]}...", stage)
            return True
        except Exception as e:
            self.log(f"Exception executing command: {str(e)}", stage)
            return False
    
    def stage_1_clone_repository(self):
        """Stage 1: Clone Repository"""
        self.log("Starting Stage 1: Clone Repository", "STAGE-1")
        
        # Clean workspace if exists
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
        os.makedirs(self.workspace, exist_ok=True)
        
        # Clone repository
        clone_cmd = f"git clone {self.repo_url} ."
        if self.run_command(clone_cmd, "STAGE-1"):
            self.log("Repository cloned successfully", "STAGE-1")
            return True
        return False
    
    def stage_2_install_dependencies(self):
        """Stage 2: Install Dependencies"""
        self.log("Starting Stage 2: Install Dependencies", "STAGE-2")
        
        # Create virtual environment
        venv_path = os.path.join(self.workspace, 'venv')
        if not os.path.exists(venv_path):
            if self.run_command(f"python -m venv venv", "STAGE-2"):
                self.log("Virtual environment created", "STAGE-2")
            else:
                return False
        
        # Install dependencies
        if sys.platform == 'win32':
            pip_cmd = "venv\\Scripts\\pip install -r requirements.txt"
        else:
            pip_cmd = ". venv/bin/activate && pip install -r requirements.txt"
        
        if self.run_command(pip_cmd, "STAGE-2"):
            self.log("Dependencies installed successfully", "STAGE-2")
            return True
        return False
    
    def stage_3_run_unit_tests(self):
        """Stage 3: Run Unit Tests"""
        self.log("Starting Stage 3: Run Unit Tests", "STAGE-3")
        
        if sys.platform == 'win32':
            pytest_cmd = "venv\\Scripts\\pytest test_app.py -v --tb=short"
        else:
            pytest_cmd = ". venv/bin/activate && pytest test_app.py -v --tb=short"
        
        if self.run_command(pytest_cmd, "STAGE-3"):
            self.log("All unit tests passed", "STAGE-3")
            return True
        else:
            self.log("Some tests failed", "STAGE-3")
            return False
    
    def stage_4_build_application(self):
        """Stage 4: Build Application"""
        self.log("Starting Stage 4: Build Application", "STAGE-4")
        
        # Verify application structure
        required_files = ['app.py', 'requirements.txt', 'templates']
        for file in required_files:
            filepath = os.path.join(self.workspace, file)
            if os.path.exists(filepath):
                self.log(f"Verified: {file}", "STAGE-4")
            else:
                self.log(f"Missing: {file}", "STAGE-4")
                return False
        
        self.log("Application structure verified", "STAGE-4")
        return True
    
    def stage_5_deploy_application(self):
        """Stage 5: Deploy Application (Simulation)"""
        self.log("Starting Stage 5: Deploy Application (Simulation)", "STAGE-5")
        
        # Create deployment directory
        os.makedirs(self.deployment_dir, exist_ok=True)
        self.log(f"Deployment directory created: {self.deployment_dir}", "STAGE-5")
        
        # Copy application files
        files_to_copy = ['app.py', 'requirements.txt', 'templates', 'test_app.py']
        for file in files_to_copy:
            src = os.path.join(self.workspace, file)
            dst = os.path.join(self.deployment_dir, file)
            try:
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                self.log(f"Copied: {file}", "STAGE-5")
            except Exception as e:
                self.log(f"Failed to copy {file}: {str(e)}", "STAGE-5")
                return False
        
        # Create deployment manifest
        manifest_path = os.path.join(self.deployment_dir, 'DEPLOYMENT_INFO.txt')
        try:
            with open(manifest_path, 'w') as f:
                f.write(f"Deployment Date: {datetime.now().isoformat()}\n")
                f.write(f"Deployment Directory: {self.deployment_dir}\n")
                f.write(f"Pipeline Simulator Version: 1.0\n")
                f.write(f"Status: SUCCESS\n")
            self.log(f"Deployment manifest created: DEPLOYMENT_INFO.txt", "STAGE-5")
        except Exception as e:
            self.log(f"Failed to create manifest: {str(e)}", "STAGE-5")
            return False
        
        self.log(f"Application deployed successfully to: {self.deployment_dir}", "STAGE-5")
        return True
    
    def run_pipeline(self):
        """Execute complete pipeline"""
        print("\n" + "="*80)
        print("JENKINS PIPELINE SIMULATOR - SSD-Final Flask Application")
        print("="*80 + "\n")
        
        stages = [
            ("Clone Repository", self.stage_1_clone_repository),
            ("Install Dependencies", self.stage_2_install_dependencies),
            ("Run Unit Tests", self.stage_3_run_unit_tests),
            ("Build Application", self.stage_4_build_application),
            ("Deploy Application", self.stage_5_deploy_application),
        ]
        
        results = {}
        for stage_name, stage_func in stages:
            try:
                result = stage_func()
                results[stage_name] = "✓ PASSED" if result else "✗ FAILED"
            except Exception as e:
                self.log(f"Exception in {stage_name}: {str(e)}", stage_name)
                results[stage_name] = "✗ FAILED"
        
        # Print summary
        print("\n" + "="*80)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*80)
        for stage, result in results.items():
            print(f"{stage:<30} {result}")
        
        # Overall status
        all_passed = all(v == "✓ PASSED" for v in results.values())
        overall_status = "✓ SUCCESS" if all_passed else "✗ FAILURE"
        print(f"\nOverall Status: {overall_status}")
        
        if all_passed:
            print(f"\nDeployment Directory: {self.deployment_dir}")
            print("\nFiles in deployment:")
            for root, dirs, files in os.walk(self.deployment_dir):
                level = root.replace(self.deployment_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")
        
        print("\n" + "="*80 + "\n")
        
        return all_passed


if __name__ == '__main__':
    simulator = JenkinsPipelineSimulator()
    success = simulator.run_pipeline()
    sys.exit(0 if success else 1)
