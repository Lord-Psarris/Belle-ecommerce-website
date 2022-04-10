import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from main.models import NewsletterSubscriber
from products.reuseable_functions import *


def home(request):
    # getting products for homepage sections
    best_selling_products = get_best_selling_products()[:10]
    on_sale_products = get_on_sale_products()[:10]
    new_arriving_products = get_newly_arrived_products()[:10]

    # if a user isn't logged in, there is no session key. So for non-logged-in users a session key is created
    # for the recently viewed model
    if not request.session.exists(request.session.session_key):
        request.session.create()

    suggested_products = get_suggested_products(request.session.session_key)

    data = {
        'best_selling_products': best_selling_products,
        'on_sale_products': on_sale_products,
        'new_arriving_products': new_arriving_products,
        'suggested_products': suggested_products,
        'home': True  # this is needed to set the classic header class in base.html
    }

    return render(request, 'main/home.html', data)


def search(request):
    """
    When a user enters a query, first check if that query matches any of the sites categories
    If so, the return products that belong to that category. Otherwise return products that match
    the query

    :param request:
    :return: HttpResponse
    """
    search_query = request.GET.get('query')
    categories = ['clothing', 'cosmetics', 'bags', 'shoes', 'accessories', 'jewellery']

    if search_query.lower() in categories:
        results = get_products_based_on_category(search_query)
    else:
        all_product_results = Product.objects.filter(name__icontains=search_query).all()
        results = []

        if all_product_results is not None:
            for product in all_product_results:

                # sorting data for the frontend
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


def blog(request):
    if request.POST:
        email = request.POST['email']

        old_subscriber = NewsletterSubscriber.objects.filter(email=email).first()
        if old_subscriber is None:
            new_subscriber = NewsletterSubscriber(email=email)
            new_subscriber.save()

            messages.success(request, 'Thank you for subscribing to our newsletter')
            return HttpResponseRedirect(reverse('main:blog'))

        messages.error(request, 'You have already subscribed')
        return HttpResponseRedirect(reverse('main:blog'))

    return render(request, 'main/coming_soon.html')


def contact(request):
    """
    When a user sends a contact form, the data could be added to an email queue on a backend service
    like celery or apscheduler. Or simply just added to the database for the admin to read

    :param request:
    :return: HttpResponse
    """
    if request.POST:
        data = request.POST
        # process contact form data

        messages.success(request, 'thank you, your message has been sent')
        return HttpResponseRedirect(reverse('main:contact'))
    return render(request, 'main/contact.html')


def faq(request):
    return render(request, 'main/faqs.html')


def about(request):
    return render(request, 'main/about.html')
