from django.urls import path

from .views import IndexView, SubmitView
from .views import EducationPathListView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("submit/", SubmitView.as_view(), name="submit"),
    path("education-paths/", EducationPathListView.as_view(), name="education_path_list"),
]