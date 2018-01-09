"""Serializers for APIs"""
from rest_framework import serializers
from .models import CrawlRequest, CrawledImages

class CrawlRequestSerializer(serializers.ModelSerializer):
    """Serializer for creating CrawlRequest"""
    class Meta:
        model = CrawlRequest
        fields = ('seed_url','depth')

class CrawlRequestListSerializer(serializers.ModelSerializer):
    """Serializer for listing CrawlRequests"""
    class Meta:
        model = CrawlRequest
        fields = ('id', 'seed_url','depth', 'status', 'created')

class CrawledImagesSerializer(serializers.ModelSerializer):
    """Serializer to return CrawledImages"""
    class Meta:
        model = CrawledImages
        fields = ('image_url',)
