from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import connection
from django.http import JsonResponse
from cart.views import cart


home_page = 'http://127.0.0.1:8000/'
cursor = connection.cursor()


def manage_offers(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    if request.session['customer_id'] == 1:
        context = {
            'customer_id': request.session['customer_id'],
            'cart_price': cart.total_cost
        }
        return render(request, 'manage_offers.html', context)


def create_flash_sale(request):
    product_id = str(request.POST.get("products"))
    percent_off = str(request.POST.get("percent_off"))

    percent_off = int(percent_off)

    sql = 'SELECT NVL(MAX(SALE_ID), 0) FROM FLASH_SALE'
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
        return redirect(home_page)

    sql = '''SELECT F.SALE_ID,
            P.PRODUCT_ID,
            P.PRODUCT_NAME,
            P.PRICE_PER_UNIT AS PREVIOUS_PRICE,
            (P.PRICE_PER_UNIT - P.PRICE_PER_UNIT * F.PERCENT_DISCOUNT/100) AS DISCOUNTED_PRICE,
            P.CATEGORY,
            P.SUB_CATEGORY
            FROM PRODUCT P,FLASH_SALE F
            WHERE P.PRODUCT_ID = F.PRODUCT_ID'''

    cursor.execute(sql)
    result = cursor.fetchall()
    table = []
    for row in result:
        sale_id = row[0]
        product_id = row[1]
        product_name = row[2]
        previous_price = row[3]
        discounted_price = row[4]
        category = row[5]
        sub_category = row[6]
        dictionary = {
            'flash_sale_id':sale_id,
            'flash_sale_product_id': product_id,
            'flash_sale_product_name': product_name,
            'flash_sale_previous_price': previous_price,
            'flash_sale_discounted_price': discounted_price,
            'flash_sale_category': category,
            'flash_sale_sub_category': sub_category
        }
        table.append(dictionary)

    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost,
        'flash_sale': table
    }

    return render(request, 'sale_list.html', context)


def end_sale(request,flash_sale_id):
    sql = '''
            DELETE FROM FLASH_SALE 
            WHERE SALE_ID = %s    
    '''
    cursor.execute(sql, [flash_sale_id])
    return redirect('http://127.0.0.1:8000/manage_offers/sale_list/')