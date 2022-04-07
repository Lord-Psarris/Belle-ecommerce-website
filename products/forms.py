import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from products.models import Product, Cart, Wishlist, Orders, OrderItems
from products.reuseable_functions import update_cart_item_quantity, clear_cart_data, get_all_cart_items


def add_to_cart(request):
    return_url = request.GET.get('return_url')
    if not request.user.is_authenticated:
        messages.success(request, 'You have to login to add to your cart')
        return HttpResponseRedirect(return_url)

    data = request.POST.copy()

    product = Product.objects.filter(pk=data['pk']).first()
    user = request.user

    old_cart_item = Cart.objects.filter(product=product, user=user).first()
    if old_cart_item is not None:
        messages.success(request, 'Item is already in cart')
        return HttpResponseRedirect(return_url)

    if data.get('size') is None:
        data['size'] = json.loads(str(product.sizes_available).strip("' ").replace('\'', '\"'))[0]

    if data.get('color') is None:
        data['color'] = json.loads(str(product.colors_available).strip("' ").replace('\'', '\"'))[0]

    if data.get('quantity') is None:
        data['quantity'] = 1

    new_cart_item = Cart(user=user, product=product, color=data['color'], size=data['size'], quantity=data['quantity'])
    new_cart_item.save()
    return HttpResponseRedirect(reverse('products:cart'))


def get_number_of_cart_items(request):
    if request.user.is_authenticated:
        cart_items_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({'count': cart_items_count}, status=200)
    return JsonResponse({'count': 0}, status=200)


def update_cart_data(request):
    data = request.POST

    for cart_item_id, quantity in data.items():
        if cart_item_id != 'csrfmiddlewaretoken' and cart_item_id != 'update':
            cart_item_id = cart_item_id.replace('cart_item-', '')
            new_quantity = quantity

            update_cart_item_quantity(cart_item_id, new_quantity)

    messages.success(request, 'Updated items')
    return HttpResponseRedirect(reverse('products:cart'))


def clear_cart_items(request):
    clear_cart_data(request.user)

    return HttpResponseRedirect(reverse('products:cart'))


def get_cart_items(request):
    if request.user.is_authenticated:
        cart_items = get_all_cart_items(request.user)
        return JsonResponse({'data': cart_items}, status=200)
    return JsonResponse({'data': []}, status=200)


def remove_item_from_cart(request):
    data = request.POST

    cart_item = Cart.objects.get(pk=data['pk'])
    cart_item.delete()

    messages.success(request, 'Removed item from cart')
    return JsonResponse({'data': 'Successful'}, status=200)


def add_to_wishlist(request):
    return_url = request.GET.get('return_url')
    if not request.user.is_authenticated:
        messages.success(request, 'You have to login to add to your wishlist')
        return HttpResponseRedirect(return_url)

    data = request.POST

    product = Product.objects.filter(pk=data['pk']).first()
    user = request.user

    old_wishlist_item = Wishlist.objects.filter(product=product, user=user).first()
    if old_wishlist_item is not None:
        messages.success(request, 'Item is already in your wishlist')
        return HttpResponseRedirect(return_url)

    new_wishlist_item = Wishlist(user=user, product=product)
    new_wishlist_item.save()

    return HttpResponseRedirect(reverse('products:wishlist'))


def remove_item_from_wishlist(request):
    data = request.POST

    wishlist_item = Wishlist.objects.get(pk=data['pk'])
    wishlist_item.delete()

    messages.success(request, 'Removed item from wishlist')
    return HttpResponseRedirect(reverse('products:wishlist'))


def use_coupon(request):
    messages.error(request, 'Invalid Discount Code')
    return HttpResponseRedirect(reverse('products:checkout'))


def process_checkout(request):
    data = request.POST
    cart_items = request.user.cart_set.all()
    print(data)

    if any(item == '' for key, item in data.items()):
        messages.error(request, 'Please fill in all required fields')
        return HttpResponseRedirect(reverse('products:checkout'))

    new_order = Orders(user=request.user, telephone=data['telephone'], address=data['address'], city=data['city'],
                       post_code=data['postcode'], state=data['state'], country=data['country'],
                       order_notes=data['order_notes'], total_price=data['total_price'])
    new_order.save()

    for item in cart_items:
        new_order_item = OrderItems(order=new_order, product=item.product)
        new_order_item.save()

    Cart.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(reverse('products:order_complete'))
