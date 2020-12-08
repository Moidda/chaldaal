from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import connection
from django.http import JsonResponse
from cart.views import cart


home_page = 'http://127.0.0.1:8000/'
cursor = connection.cursor()


def manage_product(request):
    if 'customer_id' in request.session and request.session['customer_id'] == 1:
        context = {
            'customer_id': request.session['customer_id'],
            'cart_price': cart.total_cost
        }
        return render(request, 'manage_product.html', context)
    return redirect(home_page)


def insert_product_sql(product_name, unit, units_in_stock, price_per_unit, category, sub_category):
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


def stock(request):
    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'stock.html', context)


def change_stock(request):
    if 'customer_id' not in request.session or request.session['customer_id'] != 1:
        return  redirect(home_page)

    product_id = str(request.POST.get("products"))
    change_in_stock = str(request.POST.get("change_in_stock"))
    change_in_stock = int(change_in_stock)
    sql = 'UPDATE PRODUCT SET UNITS_IN_STOCK = UNITS_IN_STOCK + %s WHERE PRODUCT_ID = %s'
    cursor.execute(sql, [change_in_stock, product_id])

    return redirect("http://127.0.0.1:8000/manage_product/stock/")


def get_products(request):
    category = request.GET.get('category', None)
    subcategory = request.GET.get('subcategory', None)
    sql = 'SELECT PRODUCT_ID, PRODUCT_NAME FROM PRODUCT WHERE CATEGORY = %s AND SUB_CATEGORY = %s'
    cursor.execute(sql, [category, subcategory])
    result = cursor.fetchall()
    data = []
    for row in result:
        data.append({
            'product_id': row[0],
            'product_name': row[1]
        })
    return JsonResponse(data, safe=False)

