from django.conf.urls.static import static
from django.urls import path
from mysite import settings
from .import views

urlpatterns = [

    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('', views.store, name= 'store'),
    path('update_item/', views.updateItem, name= 'update_item'),
    path('process_order/', views.processOrder, name= 'process_order'),
    path('show/<int:pk>', views.showdetail, name='show-detail'),
    path('query', views.search, name='search'),
    path('profile', views.profile, name='profile'),
    path('collection/<int:id>', views.collection, name='collection')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
