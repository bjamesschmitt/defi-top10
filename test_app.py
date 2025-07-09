import json
import os
import importlib.util

def test_json_file():
    """Test if the JSON file exists and can be parsed."""
    print("Testing JSON file...")
    try:
        if not os.path.exists('defi-vulnerabilities-json.json'):
            print("ERROR: defi-vulnerabilities-json.json file not found!")
            return False
        
        with open('defi-vulnerabilities-json.json', 'r') as file:
            data = json.load(file)
            
        if 'vulnerabilities' not in data:
            print("ERROR: 'vulnerabilities' key not found in JSON data!")
            return False
            
        print("✓ JSON file exists and can be parsed successfully.")
        return True
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON format in defi-vulnerabilities-json.json!")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def test_flask_installed():
    """Test if Flask is installed."""
    print("Testing Flask installation...")
    try:
        flask_spec = importlib.util.find_spec("flask")
        if flask_spec is None:
            print("ERROR: Flask is not installed. Please run 'pip install flask'")
            return False
        print("✓ Flask is installed.")
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def test_app_files():
    """Test if all required application files exist."""
    print("Testing application files...")
    required_files = ['app.py', 'templates/index.html']
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"ERROR: The following required files are missing: {', '.join(missing_files)}")
        return False
    
    print("✓ All required application files exist.")
    return True

def run_tests():
    """Run all tests and provide a summary."""
    print("Running tests for DeFi Vulnerabilities Web Application...\n")
    
    json_test = test_json_file()
    flask_test = test_flask_installed()
    files_test = test_app_files()
    
    print("\nTest Summary:")
    print(f"JSON File Test: {'PASSED' if json_test else 'FAILED'}")
    print(f"Flask Installation Test: {'PASSED' if flask_test else 'FAILED'}")
    print(f"Application Files Test: {'PASSED' if files_test else 'FAILED'}")
    
    if json_test and flask_test and files_test:
        print("\nAll tests passed! You can run the application with 'python app.py'")
        print("Then open your browser and navigate to http://127.0.0.1:5000/")
    else:
        print("\nSome tests failed. Please fix the issues before running the application.")

if __name__ == "__main__":
    run_tests()