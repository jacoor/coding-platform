import requests
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Judge0 API configuration
API_URL = "https://judge0-ce.p.rapidapi.com/submissions"
HEADERS = {
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),  # Load the API key from the environment
}

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def concatenate_files(file1, file2):
    """Combine the contents of two files."""
    code = read_file(file1)
    tests = read_file(file2)
    return f"{code}\n\n{tests}"

def submit_code(code):
    payload = {
        "source_code": code,
        "language_id": 71,  # Python (3.8.1)
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 201:
        return response.json().get("token")
    else:
        print("Error submitting code:", response.text)
        return None

def get_submission_result(token):
    response = requests.get(f"{API_URL}/{token}?base64_encoded=false", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching submission result:", response.text)
        return None

def wait_for_result(token, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = get_submission_result(token)
        status = result["status"]["description"]

        # Handle runtime errors (NZEC)
        if status == "Runtime Error (NZEC)":
            print("Runtime Error (NZEC) occurred. Details:")
            print("Error:", result.get("stderr"))
            return result

        if status in ["Accepted", "Compilation Error", "Time Limit Exceeded"]:
            return result

        print(f"Current status: {status}. Retrying in 2 seconds...")
        time.sleep(2)

    print("Timeout reached. No result available.")
    return None

def main():
    combined_code = concatenate_files("code.py", "tests.py")

    print("Submitting code...")
    token = submit_code(combined_code)
    if not token:
        return

    print("Waiting for result...")
    result = wait_for_result(token, timeout=30)

    if result:
        print("Final Status:", result["status"]["description"])
        print("Output:", result.get("stdout"))  # Standard Output
        print("Error:", result.get("stderr"))   # Standard Error
        print("Compilation Error:", result.get("compile_output"))
    else:
        print("Failed to fetch the result within 30 seconds.")

if __name__ == "__main__":
    main()
