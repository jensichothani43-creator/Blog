from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("blog.urls")),

    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
]


from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]