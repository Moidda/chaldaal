from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.shortcuts import redirect
from . import models
from cart.views import cart


home_page = 'http://127.0.0.1:8000'
cursor = connection.cursor()


# loads the check out form page with customer information retrieved from
# customer profile
def checkout(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    context = {
        'customer_id': request.session['customer_id'],
        'customer_name': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'CUSTOMER_NAME']),
        'email': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'EMAIL']),
        'street_no': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'STREET_NO']),
        'house_no': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'HOUSE_NO']),
        'apt_no': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'APT_NO']),

        'username': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'USERNAME']),
        'bank': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'BANK']),
        'card_type': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'CARD_TYPE']),
        'card_no': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'CARD_NO']),
        'bkash_phone_no': cursor.callfunc('GET_BKASH', str, [request.session['customer_id'], 'PHONE_NO'])
    }
    for key in context:
        if not context[key]:
            context[key] = ''

    # cart_products should be a list
    # for each p in cart_products, we need
    # p.product_name, p.unit, p.cnt, p.price_per_unit, p.to_pay
    context['cart_products'] = []
    for pid, cnt in cart.products.items():
        sql = 'SELECT PRODUCT_NAME, PRICE_PER_UNIT, UNIT FROM PRODUCT WHERE PRODUCT_ID = %s'
        cursor.execute(sql, [pid])
        result = cursor.fetchone()
        product_name = result[0]
        price_per_unit = result[1]
        unit = result[2]
        context['cart_products'].append({
            'product_name': product_name,
            'unit': unit,
            'price_per_unit': price_per_unit,
            'cnt': cnt,
            'to_pay': cnt*price_per_unit
        })

    sql = 'SELECT CUSTOMER_CREDIT FROM CUSTOMER WHERE CUSTOMER_ID = %s'
    cursor.execute(sql, [request.session['customer_id']])
    result = cursor.fetchall()
    customer_credit = result[0][0]
    context['points'] = customer_credit

    if 'point' in request.session:
        context['used_points'] = 2*request.session['point']
    else:
        context['used_points'] = 0

    context['total_cost'] = cart.total_cost - context['used_points']
    context['cart_price'] = cart.total_cost

    return render(request, 'checkout.html', context)


# places the order and updates the db tables
# is called upon checkout form submission
# redirects to product rating page
def confirm_checkout(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    customer_name = str(request.POST.get("customer_name"))
    email = str(request.POST.get("email"))
    street_no = str(request.POST.get("street_no"))
    house_no = str(request.POST.get("house_no"))
    apt_no = str(request.POST.get("apt_no"))
    username = str(request.POST.get("username"))
    bank = str(request.POST.get("bank"))
    card_type = str(request.POST.get("card_type"))
    card_no = str(request.POST.get("card_no"))
    bkash_phone_no = str(request.POST.get("bkash_phone_no"))
    paymentMethod = str(request.POST.get("paymentMethod"))

    ordar_no = (cursor.execute('SELECT MAX(ORDAR_NO) FROM ORDAR').fetchall())[0][0] + 1

    used_bonus = 0
    if 'point' in request.session:
        used_bonus = 2*request.session['point']

    cart.total_cost -= used_bonus

    cursor.callproc('CONFIRM_ORDAR', [ordar_no, request.session['customer_id']])
    cursor.callproc('CONFIRM_PAYMENT', [ordar_no, request.session['customer_id'], cart.total_cost])
    for pid in cart.products:
        cnt = cart.products[pid]
        cursor.callproc('INSERT_PRODUCTS_IN_ORDAR', [ordar_no, pid, cnt])

    if paymentMethod == 'credit_card':
        cursor.callproc('CONFIRM_CREDIT_CARD', [ordar_no, request.session['customer_id'], username, bank, card_type, card_no])
    elif paymentMethod == 'bkash':
        transaction_id = '123987'
        cursor.callproc('CONFIRM_BKASH', [ordar_no, request.session['customer_id'], transaction_id, bkash_phone_no])

    sql = 'UPDATE CUSTOMER SET CUSTOMER_CREDIT = CUSTOMER_CREDIT - %s WHERE CUSTOMER_ID = %s'
    cursor.execute(sql, [used_bonus, request.session['customer_id']])

    if 'point' in request.session:
        request.session['point'] = 0

    return redirect('http://127.0.0.1:8000/rate/')


# is called on click 'REDEEM' from checkout page
# checks validity of the amount of credit point customer
# is attempting to redeem, recalculates the total cost of cart accordingly
# reloads the check out form page
def using_points(request):
    point = str(request.POST.get('using_points'))
    point = int(point)

    sql = 'SELECT CUSTOMER_CREDIT FROM CUSTOMER WHERE CUSTOMER_ID = %s'
    cursor.execute(sql, [request.session['customer_id']])
    result = cursor.fetchall()
    customer_credit = result[0][0]

    if point <= customer_credit and point >= 0:
        request.session['point'] = point

    return redirect("http://127.0.0.1:8000/checkout/")
