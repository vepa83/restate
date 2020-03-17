from django.urls import path
from . import views

app_name = 'items'
urlpatterns = [
    path('', views.homeview, name="home_url"),
    path('<int:ad_id>/', views.detailview, name="detail_url"),
    path('like_ad/<int:ad_id>/', views.like_adview, name="like_ad_url"),
    path('location/<int:location_id>/', views.filter_locationview, name="location_filter_url"),
    path('kind/<kind>', views.filter_kindview, name="kind_filter_url"),
    path('category/<category>', views.filter_categoryview, name="category_filter_url"),
    path('add_comment/<int:item_id>/', views.add_comment, name="add_comment"),
    path('delete_item/<int:item_id>/', views.delete_item, name="delete_item"),
    path('search_result/', views.search_view, name="search_url"),
    path('<int:ad_id>/like/', views.like_ad_detail_view, name="like_ad_detail_url"),

]