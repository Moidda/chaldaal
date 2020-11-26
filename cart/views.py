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


# if cart is empty, then load bag.html
# else load list of products in cart
def index(request):
    if 'email' not in request.session:
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

    return render(request, 'index.html', {'product': table, 'total_price': cart.total_cost})
    # return render(request, 'bag.html')


# loads the check out form page with customer information retrieved from
# customer profile
def checkout(request):
    if 'email' not in request.session:
        return redirect(home_page)
    context = {
        'customer_name': request.session['customer_name'],
        'email': request.session['email'],
        'street_no': request.session['street_no'],
        'house_no': request.session['house_no'],
        'apt_no': request.session['apt_no'],
        'username': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['email'], 'USERNAME']),
        'bank': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['email'], 'BANK']),
        'card_type': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['email'], 'CARD_TYPE']),
        'card_no': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['email'], 'CARD_NO']),
        'bkash_phone_no': cursor.callfunc('GET_BKASH', str, [request.session['email'], 'PHONE_NO'])
    }
    return render(request, 'checkout.html', context)


# places the ordar and updates the db tables
# is called upon checkout form submission
def confirm_checkout(request):
    if 'email' not in request.session:
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
    cursor.callproc('CONFIRM_ORDAR', [ordar_no, request.session['customer_id']])
    cursor.callproc('CONFIRM_PAYMENT', [ordar_no, request.session['customer_id'], cart.total_cost])

    for pid in cart.products:
        cnt = cart.products[pid]
        cursor.callproc('INSERT_PRODUCTS_IN_ORDAR', [ordar_no, pid, cnt])

    if paymentMethod == 'credit_card':
        cursor.callproc('CONFIRM_CREDIT_CARD', [ordar_no, request.session['customer_id'], username, bank, card_type, card_no])
    elif paymentMethod == 'bkash':
        tid = '123k34k'
        cursor.callproc('CONFIRM_BKASH', [ordar_no, request.sessionp['customer_id'], tid, bkash_phone_no])
    # else:

    return redirect(home_page)

