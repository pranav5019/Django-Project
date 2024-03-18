from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('',views.HomeView.as_view(),name='home'),
    path('contact',views.contact,name='contact'),
    path('myorder',views.myorder,name='myorder'),
    # path('order',views.order,name='order'),
    path('aei',views.aei,name='aei'),
    path('tshirt',views.TshirtView.as_view(),name='tshirt'),
    path('pant',views.PantView.as_view(),name='pant'),
    path('shoes',views.ShoesView.as_view(),name='shoes'),
    path('watch',views.WatchView.as_view(),name='watch'),
    path('jacket',views.JacketView.as_view(),name='jacket'),
    path('bags',views.BagsView.as_view(),name='bags'),
    path('registration',views.registration,name='registration'),
    path('login',views.log_in,name='login'),
    path('profile',views.profile,name='profile'),
    path('logout',views.log_out, name="logout"),
    path('changepassword',views.changepassword, name="changepassword"),
    path('storedetails/<int:id>',views.StoreDetailView.as_view(),name='storedetails'),
    path('view_cart',views.view_cart, name="viewcart"),

    path('add_to_cart/<int:id>',views.add_to_cart, name="addtocart"),

    path('add_quantity/<int:id>', views.add_quantity, name='add_quantity'),

    path('delete_quantity/<int:id>', views.delete_quantity, name='delete_quantity'),
    
    
    
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)