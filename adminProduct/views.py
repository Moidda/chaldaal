from django.shortcuts import render, redirect
from cart.views import cart
from django.http import JsonResponse, HttpResponseRedirect
from django.db import connection


cursor = connection.cursor()
home_page = 'http://127.0.0.1:8000/'


def edit_product(request, product_id):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)

    product_name = (cursor.execute('SELECT PRODUCT_NAME FROM PRODUCT WHERE PRODUCT_ID=%s', [product_id])).fetchall()[0][0]
    unit = (cursor.execute('SELECT UNIT FROM PRODUCT WHERE PRODUCT_ID=%s', [product_id])).fetchall()[0][0]
    units_in_stock = (cursor.execute('SELECT UNITS_IN_STOCK FROM PRODUCT WHERE PRODUCT_ID=%s', [product_id])).fetchall()[0][0]
    price_per_unit = (cursor.execute('SELECT PRICE_PER_UNIT FROM PRODUCT WHERE PRODUCT_ID=%s', [product_id])).fetchall()[0][0]

    percent_off = None
    discounted_price = None
    cursor.execute('SELECT PERCENT_DISCOUNT FROM FLASH_SALE WHERE PRODUCT_ID=%s', [product_id])
    result = cursor.fetchall()
    if len(result):
        percent_off = result[0][0]
        discounted_price = price_per_unit*(100-percent_off) // 100

    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost,
        'product_id': product_id,
        'product_name': product_name,
        'unit': unit,
        'units_in_stock': units_in_stock,
        'price_per_unit': price_per_unit,
        'percent_off': percent_off,
        'discounted_price': discounted_price
    }
    return render(request, 'edit_product.html', context)


def save_changes(request, product_id):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1 or request.method != 'POST':
        return redirect(home_page)

    product_name = str(request.POST.get('product_name'))
    unit = str(request.POST.get('unit'))
    units_in_stock = str(request.POST.get('units_in_stock'))
    price_per_unit = int(str(request.POST.get('price_per_unit')))
    percent_off = int(str(request.POST.get('percent_off')))

    # update percent_off with a procedure

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))