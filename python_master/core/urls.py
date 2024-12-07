from django.urls import path
from .views import SubmitView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("submit/", SubmitView.as_view(), name="submit"),
]
