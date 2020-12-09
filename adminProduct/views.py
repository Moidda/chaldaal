from django.shortcuts import render, redirect
from cart.views import cart
from django.http import JsonResponse, HttpResponseRedirect
from django.db import connection


cursor = connection.cursor()
home_page = 'http://127.0.0.1:8000/'


def edit_product(request, product_id):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)

    product_name = cursor.callfunc('GET_PRODUCT', str, [product_id, 'PRODUCT_NAME'])
    unit = cursor.callfunc('GET_PRODUCT', str, [product_id, 'UNIT'])
    units_in_stock = cursor.callfunc('GET_PRODUCT', int, [product_id, 'UNITS_IN_STOCK'])
    price_per_unit = cursor.callfunc('GET_PRODUCT', int, [product_id, 'PRICE_PER_UNIT'])
    category = cursor.callfunc('GET_PRODUCT', str, [product_id, 'CATEGORY'])
    sub_category = cursor.callfunc('GET_PRODUCT', str, [product_id, 'SUB_CATEGORY'])
    rating_by_customer = cursor.callfunc('GET_PRODUCT', int, [product_id, 'RATING_BY_CUSTOMER'])
    percent_discount = cursor.callfunc('GET_PRODUCT', str, [product_id, 'PERCENT_DISCOUNT'])
    discounted_price = ''
    if percent_discount:
        percent_discount = int(percent_discount)
        discounted_price = price_per_unit - (price_per_unit * percent_discount // 100)

    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost,
        'product_id': product_id,
        'product_name': product_name,
        'unit': unit,
        'units_in_stock': units_in_stock,
        'price_per_unit': price_per_unit,
        'category': category,
        'sub_category': sub_category,
        'rating_by_customer': rating_by_customer,
        'percent_discount': percent_discount,
        'discounted_price': discounted_price
    }
    return render(request, 'edit_product.html', context)


def save_changes(request, product_id):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1 or request.method != 'POST':
        return redirect(home_page)

    product_name = str(request.POST.get('product_name'))
    unit = str(request.POST.get('unit'))
    units_in_stock = str(request.POST.get('units_in_stock'))
    price_per_unit = str(request.POST.get('price_per_unit'))
    category = str(request.POST.get('category'))
    sub_category = str(request.POST.get('sub_category'))
    percent_discount = str(request.POST.get('percent_discount'))

    cursor.callproc('UPDATE_PRODUCT', [
        product_id, product_name, unit, units_in_stock, price_per_unit, category, sub_category])
    cursor.callproc('CHECKING_FLASH_SALE', [product_id, percent_discount])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))