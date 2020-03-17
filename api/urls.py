from django.urls import path
from . views import item_serializer
urlpatterns = [
    path('item_serialized/', item_serializer),
]