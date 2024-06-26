from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("resumes/", include("resumes.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        *static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        ),
    ]
else:
    urlpatterns += staticfiles_urlpatterns()
