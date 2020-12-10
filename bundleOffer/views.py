from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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
