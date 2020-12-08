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

    cursor.callproc('CHECKING_FLASH_SALE', [product_id, percent_off])

    return redirect("http://127.0.0.1:8000/manage_offers/")


def sale_list(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    sql = '''SELECT F.SALE_ID,
            P.PRODUCT_ID,
            P.PRODUCT_NAME,
            P.PRICE_PER_UNIT AS PREVIOUS_PRICE,
            F.PERCENT_DISCOUNT,
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
        percent_discount = row[4]
        discounted_price = previous_price - (previous_price * percent_discount //100)
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