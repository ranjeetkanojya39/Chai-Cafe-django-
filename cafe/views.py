import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Page, Post


def _page(slug):
    """Meta from MySQL; harmless fallback if the row is missing."""
    return Page.objects.filter(slug=slug).first() or Page(
        slug=slug, meta_title=settings.SITE_NAME, meta_description="")


def _local_business(request):
    return {
        "@context": "https://schema.org",
        "@type": "CafeOrCoffeeShop",  # subtype of LocalBusiness
        "name": settings.SITE_NAME,
        "url": request.build_absolute_uri("/"),
        "image": request.build_absolute_uri("/static/img/hero.svg"),
        "description": "Cosy Mumbai café serving kadak masala chai, specialty coffee and fresh snacks.",
        "telephone": "+91-22-5555-0123",
        "priceRange": "₹₹",
        "servesCuisine": ["Indian", "Café", "Chai"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "12 Marine Lines Road",
            "addressLocality": "Mumbai",
            "addressRegion": "Maharashtra",
            "postalCode": "400002",
            "addressCountry": "IN",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 18.9432, "longitude": 72.8234},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "08:00",
            "closes": "23:00",
        }],
    }


def home(request):
    schema = json.dumps(_local_business(request), ensure_ascii=False, indent=2).replace("<", "\\u003c")
    return render(request, "home.html", {
        "page": _page("home"),
        "latest": Post.objects.all()[:2],
        "schema_json": schema,
    })


def about(request):
    return render(request, "about.html", {"page": _page("about")})


def blog_list(request):
    return render(request, "blog_list.html", {"page": _page("blog"), "posts": Post.objects.all()})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "post_detail.html", {"post": post})


def robots(request):
    body = "User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {}\n".format(
        request.build_absolute_uri(reverse("sitemap")))
    return HttpResponse(body, content_type="text/plain")
