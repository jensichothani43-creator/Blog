from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve

from blog.sitemaps import PostSitemap


# Sitemap configuration
sitemaps = {
    "posts": PostSitemap,
}


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Blog
    path("", include("blog.urls")),

    # Login / Logout
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),

    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),

    # Media files
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]