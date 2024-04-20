from django.urls import path

from resumes.views import (
    FolderView,
    ResumeView,
    SaveFolderView,
    SearchResumesView,
    UpdateDataView,
)

app_name = "resumes"

urlpatterns = [
    path(
        "search/",
        SearchResumesView.as_view(),
        name="search",
    ),
    path(
        "update/",
        UpdateDataView.as_view(),
        name="update",
    ),
    path(
        "save/",
        SaveFolderView.as_view(),
        name="save",
    ),
    path(
        "folder/<int:folder_pk>",
        FolderView.as_view(),
        name="folder",
    ),
    path(
        "folder/<int:folder_pk>/<int:resume_pk>",
        ResumeView.as_view(),
        name="view",
    ),
]
