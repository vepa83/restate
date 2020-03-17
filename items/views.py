from django.shortcuts import render
from . models import Item, Location, Image, Like, Footer, Comment
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, Count
from django.utils.html import strip_tags
from django.core.paginator import Paginator


def homeview(request):
    locations = Location.objects.all()
    footer_list = Footer.objects.all()
    
    if request.user.is_authenticated:
        user = request.user
        last_vip_items_list = Item.objects.exclude(status ="pending").filter(is_vip=True).annotate(has_like = Count('like', filter=Q(like__user_id=user.id))).order_by('-pub_date')[:4]
        last_items_list = Item.objects.exclude(status ="pending").filter(is_vip=False).annotate(has_like = Count('like', filter=Q(like__user_id=user.id))).order_by('-pub_date')[:4]    
    else:
        last_vip_items_list = Item.objects.exclude(status ="pending").filter(is_vip=True).order_by('-pub_date')[:4]
        last_items_list = Item.objects.exclude(status ="pending").filter(is_vip=False).order_by('-pub_date')[:4]

    item_list = list(last_vip_items_list) + list(last_items_list)
    
    image_list = Image.objects.filter(item__in=item_list).filter(is_main=True)
    context ={
        'last_vip_items_list':last_vip_items_list,
        'last_items_list':last_items_list,
        'locations':locations,
        'image_list':image_list,
        'footer_list':footer_list,
    }
   
    return render(request, 'index.html', context)


def detailview(request, ad_id):
    check = ''
    if request.user.is_authenticated:
        
        if Like.objects.filter(item_id=ad_id, user_id=request.user.id).exists():
            check = 'yes'
        else:
            check = 'not yet'
    else:
        check = 'no'
    footer_list = Footer.objects.all()
    comment_list = Comment.objects.filter(item_id=ad_id)
    locations = Location.objects.all()
    item = Item.objects.get(id=ad_id)
    image_list = Image.objects.filter(item_id=ad_id)
     
    context = {
        'item':item,
        'image_list':image_list,
        'locations':locations,
        'comment_list':comment_list,
        'footer_list':footer_list,
        'check':check,
    }

    return render(request, 'detail.html', context)


def filter_locationview(request, location_id):
    footer_list = Footer.objects.all()
    chosen_location = Location.objects.get(id=location_id)
    if request.user.is_authenticated:
        item_list = Item.objects.filter(location_id=location_id).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id)))
    else:
        item_list = Item.objects.filter(location_id=location_id)
    amount = item_list.count()
    locations = Location.objects.all()
    image_list = Image.objects.filter(item__in=list(item_list)).filter(is_main=True)
    paginator = Paginator(item_list, 16)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
            

    context={
        'amount':amount,
        'page_num':page_num,
        'page':page,
        'item_list':page.object_list,
        'locations':locations,
        'chosen_location':chosen_location,
        'image_list':image_list,
        'footer_list':footer_list
    }

    return render(request, 'location_filter.html', context)



@login_required
def like_adview(request, ad_id):
    user = request.user
    like = Like.objects.filter(item_id=ad_id, user_id=user.id)
    if like:
        like.delete()
    else:
        like = Like(item_id=ad_id, user_id=user.id)
        like.save()
    return HttpResponseRedirect(reverse('items:home_url', args=()))



@login_required
def add_comment(request, item_id):
    text = request.POST['text']
    text = strip_tags(text)
    text = text[:500] 
    comment = Comment(user_id=request.user.id, text=text, item_id=item_id)
    comment.save()

    return HttpResponseRedirect(reverse('items:detail_url', args=(item_id,)))


@login_required
def delete_item(request, item_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        item = Item.objects.get(user_id=user_id, id=item_id)
        image_list = Image.objects.filter(item_id=item_id)
        for picture in image_list:
            picture.image.delete()
        image_list.delete()
        item.delete()
    return HttpResponseRedirect(reverse('accounts:profile', args=()))


def filter_kindview(request, kind):
    footer_list = Footer.objects.all()
    chosen_kind = kind
    if request.user.is_authenticated:
        item_list = Item.objects.filter(kind=chosen_kind).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id)))
    else:
        item_list = Item.objects.filter(kind=chosen_kind)
    amount = item_list.count()
    locations = Location.objects.all()
    image_list = Image.objects.filter(item__in=list(item_list)).filter(is_main=True)
    paginator = Paginator(item_list, 16)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
            

    context={
        'amount':amount,
        'page_num':page_num,
        'page':page,
        'item_list':page.object_list,
        'locations':locations,
        'chosen_kind':chosen_kind,
        'image_list':image_list,
        'footer_list':footer_list,
    }

    return render(request, 'kind_filter.html', context)

