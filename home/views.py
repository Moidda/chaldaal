from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect
from cart.views import cart


home_page = 'http://127.0.0.1:8000'
log_in = 'http://127.0.0.1:8000/log_in'
cursor = connection.cursor()


def get_table(sql):
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
        cart_count = 0
        if product_id in cart.products:
            cart_count = cart.products[product_id]
        context.append({
            'product_id': product_id,
            'product_name': product_name,
            'unit': unit,
            'units_in_stock': units_in_stock,
            'price_per_unit': price_per_unit,
            'category': category, 'sub_category': sub_category,
            'rating_by_customer': rating_by_customer,
            'cart_count': cart_count
        })

    return context


def home(request):
    if 'customer_id' in request.session:
        context = {
            'customer_id': request.session['customer_id'],
            'cart_price': cart.total_cost
        }
        return render(request, 'Homepage.html', context)
    else:
        return redirect(log_in)


def popular(request):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    sql = "SELECT * FROM PRODUCT WHERE RATING_BY_CUSTOMER>2 ORDER BY PRODUCT_ID"
    table = get_table(sql)
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }

    return render(request, 'home_page.html', context)


def show_product_category(request, category):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    category = category.lower()
    category = category.replace('-', ' ')
    sql = "SELECT * FROM PRODUCT WHERE LOWER(CATEGORY) = '%s' ORDER BY PRODUCT_ID" % category
    table = get_table(sql)
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }

    return render(request, 'home_page.html', context)


def show_product_search(request, searched_item):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    if searched_item == 'none':
        searched_item = ''
    sql = "SELECT * FROM PRODUCT WHERE LOWER(PRODUCT_NAME) LIKE '%%%s%%' ORDER BY PRODUCT_ID" % searched_item
    table = get_table(sql)
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'home_page.html', context)


def searched(request):
    if 'customer_id' in request.session:
        searched_item = str(request.POST.get('searched'))
        searched_item = searched_item.lower()
        if not searched_item:
            searched_item = 'none'
        return redirect('http://127.0.0.1:8000/show_product_search/' + searched_item + '/')


