from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect

def home(request):
    if 'email' in request.session:
        cursor = connection.cursor()
        sql = 'SELECT * FROM PRODUCT'
        cursor.execute(sql)
        result = cursor.fetchall()
        context = []
        for row in result:
            product_id = row[0]
            product_name = row[1]
            unit = row[2]
            units_in_stock = row[3]
            price_per_unit = row[4]
            category = row[5]
            sub_category = row[6]
            rating_by_customer = row[7]
            context.append({'product_id':product_id, 'product_name':product_name, 'unit':unit, 'units_in_stock':units_in_stock, 'price_per_unit':price_per_unit, 'category':category, 'sub_category':sub_category, 'rating_by_customer':rating_by_customer})

        return render(request, 'home_page.html', {'product' : context})
    else:
        return redirect('http://127.0.0.1:8000/log_in')