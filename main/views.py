import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from main.models import NewsletterSubscriber
from products.models import Product
from products.reuseable_functions import get_on_sale_products, get_best_selling_products, get_newly_arrived_products, \
    get_products_based_on_category, get_suggested_products


def home(request):
    best_selling_products = get_best_selling_products()[:10]
    on_sale_products = get_on_sale_products()[:10]
    new_arriving_products = get_newly_arrived_products()[:10]
    suggested_products = get_suggested_products(request.session.session_key)

    data = {
        'best_selling_products': best_selling_products,
        'on_sale_products': on_sale_products,
        'new_arriving_products': new_arriving_products,
        'suggested_products': suggested_products,
        'home': True
    }

    return render(request, 'main/home.html', data)


def search(request):
    search_query = request.GET.get('query')
    categories = ['clothing', 'cosmetics', 'bags', 'shoes', 'accessories', 'jewellery']

    if search_query in categories:
        results = get_products_based_on_category(search_query)
    else:
        all_product_results = Product.objects.filter(name__icontains=search_query).all()
        results = []

        if all_product_results is not None:
            for product in all_product_results:
                item = {
                    'pk': product.id,
                    'name': product.name,
                    'short_name': product.get_short_name(),
                    'price': product.price,
                    'in_stock': product.in_stock,
                    'category': product.category,
                    'out_of_stock': True if product.in_stock == 0 else False,
                    'colors_available': json.loads(str(product.colors_available).strip("' ").replace('\'', '\"')),
                    'sizes_available': json.loads(str(product.sizes_available).strip("' ").replace('\'', '\"')),
                    'description': product.description,
                    'has_discount': product.has_discount,
                    'is_new': product.is_new,
                    'discounted_percent': product.discounted_percent,
                    'slashed_price': product.price - round(product.price * (product.discounted_percent / 100)),
                    'sales_count': product.sales_count,
                    'image1': product.productimage_set.all()[0].file,
                    'image2': product.productimage_set.all()[1].file,
                }
                if item['out_of_stock'] is False:
                    results.append(item)

    return render(request, 'main/search.html', {'search': search_query, 'results': results})


def subscribe_to_newsletter(request):
    email = request.POST.get('email')
    return_url = request.GET.get('return_url')

    old_subscriber = NewsletterSubscriber.objects.filter(email=email).first()
    if old_subscriber is None:
        new_subscriber = NewsletterSubscriber(email=email)
        new_subscriber.save()

        messages.success(request, 'Thank you for subscribing to our newsletter')
        return HttpResponseRedirect(return_url)

    messages.error(request, 'You have already subscribed')
    return HttpResponseRedirect(return_url)
