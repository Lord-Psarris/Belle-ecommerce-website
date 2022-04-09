from django.urls import path
from . import views, forms

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='all_products'),

    path('product/<str:short_name>', views.view_product_details, name='view_product_details'),

    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('order-complete/', views.order_complete, name='order_complete'),

    path('use-coupon/', forms.use_coupon, name='use_coupon'),
    path('process-checkout/', forms.process_checkout, name='process_checkout'),
    path('add-review/', forms.add_review, name='add_review'),

    path('add-to-wishlist/', forms.add_to_wishlist, name='add_to_wishlist'),
    path('remove-wishlist-item/', forms.remove_item_from_wishlist, name='remove_item_from_wishlist'),

    path('add-to-cart/', forms.add_to_cart, name='add_to_cart'),
    path('items-in-cart-count/', forms.get_number_of_cart_items, name='get_number_of_cart_items'),
    path('update-cart-data/', forms.update_cart_data, name='update_cart_data'),
    path('clear-cart-items/', forms.clear_cart_items, name='clear_cart_items'),
    path('get-cart-items/', forms.get_cart_items, name='get_cart_items'),
    path('remove-cart-item/', forms.remove_item_from_cart, name='remove_item_from_cart'),

    path('collections/', views.collections, name='collections'),
    path('collections/<str:collection>', views.collection_view, name='collection_view'),
]