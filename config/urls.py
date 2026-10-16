from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from cafe.sitemaps import StaticSitemap, PostSitemap

sitemaps = {"static": StaticSitemap, "posts": PostSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("cafe.urls")),
]
