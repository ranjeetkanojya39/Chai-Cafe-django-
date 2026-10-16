from django.db import models
from django.urls import reverse


class Page(models.Model):
    """SEO meta for static pages (home, about, blog)."""
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=170)

    def __str__(self):
        return self.slug


class Post(models.Model):
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=160)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=170)
    excerpt = models.CharField(max_length=255)
    content = models.TextField(help_text="HTML. Use h2/h3 only (the page title is the h1).")
    image = models.CharField(max_length=255, help_text="Path under static/, e.g. img/chai.svg")
    image_alt = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
