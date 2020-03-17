from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from items.models import Item, Location, Image, Like, Comment
from django.utils.html import strip_tags
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from . models import Additional


def RegisterView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login_url")
    else:
        form = UserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'registration/register.html', context)


@login_required
def ProfileView(request):
    try:
        additional_info = Additional.objects.get(user_id=request.user.id)
    except Additional.DoesNotExist:
        additional_info = None
    locations = Location.objects.all()
    image_list = Image.objects.all()
    item_list = Item.objects.filter(user_id = request.user).order_by('-pub_date') 
    like_list = Like.objects.select_related('item').filter(user_id=request.user.id)
    liked_item_list = Item.objects.all()
    
    
    context ={
       'locations':locations,
       'item_list':item_list,
       'image_list':image_list,
       'like_list':like_list,
       'liked_item_list':liked_item_list,
       'additional_info':additional_info,
    }
   
    return render(request, 'profile.html', context)

@login_required
def update_ad(request, ad_id):
    ad = Item.objects.get(id=ad_id)
    usr = request.user
    room = strip_tags(request.POST['rooms'])
    kind = strip_tags(request.POST['kind'])
    location2 = Location.objects.get(id=request.POST['location'])
    price = request.POST['price']
    if price.isdigit():
        price = price
    else:
        price = '0'
    status = strip_tags(request.POST['status'])
    address = strip_tags(request.POST['address'])
    age = strip_tags(request.POST['age'])
    description = strip_tags(request.POST['description'])
    title = strip_tags(request.POST['title'])
    category = strip_tags(request.POST['category'])
        
    ad.title=title
    ad.room=room
    ad.description=strip_tags(description)
    ad.description=ad.description[:1000]
    ad.user_id = usr.id
    ad.kind = kind
    ad.location_id = location2
    ad.price = price
    ad.status = status
    ad.address = address
    ad.age = age
    ad.category = category
    ad.save()
    
    context = {
        'ad':ad,
    }
    return HttpResponseRedirect(reverse('accounts:profile', args=()))


@login_required
def create_adview(request):
    room = strip_tags(request.POST['rooms'])
    kind = strip_tags(request.POST['kind'])
    location = Location.objects.get(id=request.POST['location'])
    price = strip_tags(request.POST['price'])
    if price.isdigit():
        price = price
    else:
        price = '0'
    status = strip_tags(request.POST['status'])
    address = strip_tags(request.POST['address'])
    age = strip_tags(request.POST['age'])
    title = strip_tags(request.POST['title'])
    description = strip_tags(request.POST['description'])
    description = description[:3000]
    category = strip_tags(request.POST['category'])
    usr = strip_tags(request.POST['user'])
    ad = Item(user_id=usr, room=room, kind=kind, location=location, price=price, status=status, address=address, age=age, title=title, description=description, category=category)
    ad.save()
    
    context = {
        'ad':ad,
    }
    return HttpResponseRedirect(reverse('accounts:profile', args=()))

@login_required
def add_imageview(request, ad_id):
    image = request.FILES['image']
    alt = strip_tags(request.POST['alt'])
    img = Image(alt=alt, image=image, item_id=ad_id)
    img.save()
    img2 = Image.objects.filter(item_id=ad_id).order_by('-id')
    for im in img2:
        if im == img2[0]:
            im.is_main=True
            im.save()
        else:
            im.is_main=False
            im.save()
    
    return HttpResponseRedirect(reverse('accounts:profile', args=()))


@login_required
def delete_imageview(request, image_id):
    image = Image.objects.get(id=image_id)
    image.delete()
    context = {
        'image':image,
    }
    return HttpResponseRedirect(reverse('accounts:profile', args=()))


@login_required
def update_profile(request):
    info = Additional.objects.get(user_id=request.user.id)
    name = strip_tags(request.POST['name'])
    email = strip_tags(request.POST['email'])
    telephone = strip_tags(request.POST['telephone'])
    if telephone.isdigit():
        telephone = telephone
    else:
        telephone = "000"
    info.name=name
    info.email=email
    info.telephone=telephone
    info.save()

    return HttpResponseRedirect(reverse('accounts:profile', args=()))


@login_required
def create_profile(request):
    name = strip_tags(request.POST['name'])
    email = strip_tags(request.POST['email'])
    telephone = strip_tags(request.POST['telephone'])
    if telephone.isdigit():
        telephone = telephone
    else:
        telephone = "000"
    info = Additional(user_id=request.user.id, name=name, email=email, telephone=telephone)
    info.save()

    return HttpResponseRedirect(reverse('accounts:profile', args=()))

