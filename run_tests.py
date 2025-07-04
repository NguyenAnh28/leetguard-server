#!/usr/bin/env python3
"""
Test runner script for LeetGuard Server.
Provides easy commands for running different types of tests.
"""
import sys
import subprocess
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed!")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("""
🧪 LeetGuard Test Runner

Usage:
    python run_tests.py [command]

Commands:
    unit          - Run unit tests only
    integration   - Run integration tests only
    email         - Run email integration tests
    all           - Run all tests
    coverage      - Run tests with coverage report
    manual-email  - Run manual email test
    help          - Show this help message

Examples:
    python run_tests.py unit
    python run_tests.py integration
    python run_tests.py all
    python run_tests.py manual-email
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        main()
        return
    
    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    if command == "unit":
        success = run_command(
            "python -m pytest tests/unit/ -v --tb=short",
            "Running unit tests..."
        )
    
    elif command == "integration":
        success = run_command(
            "python -m pytest tests/integration/ -v --tb=short",
            "Running integration tests..."
        )
    
    elif command == "email":
        success = run_command(
            "python -m pytest tests/integration/test_email_integration.py -v --tb=short",
            "Running email integration tests..."
        )
    
    elif command == "all":
        success = run_command(
            "python -m pytest tests/ -v --tb=short",
            "Running all tests..."
        )
    
    elif command == "coverage":
        # Install coverage if not available
        try:
            import coverage
        except ImportError:
            print("📦 Installing coverage...")
            subprocess.run("pip install coverage", shell=True, check=True)
        
        success = run_command(
            "coverage run -m pytest tests/ && coverage report && coverage html",
            "Running tests with coverage..."
        )
    
    elif command == "manual-email":
        print("🧪 Manual Email Test")
        print("=" * 50)
        success = run_command(
            "python tests/integration/test_email_integration.py",
            "Running manual email test..."
        )
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python run_tests.py help' for available commands")
        return
    
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 