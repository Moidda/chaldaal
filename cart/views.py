from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.shortcuts import redirect
from . import models


home_page = 'http://127.0.0.1:8000'
cart = models.Cart()
cursor = connection.cursor()


# when user adds an item in the cart from the home page
# the url 'cart/add_item/<product_id>' is called from home_page.html
def add_item(request, product_id):
    if 'email' not in request.session:
        return redirect(home_page)

    cart.add_product(product_id)
    for p, c in cart.products.items():
        print("Cart has " + str(c) + " no of " + str(p))
    return redirect(home_page)


# increase an item from the cart page
def increase_item(request, product_id):
    if 'email' not in request.session:
        return redirect(home_page)

    cart.add_product(product_id)
    return redirect('http://127.0.0.1:8000/cart/')


# decrease an item from the cart page
def decrease_item(request, product_id):
    if 'email' not in request.session:
        return redirect(home_page)

    cart.remove_product(product_id)
    return redirect('http://127.0.0.1:8000/cart/')


# erases a product from the cart
def erase_item(request, product_id):
    if 'email' not in request.session:
        return redirect(home_page)
    cart.erase_product(product_id)
    return redirect('http://127.0.0.1:8000/cart/')


def index(request):
    if 'email' not in request.session:
        return redirect(home_page)

    table = []
    total_price = 0
    for product_id, amount in cart.products.items():
        sql = 'SELECT * FROM PRODUCT WHERE PRODUCT_ID = %s'
        cursor.execute(sql, [product_id])
        result = cursor.fetchone()
        product_name = result[1]
        unit = result[2]
        price_per_unit = result[4]
        category = result[5]
        sub_category = result[6]
        rating_by_customer = result[7]
        table.append({
            'product_id': product_id,
            'product_name': product_name,
            'unit': unit,
            'price_per_unit': price_per_unit,
            'category': category,
            'sub_category': sub_category,
            'rating_by_customer': rating_by_customer,
            'amount': amount,
            'to_pay': price_per_unit*amount
        })
        total_price += amount*price_per_unit

    return render(request, 'index.html', {'product': table, 'total_price': total_price})


def checkout(request):
    if 'email' not in request.session:
        return redirect(home_page)
    return render(request, 'checkout.html')


def confirm_checkout(request):
    return HttpResponse("Your order has been placed")

