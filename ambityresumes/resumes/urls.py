from django.urls import path

import resumes.views

app_name = "resumes"

urlpatterns = [
    path(
        "search/",
        resumes.views.SearchResumesView.as_view(),
        name="search",
    ),
    path(
        "update/",
        resumes.views.UpdateDataView.as_view(),
        name="update",
    ),
    path(
        "save/",
        resumes.views.SaveFolderView.as_view(),
        name="save",
    ),
    path(
        "folder/<int:pk>",
        resumes.views.FolderView.as_view(),
        name="folder",
    ),
]
