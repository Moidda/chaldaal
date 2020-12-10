from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from cart.views import cart
from django.db import connection

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

    bundle_name = 'mehedi_dibe'
    total_cost = 1000
    product = []

    sql = 'SELECT NVL(MAX(BUNDLE_ID),0) FROM BUNDLE_OFFER'
    cursor.execute(sql)
    result = cursor.fetchall()
    bundle_id = int(result[0][0]) + 1

    sql = '''INSERT INTO BUNDLE_OFFER(BUNDLE_ID,BUNDLE_NAME,COST)
            VALUES (%s,%s,%s)'''
    cursor.execute(sql,[bundle_id,bundle_name,total_cost])

    for i in product:

        sql = '''INSERT INTO PRODUCTS_IN_BUNDLE_OFFER(BUNDLE_ID,PRODUCT_ID)
                VALUES(%s,%s)
        '''
        cursor.execute(sql,[bundle_id,product[i]])


def bundle_list(request):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)
    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost,
        'bundle': [
            {'bundle_id': 1, 'bundle_name': 'Bundle 1', 'bundle_cost': 320},
            {'bundle_id': 2, 'bundle_name': 'Bundle 2', 'bundle_cost': 430}
        ]
    }
    return render(request, 'bundle-list.html', context)


def bundle_end(request, bundle_id):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)

    print("--------------------------------------------------------------------------------------------------")
    print("Delete bundle offer with id = " + str(bundle_id) + " from database")
    print("--------------------------------------------------------------------------------------------------")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

