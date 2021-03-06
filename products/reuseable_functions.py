import json
import random
from datetime import datetime

from .models import Product, Cart, ProductReview


def get_best_selling_products(include_out_of_stock=False, order='descending'):
    """This is also for the popular products"""

    if order == 'ascending':
        sorting_text = 'sales_count'
    elif order == 'descending':
        sorting_text = '-sales_count'

    all_shop_products = Product.objects.all().order_by(sorting_text)
    returned_list = []

    for product in all_shop_products:
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
            'total_reviews': get_all_product_reviews_ratings(product),
            'has_reviews': True if len(get_all_product_reviews(product)) != 0 else False
        }
        if include_out_of_stock is False:
            if item['out_of_stock'] is False:
                returned_list.append(item)
        else:
            returned_list.append(item)

    return returned_list


def get_newly_arrived_products(include_out_of_stock=False):
    all_shop_products = Product.objects.filter(is_new=True).all()
    returned_list = []

    for product in all_shop_products:
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
            'total_reviews': get_all_product_reviews_ratings(product),
            'has_reviews': True if len(get_all_product_reviews(product)) != 0 else False
        }
        if include_out_of_stock is False:
            if item['out_of_stock'] is False:
                returned_list.append(item)
        else:
            returned_list.append(item)

    return returned_list


def get_on_sale_products(include_out_of_stock=False):
    all_shop_products = Product.objects.filter(has_discount=True).all()
    returned_list = []

    for product in all_shop_products:
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
            'total_reviews': get_all_product_reviews_ratings(product),
            'has_reviews': True if len(get_all_product_reviews(product)) != 0 else False
        }
        if include_out_of_stock is False:
            if item['out_of_stock'] is False:
                returned_list.append(item)
        else:
            returned_list.append(item)

    return returned_list


def get_all_products(include_out_of_stock=False):
    all_shop_products = Product.objects.all()
    returned_list = []

    for product in all_shop_products:
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
            'total_reviews': get_all_product_reviews_ratings(product),
            'has_reviews': True if len(get_all_product_reviews(product)) != 0 else False
        }
        if include_out_of_stock is False:
            if item['out_of_stock'] is False:
                returned_list.append(item)
        else:
            returned_list.append(item)

    return returned_list


def get_products_based_on_category(category):
    """This is for collections/categories... would've been best to use the same naming convention tho"""
    all_shop_products = Product.objects.filter(category=category).all()
    returned_list = []

    if all_shop_products is None:
        return []

    for product in all_shop_products:
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
            'total_reviews': get_all_product_reviews_ratings(product),
            'has_reviews': True if len(get_all_product_reviews(product)) != 0 else False
        }
        if item['out_of_stock'] is False:
            returned_list.append(item)

    return returned_list


def get_all_cart_items(user):
    cart_items = Cart.objects.filter(user=user).all()
    returned_list = []

    if cart_items is None:
        return []

    for item in cart_items:
        if item.product.has_discount:
            price = item.product.price - round(item.product.price * (item.product.discounted_percent / 100))
        else:
            price = item.product.price

        item_data = {
            "pk": item.id,
            "name": item.product.name,
            "short_name": item.product.get_short_name(),
            "image": str(item.product.productimage_set.all()[0].file),
            "color": item.color,
            "size": item.size,
            "price": round(price, 2),
            "total_price": round(price * item.quantity, 2),
            "quantity": item.quantity,
        }
        returned_list.append(item_data)

    return returned_list


def get_suggested_products(session_key):
    random.seed(session_key)
    returned_list = []

    products = get_all_products(include_out_of_stock=False)
    for i in range(12):
        random_product = random.choice(products)
        if random_product not in returned_list:
            returned_list.append(random_product)

    return returned_list


def update_cart_item_quantity(cart_item_id, new_quantity):
    cart_item = Cart.objects.filter(id=cart_item_id).first()
    cart_item.quantity = new_quantity
    cart_item.save()
    return


def clear_cart_data(user):
    Cart.objects.filter(user=user).delete()
    return


def get_all_product_reviews(product):
    all_reviews = ProductReview.objects.filter(product=product).all()
    returned_list = []

    if not all_reviews:
        return []

    for review in all_reviews:
        ratings = []
        for i in range(1, 6):
            if i <= review.rating:
                ratings.append(True)
            else:
                ratings.append(False)

        item = {
            'name': review.name,
            'title': review.title,
            'date': datetime.strftime(review.review_date, '%d %B %Y'),
            'body': review.body,
            'rating': ratings,
            'star_count': review.rating
        }
        returned_list.append(item)

    return returned_list


def get_all_product_reviews_ratings(product):
    """
    This is to get all the reviews and process them to get the rating for the product as a whole.
    This will return a list of 5 boolean values. They represent the 5 product review stars. When looping through
    the list, if the value is True, it means that's a full star (good reviews). if its false it means the star is empty
    (bad reviews)

    :param product:
    :return: list
    """
    all_reviews = get_all_product_reviews(product)
    total_product_rating = 0
    total_product_rating_bool = []  # this list contains the 'True/False for each star

    if not all_reviews:
        # if there are no reviews then all the stars will be empty
        return [False, False, False, False, False]

    count_interval = len(all_reviews)
    total_review_count = sum(i['star_count'] for i in all_reviews)
    max_review_count = len(all_reviews) * 5

    prev_count = 1
    review_count = 1

    for current_index in range(1, max_review_count, count_interval):
        if prev_count <= total_review_count <= current_index:
            total_product_rating = review_count
            break
        review_count += 1

    for i in range(1, 6):
        if i <= total_product_rating:
            total_product_rating_bool.append(True)
        else:
            total_product_rating_bool.append(False)

    return total_product_rating_bool

