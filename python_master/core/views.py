import json

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .utils import submit_code, wait_for_result


class IndexView(TemplateView):
    template_name = "core/index.html"


class SubmitView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            tests = data.get("tests", "")

            # Combine the code and tests into a full script
            full_script = f"""
# User's original code
{code}

{tests}

# Run tests
if __name__ == '__main__':
    unittest.main()
"""
            print(full_script)
            # Submit the full script to Judge0
            token = submit_code(full_script)
            if not token:
                return JsonResponse({"status": "error", "message": "Code submission failed"})

            # Wait for the result from Judge0
            result = wait_for_result(token)
            if not result:
                return JsonResponse({"status": "error", "message": "Failed to retrieve submission result"})

            # Extract relevant information from the result
            status = result["status"]["description"]
            stdout_output = result.get("stdout", "")
            stderr_output = result.get("stderr", "")

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Submission processed",
                    "result": {"status": status, "stdout": stdout_output, "stderr": stderr_output},
                }
            )

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
