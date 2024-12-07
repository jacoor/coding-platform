from django.http import JsonResponse
from django.views import View
import json
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"


class SubmitView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            tests = data.get("tests", "")
            print(code, tests)
            # Process the code and tests as needed
            return JsonResponse({"status": "success", "message": "Submission received"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
