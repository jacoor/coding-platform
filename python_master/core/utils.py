import logging
import time

import requests
from django.conf import settings


def submit_code(code: str) -> str:
    """Submit code to Judge0 with the provided code."""
    logging.debug("Submitting code to Judge0.")
    data = {
        "source_code": code,
        "language_id": 71,  # Language ID for Python 3.8.1
        "redirect_stderr_to_stdout": True,  # Redirect stderr to stdout
    }

    try:
        response = requests.post(
            settings.JUDGE0["API_URL"],
            json=data,
            headers=settings.JUDGE0["HEADERS"],
            timeout=10  # Add timeout
        )

        created_status = 201
        if response.status_code == created_status:
            submission = response.json()
            logging.info("Code submission successful. Token received: %s", submission["token"])
            return submission["token"]

        error_message = "Error during submission"
        logging.error("Error during submission: %d, %s", response.status_code, response.text)
        raise RuntimeError(error_message)

    except requests.exceptions.RequestException:
        logging.exception("An error occurred while submitting the code")
        return None


def get_submission_result(token: str) -> dict:
    """Fetch the result of the code submission."""
    logging.debug("Fetching result for token: %s", token)
    try:
        response = requests.get(
            f"{settings.JUDGE0['API_URL']}/{token}",
            headers=settings.JUDGE0["HEADERS"],
            timeout=10  # Add timeout
        )

        ok_status = 200
        if response.status_code == ok_status:
            submission = response.json()
            logging.debug("Submission result: %s", submission)
            return submission

        logging.error("Error fetching result: %d, %s", response.status_code, response.text)

    except requests.exceptions.RequestException:
        logging.exception("An error occurred while fetching the result")
    return None


def wait_for_result(token: str, timeout: int = 30) -> dict:
    """Wait for the result (status and output)."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = get_submission_result(token)

        if result is None:
            logging.error("Error while fetching result. Stopping execution.")
            return None

        status = result["status"]["description"]
        logging.info("Current status: %s", status)

        # Safely get stdout output
        stdout_output = result.get("stdout", "")

        # Check if tests passed based on stdout
        if stdout_output and "OK" in stdout_output:
            logging.info("All tests passed successfully.")
            return result

        # Handle runtime errors (NZEC)
        if status == "Runtime Error (NZEC)":
            logging.error("Runtime Error (NZEC) occurred. Details:")
            logging.error("Output: %s", stdout_output)
            return result  # Stop processing further

        # Handle other terminal states (Compilation Error, etc.)
        if status in ["Compilation Error", "Time Limit Exceeded"]:
            return result

        logging.info("Current status: %s. Retrying in %d seconds...", status, settings.JUDGE0["DELAY"])
        time.sleep(settings.JUDGE0["DELAY"])  # Use the global DELAY value

    logging.warning("Timeout reached. No result available.")
    return None
