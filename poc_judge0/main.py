import requests
import json
import time

# Judge0 API URL
API_URL = "https://judge0-ce.p.rapidapi.com/submissions"
HEADERS = {
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
    "x-rapidapi-key": "79dfa15cbdmsh8031319b3d7e30ep18a717jsn3d23dbcea455",  # Zastąp własnym kluczem API
}


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def submit_code(code, tests):
    payload = {
        "source_code": code,
        "language_id": 71,  # Python (3.8.1)
        "stdin": tests,
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

def wait_for_result(token):
    print("Waiting for result...")
    while True:
        result = get_submission_result(token)
        status = result["status"]["description"]
        if status in ["Accepted", "Compilation Error", "Runtime Error", "Time Limit Exceeded"]:
            return result
        print(f"Current status: {status}. Retrying in 2 seconds...")
        time.sleep(2)

def main():
    code = read_file("code.py")
    tests = read_file("tests.txt")

    print("Submitting code...")
    token = submit_code(code, tests)
    if not token:
        return

    result = wait_for_result(token)

    print("Final Status:", result["status"]["description"])
    print("Output:", result.get("stdout"))  # Standard Output
    print("Error:", result.get("stderr"))   # Standard Error
    print("Compilation Error:", result.get("compile_output"))

if __name__ == "__main__":
    main()
