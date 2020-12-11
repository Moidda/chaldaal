from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import redirect
from cart.views import cart
from django.http import JsonResponse


welcome = 'http://127.0.0.1:8000/welcome/'
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
        rating_by_customer = int(round(row[7]))
        percent_discount = cursor.callfunc('GET_PRODUCT', str, [product_id, 'PERCENT_DISCOUNT'])
        if not percent_discount:
            percent_discount = 0
        percent_discount = int(percent_discount)
        discounted_price = price_per_unit - (price_per_unit * percent_discount // 100)

        cart_count = 0
        if product_id in cart.products:
            cart_count = cart.products[product_id]
        context.append({
            'product_id': product_id,
            'product_name': product_name,
            'unit': unit,
            'units_in_stock': units_in_stock,
            'price_per_unit': price_per_unit,
            'category': category,
            'sub_category': sub_category,
            'rating_by_customer': rating_by_customer,
            'percent_discount': percent_discount,
            'discounted_price': discounted_price,
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
        return redirect(welcome)


def popular(request):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    sql = "SELECT * FROM PRODUCT WHERE RATING_BY_CUSTOMER>2 ORDER BY PRODUCT_ID"
    table = get_table(sql)
    table = [table[i: i+3] for i in range(0, len(table), 3)]
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'product_list.html', context)


def show_product_category(request, category):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    category = category.lower()
    category = category.replace('-', ' ')
    sql = "SELECT * FROM PRODUCT WHERE LOWER(CATEGORY) = '%s' ORDER BY PRODUCT_ID" % category
    table = get_table(sql)
    table = [table[i: i + 3] for i in range(0, len(table), 3)]
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'product_list.html', context)


def show_sub_category(request, sub_category):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    sub_category = sub_category.lower()
    sub_category = sub_category.replace('-', ' ')
    sql = "SELECT * FROM PRODUCT WHERE LOWER(SUB_CATEGORY) = '%s' ORDER BY PRODUCT_ID" % sub_category
    table = get_table(sql)
    table = [table[i: i + 3] for i in range(0, len(table), 3)]
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'product_list.html', context)


def show_product_search(request, searched_item):
    if 'customer_id' not in request.session:
        return redirect(log_in)

    if searched_item == 'none':
        searched_item = ''
    searched_item = searched_item.replace('-', ' ')
    sql = "SELECT * FROM PRODUCT WHERE LOWER(PRODUCT_NAME) LIKE '%%%s%%' ORDER BY PRODUCT_ID" % searched_item
    table = get_table(sql)
    table = [table[i: i+3] for i in range(0, len(table), 3)]
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    if len(table) == 0:
        return render(request, 'not_found.html', context)
    return render(request, 'product_list.html', context)


# is called from the search-form in navbar html
def searched(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)
    searched_item = str(request.POST.get('searched'))
    searched_item = searched_item.lower()
    if not searched_item:
        searched_item = 'none'
    searched_item = searched_item.replace(' ', '-')
    return redirect('http://127.0.0.1:8000/show_product_search/' + searched_item + '/')


def get_subcategory_filter(request):
    categories = request.GET.getlist('categories[]', None)
    data = []
    for cat in categories:
        sql = 'SELECT UNIQUE(SUB_CATEGORY) FROM PRODUCT WHERE CATEGORY = %s'
        cursor.execute(sql, [cat])
        result = cursor.fetchall()
        for row in result:
            data.append(row[0])

    return JsonResponse(data, safe=False)


def get_sale_table(sql):
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
        rating_by_customer = int(round(row[7]))
        percent_discount = row[8]
        discounted_price = price_per_unit - (price_per_unit * percent_discount // 100)
        cart_count = 0
        if product_id in cart.products:
            cart_count = cart.products[product_id]
        context.append({
            'product_id': product_id,
            'product_name': product_name,
            'unit': unit,
            'units_in_stock': units_in_stock,
            'price_per_unit': price_per_unit,
            'category': category,
            'sub_category': sub_category,
            'rating_by_customer': rating_by_customer,
            'percent_discount': percent_discount,
            'discounted_price': discounted_price,
            'cart_count': cart_count
        })

    return context


def show_product_flash_sale(request):
    if 'customer_id' not in request.session:
        return redirect(log_in)
    sql = '''
            SELECT 
                P.PRODUCT_ID,
                P.PRODUCT_NAME,
                P.UNIT,
                P.UNITS_IN_STOCK,
                P.PRICE_PER_UNIT,
                P.CATEGORY,
                P.SUB_CATEGORY,
                P.RATING_BY_CUSTOMER,
                F.PERCENT_DISCOUNT
            FROM 
                PRODUCT P,
                FLASH_SALE F
            WHERE 
                P.PRODUCT_ID = F.PRODUCT_ID AND
                F.PERCENT_DISCOUNT > 0
    '''
    table = get_sale_table(sql)
    table = [table[i: i + 3] for i in range(0, len(table), 3)]
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'product_list.html', context)


def flash_sale_count(request):
    count = (cursor.execute('SELECT COUNT(*) FROM FLASH_SALE WHERE PERCENT_DISCOUNT>0')).fetchall()[0][0]
    return JsonResponse({'count': int(count)})


def show_bundle_offer(request):
    context = {
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'bundle-customer-end.html', context)

def covid(request):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    sql = "SELECT * FROM PRODUCT WHERE CATEGORY = 'Covid-19 Protection'"
    table = get_table(sql)
    table = [table[i: i + 3] for i in range(0, len(table), 3)]
    context = {
        'product': table,
        'customer_id': request.session['customer_id'],
        'cart_price': cart.total_cost
    }
    return render(request, 'product_list.html', context)