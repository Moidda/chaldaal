from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from cart.views import cart
from django.db import connection
import json


home_page = 'http://127.0.0.1:8000/'

cursor = connection.cursor()

def bundleOffer(request):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)
    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'bundle-offer.html', context)


def create_bundle_offer(request):
    if'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)

    bundle_name = request.GET.get('bundle_name')
    total_cost = int(request.GET.get('bundle_cost'))
    product = request.GET.getlist('product_list[]', None)

    sql = 'SELECT NVL(MAX(PRODUCT_ID),0) FROM PRODUCT'
    cursor.execute(sql)
    result = cursor.fetchall()
    bundle_id = int(result[0][0]) + 1

    sql = '''INSERT INTO BUNDLE_OFFER(BUNDLE_ID,BUNDLE_NAME,COST)
            VALUES (%s,%s,%s)'''
    cursor.execute(sql, [bundle_id, bundle_name, total_cost])

    for i in range(0, len(product), 2):
        sql = '''INSERT INTO PRODUCTS_IN_BUNDLE_OFFER(BUNDLE_ID,PRODUCT_ID,QUANTITY)
                VALUES(%s,%s,%s)
        '''
        product_id = product[i]
        product_amount = product[i+1]
        cursor.execute(sql, [bundle_id, product_id, product_amount])

    return JsonResponse({})


def bundle_list(request):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)

    sql = 'SELECT * FROM BUNDLE_OFFER'
    cursor.execute(sql)
    result = cursor.fetchall()
    bundle = []

    for row in result:
        bundle_id = row[0]
        bundle_name = row[1]
        bundle_cost = row[2]
        dictionary = {
            'bundle_id': bundle_id,
            'bundle_name': bundle_name,
            'bundle_cost': bundle_cost
        }
        bundle.append(dictionary)

    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost,
        'bundle': bundle
    }
    return render(request, 'bundle-list.html', context)


def bundle_end(request, bundle_id):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)

    sql = 'DELETE FROM BUNDLE_OFFER WHERE BUNDLE_ID = %s'
    cursor.execute(sql, [bundle_id])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

