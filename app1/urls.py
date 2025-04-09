
from django.urls import path
from .views import *

app_name='app1'

urlpatterns = [
    path('', home_view, name='home1'),
    # path('home/', home, name='home'),
    path('about/',about, name='about'),
    path('contactus/',contactus, name='contactus'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("pickles/", pickles, name="pickles"),
    path("sweets/", sweets, name="sweets"),
    path("snacks/", snacks, name="snacks"),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/',update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/',remove_from_cart, name='remove_from_cart'),
    path('checkout/',checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    # path('order-success/', order_success, name='order_success'),
    path("order-history/", order_history, name="order_history"),
    path("wishlist/", wishlist, name="wishlist"),
    path("wishlist/add/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/", remove_from_wishlist, name="remove_from_wishlist"),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/add-address/', add_address, name='add_address'),
    path('profile/edit-address/<int:address_id>/', edit_address, name='edit_address'),
    path('profile/delete-address/<int:pk>/',delete_address, name='delete_address'),
    path('search/',search_products, name='search_products'),
    path('product/<int:product_id>/',product_detail, name='product_detail'),
    path('update-profile-photo/', update_profile_photo, name='update_profile_photo'),
]
