import json

from django.shortcuts import render
from products.reuseable_functions import get_on_sale_products, get_best_selling_products, get_newly_arrived_products, \
    get_products_based_on_category


def home(request):
    best_selling_products = get_best_selling_products()[:10]
    on_sale_products = get_on_sale_products()[:10]
    new_arriving_products = get_newly_arrived_products()[:10]

    data = {
        'best_selling_products': best_selling_products,
        'on_sale_products': on_sale_products,
        'new_arriving_products': new_arriving_products,
        'home': True
    }

    return render(request, 'main/home.html', data)


def search(request):
    search_query = request.GET.get('query')
    categories = ['clothing', 'cosmetics', 'bags', 'shoes', 'accessories', 'jewellery']
    print(search_query)

    if search_query in categories:
        results = get_products_based_on_category(search_query)

    return render(request, 'main/search.html', {'search': search_query, 'results': results})
