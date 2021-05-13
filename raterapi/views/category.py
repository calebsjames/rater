"""View module for handling requests about category types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from raterapi.models import Category


class CategoryViewSet(ViewSet):
    
    # Get a single record
    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    # Get a list of all records
    def list(self, request):
        categories = Category.objects.all()
        
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'name')
