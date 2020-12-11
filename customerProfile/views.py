from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection
from django.shortcuts import redirect
from cart.views import cart


cursor = connection.cursor()
home_page = 'http://127.0.0.1:8000/'


# loads the profile page, retrieving info from DB
def customer_profile(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    context = {
        'customer_id': request.session['customer_id'],
        'customer_name': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'CUSTOMER_NAME']),
        'email': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'EMAIL']),
        'phone_no': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'PHONE_NO']),
        'street_no': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'STREET_NO']),
        'house_no': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'HOUSE_NO']),
        'apt_no': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'APT_NO']),
        'customer_credit': cursor.callfunc('GET_CUSTOMER', str, [request.session['customer_id'], 'CUSTOMER_CREDIT']),

        'username': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'USERNAME']),
        'bank': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'BANK']),
        'card_type': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'CARD_TYPE']),
        'card_no': cursor.callfunc('GET_CREDIT_CARD', str, [request.session['customer_id'], 'CARD_NO']),
        'bkash_phone_no': cursor.callfunc('GET_BKASH', str, [request.session['customer_id'], 'PHONE_NO']),

        'cart_price': cart.total_cost
    }
    for key in context:
        if not context[key]:
            context[key] = ''

    cursor.execute('SELECT EMAIL FROM CUSTOMER WHERE CUSTOMER_ID <> %s', [request.session['customer_id']])
    result = cursor.fetchall()
    db_emails = [lst[0] for lst in result]
    context['db_emails'] = db_emails

    cursor.execute('SELECT PHONE_NUMBER FROM CUSTOMER_PHONE WHERE CUSTOMER_ID <> %s', [request.session['customer_id']])
    result = cursor.fetchall()
    db_phone_nos = [lst[0] for lst in result]
    context['db_phone_nos'] = db_phone_nos

    return render(request, 'profile_index.html', context)


# - retrieves from profile Form/page,
# - saves changes in DB
# - reloads the page
def save_changes(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    if request.method == 'POST':
        customer_name = str(request.POST.get("customer_name"))
        email = str(request.POST.get("email"))
        phone_no = str(request.POST.get("phone_no"))
        street_no = str(request.POST.get("street_no"))
        house_no = str(request.POST.get("house_no"))
        apt_no = str(request.POST.get("apt_no"))
        username = str(request.POST.get("username"))
        bank = str(request.POST.get("bank"))
        card_type = str(request.POST.get("card_type"))
        card_no = str(request.POST.get("card_no"))
        bkash_phone_no = str(request.POST.get("bkash_phone_no"))

        cursor.callproc('UPDATE_CUSTOMER_INFO', [request.session['customer_id'], customer_name, email, phone_no, street_no, house_no, apt_no])
        cursor.callproc('UPDATE_CUSTOMER_PAYMENT_INFO', [request.session['customer_id'], username, bank, card_type, card_no, bkash_phone_no])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def customer_list(request):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)

    clist = []
    result = (cursor.execute('SELECT * FROM CUSTOMER')).fetchall()
    for r in result:
        clist.append({
            'customer_name': r[1],
            'street_no': r[2],
            'house_no': r[3],
            'apt_no': r[4],
            'email': r[5],
            'credit_card': cursor.callfunc('GET_CREDIT_CARD', str, [r[0], 'CARD_NO']),
            'bkash': cursor.callfunc('GET_BKASH', str, [r[0], 'PHONE_NO'])
        })

    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost,
        'customer_list': clist
    }
    return render(request, 'customer-list.html', context)
