from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import connection


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


def check_mail_sql(user_email):
    email_found = False
    cursor = connection.cursor()
    sql = 'SELECT EMAIL FROM CUSTOMER'
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        customer_email_in_db = row[0]
        if user_email == customer_email_in_db:
            email_found = True
    cursor.close()
    return email_found


def get_customer_pass_sql(user_email):
    cursor = connection.cursor()
    sql = '''
                SELECT PASSWORD
                FROM CUSTOMER
                WHERE EMAIL = %s
    '''
    cursor.execute(sql, [user_email])
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]


def get_customer_info_sql(user_email):
    cursor = connection.cursor()
    sql = 'SELECT * FROM CUSTOMER WHERE EMAIL LIKE %s'
    cursor.execute(sql, [user_email])
    ret = cursor.fetchall()
    cursor.close()
    return ret[0]


def create_session(request, result):
    request.session['customer_id'] = result[0]
    request.session['customer_name'] = result[1]
    request.session['street_no'] = result[2]
    request.session['house_no'] = result[3]
    request.session['apt_no'] = result[4]
    request.session['email'] = result[5]
    request.session['customer_credit'] = result[6]
    request.session['password'] = result[7]


def log_in_verification(request):
    if request.method == 'POST':
        response = redirect('http://127.0.0.1:8000/')

        # retrieve user input from web page
        user_email = str(request.POST.get("user_email"))
        user_pass = str(request.POST.get("user_pass"))

        if user_email == '':
            error_context = {}
            error_context['error_message'] = 'Please Enter your email'
            error_context['try_again_link'] = "http://127.0.0.1:8000/log_in/"
            return render(request, 'error.html', error_context)

        if user_pass == '':
            error_context = {}
            error_context['error_message'] = 'Incorrect Password'
            error_context['try_again_link'] = "http://127.0.0.1:8000/log_in/"
            return render(request, 'error.html', error_context)

        email_found = check_mail_sql(user_email)
        if not email_found:
            context = {}
            context['error_message'] = "Email not found"
            context['try_again_link'] = "http://127.0.0.1:8000/log_in/"
            return render(request, 'error.html', context)

        customer_pass_in_db = get_customer_pass_sql(user_email)
        if user_pass != customer_pass_in_db:
            context = {}
            context['error_message'] = "Incorrect Password"
            context['try_again_link'] = "http://127.0.0.1:8000/log_in/"
            return render(request, 'error.html', context)

        # set session here
        result = get_customer_info_sql(user_email)
        create_session(request, result)

        return response


def log_out(request):
    request.session.clear()
    request.session.flush()
    return redirect('http://127.0.0.1:8000/log_in/')
