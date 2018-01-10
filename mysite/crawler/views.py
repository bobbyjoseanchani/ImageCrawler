from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from .models import CrawledImages, CrawlRequest
from .serializers import CrawlRequestSerializer, CrawlRequestListSerializer, CrawledImagesSerializer
from rest_framework.response import Response
from rest_framework.decorators import list_route

def index(request):
    """Serving index.html through django"""
    return render(request, 'crawler/index.html')

class CreateCrawlRequestPermission(permissions.BasePermission):
    """Permission class for CrawlRequest""" 
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

    @list_route()
    def get_images(self, request):
        """Custom method to return images corresponding to a crawl request"""
        my_crawl_id = request.query_params.get('id', None)
        my_request = self.queryset.filter(id=my_crawl_id)
        serializer = CrawledImagesSerializer(my_request, many=True)
        return Response(serializer.data)
