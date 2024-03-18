from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('myorder',views.myorder,name='myorder'),
    # path('order',views.order,name='order'),
    path('aei',views.aei,name='aei'),
    path('tshirt',views.tshirt,name='tshirt'),
    path('pant',views.pant,name='pant'),
    path('shoes',views.shoes,name='shoes'),
    path('watch',views.watch,name='watch'),
    path('jacket',views.jacket,name='jacket'),
    path('bags',views.bags,name='bags'),
    path('registration',views.registration,name='registration'),
    path('login',views.log_in,name='login'),
    path('profile',views.profile,name='profile'),
    path('logout',views.log_out, name="logout"),
    path('changepassword',views.changepassword, name="changepassword"),
    
    
]
