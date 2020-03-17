from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "locations"


class Item(models.Model):
        
    KINDS = (
        ('apartment', 'apartment'),
        ('house', 'house'),
        ('penthouse', 'penthouse'),
        ('condo', 'condo'),
        ('studio', 'studio'),
        ('office', 'office'),
        ('store', 'store'),
    )
    
    STATUSES = (
        ('open', 'open'),
        ('removed', 'removed'),
        ('pending', 'pending'),
        ('deleted', 'deleted'),
        ('closed', 'closed'),
        ('frozen', 'frozen'),
    )

    CATEGORIES = (
        ('sell', 'sell'),
        ('buy', 'buy'),
        ('change', 'change'),
        ('rent', 'rent'),
    )

    ROOMS =(
        ('one bedroom', 'one bedroom'),
        ('two bedrooms', 'two bedrooms'),
        ('three bedrooms', 'three bedrooms'),
        ('four bedrooms', 'four bedrooms'),
        ('more than 4 bedrooms', 'more than 4 bedrooms'),
    )

    AGES = (
        ('new', 'new'),
        ('less than 5 years', 'less than 5 years'),
        ('less than 10 years', 'less than 10 years'),
        ('more than 10 years', 'more than 10 years'),
        ('more than 20 years', 'more than 20 years'),
    )

    kind = models.CharField(max_length=25, choices=KINDS, default='house')
    status = models.CharField(max_length=25, choices=STATUSES, default="pending")
    category = models.CharField(max_length=25, choices=CATEGORIES, default='sell')
    room = models.CharField(max_length=25, choices=ROOMS, default='two bedrooms')
    age = models.CharField(max_length=25, choices=AGES, default='less than 5 years')
       
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    
    is_vip = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"



class Like(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.item.title

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    alt = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(220, 220)],
                               format='JPEG',
                               options={'quality': 80})
    
    def __str__(self):
        return self.alt

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"


class Footer(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "footer"
        verbose_name_plural = "footers"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField()


    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
