from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from items.models import Item
from . serializers import ItemSerializer

@api_view(['GET'])
def item_serializer(request):
    if request.method == 'GET':
        item_list_s = Item.objects.exclude(status='pending').order_by('-pub_date')[:10]
        serializer = ItemSerializer(item_list_s, many=True)
        return Response(serializer.data)
