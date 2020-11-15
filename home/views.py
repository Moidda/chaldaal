from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect

def home(request):
    if 'email' in request.session:
        customer_info = {}
        customer_info['customer_id'] = request.session['customer_id']
        customer_info['customer_name'] = request.session['customer_name']
        customer_info['street_no'] = request.session['street_no']
        customer_info['house_no'] = request.session['house_no']
        customer_info['apt_no'] = request.session['apt_no']
        customer_info['email'] = request.session['email']
        customer_info['customer_credit'] = request.session['customer_credit']
        customer_info['password'] = request.session['password']
        return render(request, 'home_page.html', customer_info)
    else:
        return redirect('http://127.0.0.1:8000/log_in')