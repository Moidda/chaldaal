from django.shortcuts import render, redirect
from cart.views import cart


home_page = 'http://127.0.0.1:8000/'


def bundleOffer(request):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return redirect(home_page)
    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'bundle-offer.html', context)
