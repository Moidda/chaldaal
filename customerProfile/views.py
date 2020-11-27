from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.shortcuts import redirect

cursor = connection.cursor()
home_page = 'http://127.0.0.1:8000/'


# loads the profile page, retrieving info from DB
def customer_profile(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    context = {
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

    return render(request, 'profile_index.html', context)


# retrieves from profile Form/page, saves changes in DB
# reloads the page
def save_changes(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    if request.method == 'POST':
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

        cursor.callproc('UPDATE_CUSTOMER_INFO', [request.session['customer_id'], customer_name, email, street_no, house_no, apt_no])
        cursor.callproc('UPDATE_CUSTOMER_PAYMENT_INFO', [request.session['customer_id'], bank, username, card_type, card_no, bkash_phone_no])

        return redirect('/')

