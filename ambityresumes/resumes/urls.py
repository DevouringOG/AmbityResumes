from django.urls import path

import resumes.views

app_name = "resumes"

urlpatterns = [
    path(
        "search/",
        resumes.views.SearchResumes.as_view(),
        name="search",
    ),
]
