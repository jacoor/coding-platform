import json

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from .utils import submit_code, wait_for_result
from django.views.generic import ListView
from core.models import EducationPath


class IndexView(TemplateView):
    template_name = "core/index.html"


class SubmitView(View):
    def post(self, request: JsonResponse, *args: tuple, **kwargs: dict) -> JsonResponse:
        # args and kwargs are not used, so let's remove them
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            tests = data.get("tests", "")

            # Combine the code and tests into a full script
            full_script = (
                f"# User's original code\n{code}\n\n{tests}\n\n"
                "# Run tests\nif __name__ == '__main__':\n    unittest.main()"
            )

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

class EducationPathListView(ListView):
    model = EducationPath
    template_name = "core/education_path_list.html"
    context_object_name = "paths"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context