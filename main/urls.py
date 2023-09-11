from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.callback, name='contact'),
    path('computers/', views.computers, name='computers'),
    path('mans_clothes/', views.mans_clothes, name='mans_clothes'),
    path('womans_clothes/', views.womans_clothes, name='womans_clothes'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.products, name='products'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_item/<int:product_id>/', views.decrease_item, name='decrease_item'),
    path('place_order/', views.place_order, name='place_order'),
]