def filter_categoryview(request, category):
    footer_list = Footer.objects.all()
    chosen_category = category
    if request.user.is_authenticated:
        item_list = Item.objects.filter(category=chosen_category).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id)))
    else:
        item_list = Item.objects.filter(category=chosen_category)
    amount = item_list.count()
    locations = Location.objects.all()
    image_list = Image.objects.filter(item__in=list(item_list)).filter(is_main=True)
    
    paginator = Paginator(item_list, 16)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
            

    context={
        'page_num':page_num,
        'page':page,
        'item_list':page.object_list,
        'locations':locations,
        'chosen_category':chosen_category,
        'image_list':image_list,
        'footer_list':footer_list,
        'amount':amount,
    }

    return render(request, 'category_filter.html', context)


def search_view(request):
    locations = Location.objects.all()
    footer_list = Footer.objects.all()
    
    kind = request.POST['kind']
    if kind == 'any':
        kind_f = ['apartment','house','penthouse','condo','studio','office','store']
    else:
        kind_f = [kind]

    room = request.POST['room']
    if room == 'any':
        room_f = ['one bedroom','two bedrooms','three bedrooms','four bedrooms','more than 4 bedrooms']
    else:
         room_f = [room]

    category = request.POST['category']
    if category == 'any':
        category_f = ['sell', 'buy', 'change', 'rent']
    else:
        category_f = [category]

    age = request.POST['age']
    if age == 'any':
        age_f = ['new','less than 5 years','less than 10 years','more than 10 years','more than 20 years']
    else:
        age_f = [age]

    location = request.POST['location']
    if location == 'any':
        location_f = [area.id for area in Location.objects.all()]
    else:
        location_f = [location]
    
    text = strip_tags(request.POST['text'])[:15]
    if len(text)<=3:
        text = ''

    price = request.POST['price']
    
    if price.isdigit():
        price = price[:15]
    else:
        price = '0'
    
    price_range = request.POST['price_range']
    
    if  price_range == 'any' and (text == None or text == ''):
        if request.user.is_authenticated:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id))).order_by('-pub_date')
        else:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).order_by('-pub_date')
    
    elif price_range == 'any' and text != '' and text !=None:
        if request.user.is_authenticated:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(title__icontains=text).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id))).order_by('-pub_date')
        else:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(title__icontains=text).order_by('-pub_date')
    
    elif price_range == 'max' and text != '' and text !=None:
        if request.user.is_authenticated:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(title__icontains=text).filter(price__lt=price).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id))).order_by('-pub_date')
        else:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(title__icontains=text).filter(price__lt=price).order_by('-pub_date')
    
    elif price_range == 'max' and (text == '' or text ==None):
        if request.user.is_authenticated:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(price__lt=price).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id))).order_by('-pub_date')
        else:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(price__lt=price).order_by('-pub_date')
    
    elif price_range == 'min' and text != '' and text !=None:
        if request.user.is_authenticated:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(title__icontains=text).filter(price__gt=price).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id))).order_by('-pub_date')
        else:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(title__icontains=text).filter(price__gt=price).order_by('-pub_date')

    elif price_range == 'min' and (text == '' or text ==None):
        if request.user.is_authenticated:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(price__gt=price).annotate(has_like = Count('like', filter=Q(like__user_id=request.user.id))).order_by('-pub_date')
        else:
            item_list = Item.objects.filter(kind__in=kind_f).filter(room__in=room_f).filter(category__in=category_f).filter(age__in=age_f).filter(location_id__in=location_f).filter(price__gt=price).order_by('-pub_date')
    
    image_list = Image.objects.filter(item__in=list(item_list)).filter(is_main=True)
    
    paginator = Paginator(item_list, 16)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    
    context = {
        'item_list':item_list,
        'image_list':image_list,
        'locations':locations,
        'footer_list':footer_list,
        'page_num':page_num,
        'page':page,
    }
            
    return render(request, 'search_result.html', context)

@login_required
def like_ad_detail_view(request, ad_id):
    user = request.user
    like = Like.objects.filter(item_id=ad_id, user_id=user.id)
    if like:
        like.delete()
    else:
        like = Like(item_id=ad_id, user_id=user.id)
        like.save()
    return HttpResponseRedirect(reverse('items:detail_url', args=(ad_id,)))    

