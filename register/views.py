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

        #validity checking
        error_context = {}
        error_context['try_again_link'] = 'http://127.0.0.1:8000/sign_up/'
        if customer_name == '':
            error_context['error_message'] = 'Please provide a name'
            return render(request, 'error.html', error_context)
        if street_no == '':
            error_context['error_message'] = 'Please provide a Street NO'
            return render(request, 'error.html', error_context)
        if house_no == '':
            error_context['error_message'] = 'Please provide a house no'
            return render(request, 'error.html', error_context)
        if apt_no == '':
            error_context['error_message'] = '''
                Please provide an apt no.\n
                If you can't provide an apt no, type in 'default'.
            '''
            return render(request, 'error.html', error_context)
        if email == '':
            error_context['error_message'] = 'Please provide an email'
            return render(request, 'error.html', error_context)
        if password1 == '':
            error_context['error_message'] = 'Please provide a password'
            return render(request, 'error.html', error_context)
        if password1 != password2:
            error_context['error_message'] = 'Could not confirm password'
            return render(request, 'error.html', error_context)

        # retrieve all email from customer table
        cursor = connection.cursor()
        sql = 'SELECT EMAIL FROM CUSTOMER'
        cursor.execute(sql)
        result = cursor.fetchall()

        # check if email is already in use by another customer
        for row in result:
            customer_email_in_db = row[0]
            if email == customer_email_in_db:
                error_context['error_message'] = 'Email already in use'
                return render(request, 'error.html', error_context)

        # creating a unique id for the new customer (max_id + 1)
        # this portion is probably redundant and can be handled in a better
        # way using oracle itself
        sql = 'SELECT MAX(CUSTOMER_ID) FROM CUSTOMER'
        cursor.execute(sql)
        result = cursor.fetchall()
        max_id = int(result[0][0])
        new_id = max_id+1

        # inserting into database the information of the new user
        sql = '''
            INSERT INTO CUSTOMER
            (CUSTOMER_ID, CUSTOMER_NAME, STREET_NO, HOUSE_NO, APT_NO, EMAIL, CUSTOMER_CREDIT, PASSWORD)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(sql, [new_id, customer_name, street_no, house_no, apt_no, email, 0, password1])

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
