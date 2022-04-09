import json

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
from .reuseable_functions import get_all_products, get_on_sale_products, get_best_selling_products, get_all_cart_items, \
    get_suggested_products, get_all_product_reviews, \
    get_all_product_reviews_ratings


def all_products(request):
    products = []
    all_shop_products = get_all_products(include_out_of_stock=True)
    popular_products = get_best_selling_products(include_out_of_stock=False, order='descending')[:4]

    if request.GET.get('on-sale'):
        all_shop_products = get_on_sale_products(include_out_of_stock=True)

    if request.GET.get('sort'):
        sort = request.GET.get('sort')
        if sort == 'a-z':
            all_shop_products = sorted(all_shop_products, key=lambda x: x['name'])
        elif sort == 'z-a':
            all_shop_products = sorted(all_shop_products, key=lambda x: x['name'], reverse=True)
        elif sort == 'price-high-price-low':
            all_shop_products = sorted(all_shop_products, key=lambda x: x['price'], reverse=True)
        elif sort == 'price-low-price-high':
            all_shop_products = sorted(all_shop_products, key=lambda x: x['price'])
        elif sort == 'best-selling':
            all_shop_products = sorted(all_shop_products, key=lambda x: x['sales_count'])

    for product in all_shop_products:
        if request.GET.get('price'):
            price_range = request.GET.get('price').replace('%24', '').split('-')
            min_price = int(price_range[0].strip('+$ '))
            max_price = int(price_range[1].strip('+$ ')) + 1

            if product['price'] not in range(min_price, max_price) and product['slashed_price'] not in range(
                    min_price, max_price):
                continue
        if request.GET.get('category'):
            if product['category'] == request.GET.get('category'):
                products.append(product)
        else:
            products.append(product)

    data = {'products': products, 'popular_products': popular_products, 'products_length': len(products)}
    return render(request, 'products/shop.html', data)


def collections(request):
    return render(request, 'products/collections.html')


def collection_view(request, collection):
    return redirect(f'/shop?category={collection}')


def view_product_details(request, short_name):
    products = Product.objects.all()
    suggested_products = get_suggested_products(request.session.session_key)

    for product in products:
        if product.get_short_name() == short_name:
            slashed_price = product.price - round(product.price * (product.discounted_percent / 100))
            colors_available = json.loads(str(product.colors_available).strip("' ").replace('\'', '\"'))
            sizes_available = json.loads(str(product.sizes_available).strip("' ").replace('\'', '\"'))
            reviews = get_all_product_reviews(product)
            total_reviews = get_all_product_reviews_ratings(product)
            review_count = len(reviews)

            product_data = {
                'pk': product.id,
                'first_image': product.productimage_set.all()[0].file,
                'all_product_images': product.productimage_set.all(),
                'name': product.name,
                'short_name': product.get_short_name(),
                'price': product.price,
                'in_stock': product.in_stock,
                'out_of_stock': True if product.in_stock == 0 else False,
                'first_color': colors_available[0],
                'colors_available': colors_available,
                'first_size': sizes_available[0],
                'sizes_available': sizes_available,
                'description': product.description,
                'has_discount': product.has_discount,
                'is_new': product.is_new,
                'discounted_percent': product.discounted_percent,
                'slashed_price': round(slashed_price, 2),
                'saved_amount': round(product.price - slashed_price, 2),
            }

            already_viewed_count = RecentlyViewedProduct.objects.filter(product=product,
                                                                        session_key=request.session.session_key).count()
            if already_viewed_count == 0:
                new_recently_viewed_product = RecentlyViewedProduct(session_key=request.session.session_key,
                                                                    product=product)
                new_recently_viewed_product.save()

            recently_viewed_items = []

            for viewed_product in RecentlyViewedProduct.objects.filter(session_key=request.session.session_key).all():
                item = {
                    'name': viewed_product.product.name,
                    'short_name': viewed_product.product.get_short_name(),
                    'first_image': viewed_product.product.productimage_set.all()[0].file,
                    'second_image': viewed_product.product.productimage_set.all()[1].file,
                    'has_discount': viewed_product.product.has_discount,
                    'is_new': viewed_product.product.is_new,
                    'discounted_percent': viewed_product.product.discounted_percent,
                }

                recently_viewed_items.append(item)

            data = {
                'product_data': product_data,
                'recently_viewed_items': recently_viewed_items,
                'suggested_products': suggested_products,
                'reviews': reviews,
                'total_reviews': total_reviews,
                'has_reviews': True if review_count != 0 else False,
                'review_count': review_count
            }
            return render(request, 'products/product_detail.html', data)
    raise Http404


@login_required(login_url='/auth/login/')
def cart(request):
    cart_items = get_all_cart_items(request.user)
    subtotal = round(sum(item['total_price'] for item in cart_items), 2)
    return render(request, 'products/cart.html', {'cart_items': cart_items, 'subtotal': subtotal})


@login_required(login_url='/auth/login/')
def wishlist(request):
    all_wishlist_items = Wishlist.objects.filter(user=request.user).all()
    wishlist_items = []

    for item in all_wishlist_items:
        if item.product.has_discount:
            price = round(item.product.price - round(item.product.price * (item.product.discounted_percent / 100)), 2)
        else:
            price = round(item.product.price, 2)

        data = {
            'pk': item.id,
            'name': item.product.name,
            'image': item.product.productimage_set.all()[0].file,
            'short_name': item.product.get_short_name(),
            'price': price,
            'stock': 'out of stock' if item.product.in_stock == 0 else 'in stock',
        }
        wishlist_items.append(data)
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})


@login_required(login_url='/auth/login/')
def checkout(request):
    cart_items = get_all_cart_items(request.user)
    subtotal = sum(item['total_price'] for item in cart_items)
    shipping_fee = round(subtotal * 0.12)
    sum_total = subtotal + shipping_fee

    data = {'cart_items': cart_items, 'subtotal': subtotal, 'shipping_fee': shipping_fee, 'sum_total': sum_total}
    return render(request, 'products/checkout.html', data)


def orders(request):
    all_orders = request.user.orders_set.all()
    order_items = []

    if all_orders:
        for order in all_orders:
            all_order_items = order.orderitems_set.all()
            for order_item in all_order_items:
                item = {
                    'name': order_item.product.name,
                    'image': order_item.product.productimage_set.all()[0].file,
                    'short_name': order_item.product.get_short_name(),
                    'price': order_item.product.price,
                    'status': order.status,
                }
                order_items.append(item)
    return render(request, 'products/orders.html', {'order_items': order_items})


def order_complete(request):
    return render(request, 'products/order_complete.html')
