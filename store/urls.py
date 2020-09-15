from django.conf.urls.static import static
from django.urls import path
from mysite import settings
from .import views
from .views import registeruser

urlpatterns = [

    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('', views.store, name= 'store'),
    path('update_item/', views.updateItem, name= 'update_item'),
    path('update_wishlist/', views.updatewishlist, name='update_wishlist'),
    path('process_order/', views.processOrder, name= 'process_order'),
    path('show/<int:pk>/', views.showdetail, name='show-detail'),
    path('query', views.search, name='search'),
    path('profile', views.profile, name='profile'),


    path('supplier/', views.supplier, name='supplier'),
    path('addsupplier/', views.addsupplier, name='add-supplier'),

    path('update_profile/', views.update_profile, name='update-profile'),
    path('customer_register/', views.cregister, name='c-register'),


    path('addproduct/', views.add_product, name='add-product'),
    path('order/', views.order, name='order'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('update_like/', views.like, name='like'),

    path('category/', views.category, name='category'),

    path('registeruser/', views.registeruser, name='register.user'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
