from django.contrib import admin

from .models import CrawlRequest, CrawledImages

admin.site.register(CrawlRequest)
admin.site.register(CrawledImages)