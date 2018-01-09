from django.http import HttpResponse
from rest_framework import viewsets, mixins, permissions
from .models import CrawledImages, CrawlRequest
from .serializers import CrawlRequestSerializer, CrawlRequestListSerializer, CrawledImagesSerializer
from rest_framework.response import Response


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class CreateCrawlRequestPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		return True

class CrawlRequestViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Views for CrawlRequest model."""
    queryset = CrawlRequest.objects.all()
    serializer_class = CrawlRequestSerializer
    permission_classes = (CreateCrawlRequestPermission,)

    def list(self, request):
        """Overriding list method to use a different serializer."""
        serializer = CrawlRequestListSerializer(self.queryset, many=True)
        return Response(serializer.data)
 

class CrawledImagesViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CrawledImages.objects.all()
    serializer_class = CrawledImagesSerializer

    def list(self, request):
        """Overriding list method to use return only image urls related 
        to a single CrawlRequest.
        """
        my_crawl_id = request.query_params.get('crawl_id', None)
        my_images = self.queryset.filter(crawl_request__id=my_crawl_id)
        serializer = CrawledImagesSerializer(my_images, many=True)
        return Response(serializer.data)
   