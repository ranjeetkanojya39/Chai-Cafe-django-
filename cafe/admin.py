from django.contrib import admin
from .models import Page, Post

admin.site.register(Page)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "published_at")
    prepopulated_fields = {"slug": ("title",)}
