from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.shortcuts import redirect

cursor = connection.cursor()
home_page = 'http://127.0.0.1:8000/'


def customer_profile(request):
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

    return render(request, 'profile_index.html', context)


def save_changes(request):
    if 'email' not in request.session:
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

        print(customer_name)
        print(email)
        print(street_no)
        print(house_no)
        print(apt_no)

        print(username)
        print(bank)
        print(card_type)
        print(card_no)

        print(bkash_phone_no)

        return redirect(home_page)

