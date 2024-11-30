import os
import time
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    logging.debug(f"Reading file: {file_path}")
    with open(file_path, "r") as file:
        content = file.read()
    logging.debug(f"File content from {file_path}: {content[:100]}...")  # Log first 100 characters
    return content

def concatenate_files(code_file, test_file):
    """Concatenate code with test cases."""
    logging.debug(f"Concatenating files: {code_file} and {test_file}")
    code = read_file(code_file)
    tests = read_file(test_file)
    return prepare_test_script(code, tests)

def prepare_test_script(user_code, test_cases):
    """Prepare the test script by combining user code with unittest test cases."""
    logging.debug("Preparing test script.")
    full_script = f"""

# User's original code
{user_code}


{test_cases}

# Run tests

if __name__ == '__main__':
    unittest.main()
"""
    logging.debug(f"Prepared script: {full_script[:100]}...")  # Log first 100 characters
    return full_script

def submit_code(code):
    """Submit code to Judge0 with the provided code."""
    logging.debug("Submitting code to Judge0.")
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
            logging.info(f"Code submission successful. Token received: {submission['token']}")
            return submission['token']
        else:
            logging.error(f"Error during submission: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while submitting the code: {e}")
        return None

def get_submission_result(token):
    """Fetches the result of the code submission."""
    logging.debug(f"Fetching result for token: {token}")
    try:
        response = requests.get(f"{API_URL}/{token}", headers=HEADERS)
        
        if response.status_code == 200:
            submission = response.json()
            logging.debug(f"Submission result: {submission}")
            return submission
        else:
            logging.error(f"Error fetching result: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching the result: {e}")
        return None

def wait_for_result(token, timeout=30):
    """Wait for the result (status and output)."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = get_submission_result(token)
        
        if result is None:
            logging.error("Error while fetching result. Stopping execution.")
            return None

        status = result["status"]["description"]
        logging.info(f"Current status: {status}")

        # Safely get stderr output
        stderr_output = result.get("stderr", "")

        # Check if tests passed
        if stderr_output and "OK" in stderr_output:
            logging.info("All tests passed successfully.")
            return result

        # Handle runtime errors (NZEC)
        if status == "Runtime Error (NZEC)":
            logging.error("Runtime Error (NZEC) occurred. Details:")
            logging.error("Error:", stderr_output)
            return result  # Stop processing further
        
        # Handle other terminal states (Compilation Error, etc.)
        if status in ["Compilation Error", "Time Limit Exceeded"]:
            return result

        if status != "Processing":
            logging.info(f"Current status: {status}. Retrying in {DELAY} seconds...")
        
        time.sleep(DELAY)  # Use the global DELAY value

    logging.warning("Timeout reached. No result available.")
    return None

def main():
    """Main function to submit the code and wait for results."""
    logging.info("Starting the process...")

    # Concatenate code and tests
    code = concatenate_files("code.py", "tests.py")
    logging.info("Code with tests prepared.")

    # Submit code to Judge0
    token = submit_code(code)
    if not token:
        logging.error("Failed to submit code. Stopping process.")
        return

    # Wait for and get the result
    result = wait_for_result(token, timeout=30)
    if result:
        logging.info("Final Status: %s", result['status']['description'])
        logging.info("Output: %s", result['stdout'])
        logging.info("Error: %s", result['stderr'])
        logging.info("Compilation Error: %s", result['compile_output'])
    else:
        logging.error("Failed to fetch the result within 30 seconds. Stopping process.")

if __name__ == "__main__":
    main()