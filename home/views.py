from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect

home_page = 'http://127.0.0.1:8000'


def get_table(searched_item):
    cursor = connection.cursor()
    sql = "SELECT * FROM PRODUCT WHERE LOWER(PRODUCT_NAME) LIKE '%%%s%%'" % searched_item
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
        context.append({'product_id': product_id, 'product_name': product_name, 'unit': unit, 'units_in_stock': units_in_stock,
             'price_per_unit': price_per_unit, 'category': category, 'sub_category': sub_category,
             'rating_by_customer': rating_by_customer})

    return context



def home(request):
    if 'customer_id' in request.session:
        searched_item = ""
        if 'searched_item' in request.session:
            searched_item = request.session['searched_item']
        table = get_table(searched_item)
        return render(request, 'home_page.html', {'product': table})
    else:
        return redirect('http://127.0.0.1:8000/log_in')


def searched(request):
    if 'customer_id' in request.session:
        searched_item = str(request.POST.get('searched'))
        searched_item = searched_item.lower()
        request.session['searched_item'] = searched_item
        return redirect(home_page)


