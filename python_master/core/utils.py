import logging
import time

import requests
from django.conf import settings


def submit_code(code):
    """Submit code to Judge0 with the provided code."""
    logging.debug("Submitting code to Judge0.")
    data = {
        "source_code": code,
        "language_id": 71,  # Language ID for Python 3.8.1
        "redirect_stderr_to_stdout": True,  # Redirect stderr to stdout
    }

    try:
        response = requests.post(settings.JUDGE0["API_URL"], json=data, headers=settings.JUDGE0["HEADERS"])

        if response.status_code == 201:
            submission = response.json()
            logging.info(f"Code submission successful. Token received: {submission['token']}")
            return submission["token"]
        else:
            logging.error(f"Error during submission: {response.status_code}, {response.text}")
            raise Exception(f"Error during submission: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        logging.exception(f"An error occurred while submitting the code: {e}")
        return None


def get_submission_result(token):
    """Fetches the result of the code submission."""
    logging.debug(f"Fetching result for token: {token}")
    try:
        response = requests.get(f"{settings.JUDGE0["API_URL"]}/{token}", headers=settings.JUDGE0["HEADERS"])

        if response.status_code == 200:
            submission = response.json()
            logging.debug(f"Submission result: {submission}")
            return submission
        else:
            logging.error(f"Error fetching result: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.exception(f"An error occurred while fetching the result: {e}")
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

        # Safely get stdout output
        stdout_output = result.get("stdout", "")

        # Check if tests passed based on stdout
        if stdout_output and "OK" in stdout_output:
            logging.info("All tests passed successfully.")
            return result

        # Handle runtime errors (NZEC)
        if status == "Runtime Error (NZEC)":
            logging.error("Runtime Error (NZEC) occurred. Details:")
            logging.error("Output:", stdout_output)
            return result  # Stop processing further

        # Handle other terminal states (Compilation Error, etc.)
        if status in ["Compilation Error", "Time Limit Exceeded"]:
            return result

        logging.info(f"Current status: {status}. Retrying in {settings.JUDGE0["DELAY"]} seconds...")
        time.sleep(settings.JUDGE0["DELAY"])  # Use the global DELAY value

    logging.warning("Timeout reached. No result available.")
    return None
