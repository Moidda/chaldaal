from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from cart.views import cart
from . import models


cursor = connection.cursor()
home_page = 'http://127.0.0.1:8000/'
ratingSystem = models.RatingSystem()


def rating(request):
    if 'customer_id' not in request.session:
        redirect(home_page)

    lst = []
    for pid in ratingSystem.rating:
        product_name = (cursor.execute('SELECT PRODUCT_NAME FROM PRODUCT WHERE PRODUCT_ID = %s', [pid]).fetchall())[0][0]
        lst.append({
            'product_id': pid,
            'rating': ratingSystem.rating[pid],
            'product_name': product_name
        })

    context = {
        'product': lst,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'rating.html', context)


def increase_rating(request):
    pid = int(request.GET.get('product_id'))
    ratingSystem.increase_rating(pid)
    data = {'rating': ratingSystem.rating[pid]}
    return JsonResponse(data)


def decrease_rating(request):
    pid = int(request.GET.get('product_id'))
    ratingSystem.decrease_rating(pid)
    data = {'rating': ratingSystem.rating[pid]}
    return JsonResponse(data)


def save_rating(request):
    ratingSystem.save_rating()
    return redirect(home_page)


