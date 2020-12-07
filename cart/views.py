# THIS IS THE AJAXIFY BRANCH UwU

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
# redirects to the previous page (the page/address it came from)
def add_item(request, product_id):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    units_in_stock = (cursor.execute('SELECT UNITS_IN_STOCK FROM PRODUCT WHERE PRODUCT_ID = %s', [product_id]).fetchall())[0][0]
    if units_in_stock:
        cart.add_product(product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# increase an item from the cart page
# reloads the cart page
def increase_item(request, product_id):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    units_in_stock = (cursor.execute('SELECT UNITS_IN_STOCK FROM PRODUCT WHERE PRODUCT_ID = %s', [product_id]).fetchall())[0][0]
    if units_in_stock:
        cart.add_product(product_id)
    return redirect('http://127.0.0.1:8000/cart/')


# decrease an item from the cart page
# reloads the cart page
def decrease_item(request, product_id):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    cart.remove_product(product_id)
    return redirect('http://127.0.0.1:8000/cart/')


# erases a product from the cart
# reloads the cart page
def erase_item(request, product_id):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    cart.erase_product(product_id)
    return redirect('http://127.0.0.1:8000/cart/')


# if cart is empty, then load bag.html
# else load list of products in cart
def index(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    table = []
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

    if cart.is_empty():
        return render(request, 'bag.html')
    context = {
        'customer_id': request.session['customer_id'],
        'product': table,
        'total_price': cart.total_cost,
        'cart_price': cart.total_cost
    }
    return render(request, 'index.html', context)
