from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import connection
from django.http import JsonResponse
from cart.views import cart
from home.views import get_table


home_page = 'http://127.0.0.1:8000/'
cursor = connection.cursor()

def manage_offers(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    if request.session['customer_id'] == 1 :
        context = {
            'customer_id': request.session['customer_id'],
            'cart_price': cart.total_cost
        }
        return render(request, 'manage_offers.html', context)

def create_flash_sale(request):
    product_id = str(request.POST.get("products"))
    percent_off = str(request.POST.get("percent_off"))

    percent_off = int(percent_off)

    sql = 'SELECT MAX(SALE_ID) FROM FLASH_SALE'
    cursor.execute(sql)
    result = cursor.fetchall()
    max_sale_id = int(result[0][0])

    sql = '''
            INSERT INTO FLASH_SALE
            (SALE_ID,PRODUCT_ID,PERCENT_DISCOUNT,START_DATE,AVAILABILITY)
            VALUES
            (%s,%s,%s,SYSDATE,'Y')
    '''
    cursor.execute(sql, [max_sale_id+1, product_id, percent_off])

    return redirect("http://127.0.0.1:8000/manage_offers/")

def sale_list(request):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    sql = "SELECT P.PRODUCT_ID,"
    table = get_table(sql)
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }

    return render(request, 'sale_list.html',context)
