from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import connection
from cart.views import cart


def sign_up(request):
    if 'customer_id' in request.session:
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'sign_up.html')


def log_in(request):
    if 'customer_id' in request.session:
        return redirect('http://127.0.0.1:8000/')
    return render(request, 'log_in.html')


def sign_up_verification(request):
    if request.method == 'POST':
        customer_name = str(request.POST.get("customer_name"))
        street_no = str(request.POST.get("street_no"))
        house_no = str(request.POST.get("house_no"))
        apt_no = str(request.POST.get("apt_no"))
        email = str(request.POST.get("email"))
        password1 = str(request.POST.get("password1"))
        password2 = str(request.POST.get("password2"))

        error_context = {}
        error_context['try_again_link'] = 'http://127.0.0.1:8000/sign_up/'
        cursor = connection.cursor()
        args = [customer_name, street_no, house_no, apt_no, email, password1, password2]
        error_context['error_message'] = cursor.callfunc("IS_VALID_SIGN_UP", str, args)

        if error_context['error_message'] != 'VALID':
            return render(request, 'error.html', error_context)

        cursor.callproc("CREATE_CUSTOMER", args)

        return redirect('http://127.0.0.1:8000/')


def get_customer_info_sql(user_email):
    cursor = connection.cursor()
    sql = 'SELECT * FROM CUSTOMER WHERE EMAIL LIKE %s'
    cursor.execute(sql, [user_email])
    ret = cursor.fetchall()
    cursor.close()
    return ret[0]


def create_session(request, result):
    request.session['customer_id'] = result[0]


def log_in_verification(request):
    if request.method == 'POST':
        user_email = str(request.POST.get("user_email"))
        user_pass = str(request.POST.get("user_pass"))

        cursor = connection.cursor()
        error_context = {}
        error_context['try_again_link'] = "http://127.0.0.1:8000/log_in/"
        error_context['error_message'] = cursor.callfunc("IS_VALID_LOG_IN", str, [user_email, user_pass])

        if error_context['error_message'] != 'VALID':
            return render(request, 'error.html', error_context)

        create_session(request, get_customer_info_sql(user_email))

        return redirect('http://127.0.0.1:8000/')


def log_out(request):
    request.session.clear()
    request.session.flush()
    cart.clear_cart()
    return redirect('http://127.0.0.1:8000/log_in/')
