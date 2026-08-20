from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse
from django.conf.urls.static import static
from blog.sitemaps import PostSitemap


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Disallow: /accounts/\n"
        "\n"
        "Sitemap: https://blog-ak8g.onrender.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


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

    # Robots.txt
    path("robots.txt", robots_txt),

    # Media files
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
