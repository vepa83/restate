from django.contrib import admin
from . models import Item, Location, Image, Like, Footer, Comment

admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Footer)
admin.site.register(Comment)