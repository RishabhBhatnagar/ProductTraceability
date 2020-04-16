from django.urls import path
from login import views


urlpatterns = [
    path('', views.home),
    path('home.html', views.home),
    path('about.html', views.about),
    path('login.html', views.login),
    path('contact.html', views.contact),
    path('add_detail.html', views.add_detail),
    path('view_details.html', views.view_details),
    path('actor.html', views.actor),
    path('timeline.html', views.timeline),
    path('signup', views.signup),
    path('product_detail_hander', views.product_detail_hander)
]