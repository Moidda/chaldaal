from django.shortcuts import render, redirect
from cart.views import cart
from django.db import connection
from django.http import HttpResponse


cursor = connection.cursor()
home_page = 'http://127.0.0.1:8000/'


def rating(request):
    lst = []
    for pid in cart.products:
        product_name = (cursor.execute('SELECT PRODUCT_NAME FROM PRODUCT WHERE PRODUCT_ID = %s', [pid]).fetchall())[0][0]
        lst.append({
            'product_id': pid,
            'product_name': product_name,
            'rating': cart.rating[pid]
        })
    return render(request, 'rating.html', {'product': lst})


def increase_rating(request, pid):
    cart.increase_rating(product_id=pid)
    return redirect('http://127.0.0.1:8000/rate/')


def decrease_rating(request, pid):
    cart.decrease_rating(product_id=pid)
    return redirect('http://127.0.0.1:8000/rate/')


def save_rating(request):
    for pid in cart.rating:
        cursor.callproc('UPDATE_PRODUCT_RATING', [pid, cart.rating[pid]])
    cart.clear_cart()
    return redirect(home_page)

