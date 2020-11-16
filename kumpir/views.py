from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import connection

home_page = 'http://127.0.0.1:8000/'


def manage_product(request):
    if 'email' in request.session and request.session['email'] == 'kumpir@yanak.com':
        return render(request, 'manage_product.html')
    return redirect(home_page)


def insert_product_sql(product_name, unit, units_in_stock, price_per_unit, category, sub_category):
    cursor = connection.cursor()
    sql = 'SELECT MAX(PRODUCT_ID) FROM PRODUCT'
    cursor.execute(sql)
    result = cursor.fetchall()
    max_id = int(result[0][0])

    sql = '''
        INSERT INTO PRODUCT
        (PRODUCT_ID, PRODUCT_NAME, UNIT, UNITS_IN_STOCK, PRICE_PER_UNIT, CATEGORY, SUB_CATEGORY, RATING_BY_CUSTOMER)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, [max_id + 1, product_name, unit, units_in_stock, price_per_unit, category, sub_category, 0])


def insert_product(request):
    if request.method == 'POST':
        product_name = str(request.POST.get('product_name'))
        unit = str(request.POST.get('unit'))
        units_in_stock = str(request.POST.get('units_in_stock'))
        price_per_unit = str(request.POST.get('price_per_unit'))
        category = str(request.POST.get('category'))
        sub_category = str(request.POST.get('sub_category'))

        insert_product_sql(product_name, unit, units_in_stock, price_per_unit, category, sub_category)

        return redirect('http://127.0.0.1:8000/manage_product/')

