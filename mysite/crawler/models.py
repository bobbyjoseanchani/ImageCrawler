from __future__ import unicode_literals
from django.db import models
from django.db.models import signals

class CrawlRequest(models.Model):
    """Model to hold crawl request."""
    seed_url = models.CharField(max_length=300)
    depth = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default="Started")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class CrawledImages(models.Model):
    """Model to hold crawled images.
    This model has a many-to-one relationship with CrawlRequest.
    """
    crawl_request = models.ForeignKey(CrawlRequest, related_name='images')
    image_url = models.CharField(max_length=300)

    def __unicode__(self):
        return self.image_url

from .tasks import crawl_task 
def process_crawl_request(sender, instance, created, **kwargs):
    """Create a celery task for every crawl request recieved.
    """
    if created:
        # Create task only if a new request was created
        crawl_task.apply_async( (sender.__name__, instance.id), serializer = 'json' )

signals.post_save.connect(process_crawl_request, sender=CrawlRequest)