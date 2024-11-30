import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Judge0 API configuration
API_URL = "https://judge0-ce.p.rapidapi.com/submissions"
HEADERS = {
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),  # Load the API key from the environment
}

# Configurable delay (in seconds)
DELAY = 0.5  # Default to 500ms

def read_file(file_path):
    """Reads the contents of a file."""
    with open(file_path, "r") as file:
        content = file.read()
    return content

def concatenate_files(code_file, test_file):
    """Concatenate code with test cases."""
    code = read_file(code_file)
    tests = read_file(test_file)
    return prepare_test_script(code, tests)

def prepare_test_script(user_code, test_cases):
    """Prepare the test script by combining user code with pytest test cases."""
    full_script = f"""
# Install pytest
import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pytest'])

# User's original code
{user_code}

# Test cases
import pytest

{test_cases}

# Run tests
if __name__ == '__main__':
    pytest.main(['-v'])
"""
    return full_script

def submit_code(code):
    """Submit code to Judge0 with the provided code."""
    data = {
        "source_code": code,
        "language_id": 71,  # Language ID for Python 3.8.1
        "stdin": "",  # Empty input for now (you can modify this)
        "expected_output": "",  # Optional: specify expected output if needed
    }

    try:
        response = requests.post(API_URL, json=data, headers=HEADERS)
        
        if response.status_code == 201:
            submission = response.json()
            print(f"Code submission successful. Token received: {submission['token']}")
            return submission['token']
        else:
            print(f"Error during submission: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while submitting the code: {e}")
        return None

def get_submission_result(token):
    """Fetches the result of the code submission."""
    try:
        response = requests.get(f"{API_URL}/{token}", headers=HEADERS)
        
        if response.status_code == 200:
            submission = response.json()
            return submission
        else:
            print(f"Error fetching result: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the result: {e}")
        return None

def wait_for_result(token, timeout=30):
    """Wait for the result (status and output)."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = get_submission_result(token)
        
        if result is None:
            print("Error while fetching result. Stopping execution.")
            return None

        status = result["status"]["description"]

        # Handle runtime errors (NZEC)
        if status == "Runtime Error (NZEC)":
            print("Runtime Error (NZEC) occurred. Details:")
            print("Error:", result.get("stderr"))
            return result  # Stop processing further
        
        # Handle other terminal states (Accepted, Compilation Error, etc.)
        if status in ["Accepted", "Compilation Error", "Time Limit Exceeded"]:
            return result

        print(f"Current status: {status}. Retrying in {DELAY} seconds...")
        time.sleep(DELAY)  # Use the global DELAY value

    print("Timeout reached. No result available.")
    return None

def main():
    """Main function to submit the code and wait for results."""
    print("Starting the process...")

    # Concatenate code and tests
    code = concatenate_files("code.py", "tests.py")
    print("Code with tests prepared.")

    # Submit code to Judge0
    token = submit_code(code)
    if not token:
        print("Failed to submit code. Stopping process.")
        return

    # Wait for and get the result
    result = wait_for_result(token, timeout=30)
    if result:
        print("Final Status:", result['status']['description'])
        print("Output:", result['stdout'])
        print("Error:", result['stderr'])
        print("Compilation Error:", result['compile_output'])
    else:
        print("Failed to fetch the result within 30 seconds. Stopping process.")

if __name__ == "__main__":
    main()
