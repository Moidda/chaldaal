from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from cart.views import cart


home_page = 'http://127.0.0.1:8000/'
cursor = connection.cursor()


def history(request, isCustomer, slug=''):
    if 'customer_id' not in request.session:
        return redirect(home_page)

    history_data = []
    if isCustomer:
        cursor.execute('SELECT ORDAR_NO FROM ORDAR WHERE CUSTOMER_ID = %s ORDER BY ORDAR_NO DESC', [request.session['customer_id']])
    elif slug != '':
        sql = 'SELECT CUSTOMER_ID FROM CUSTOMER WHERE EMAIL = %s'
        cursor.execute(sql, [slug])
        temp = cursor.fetchall()
        if not len(temp):
            return render(request, 'not_found.html', {'customer_id': request.session['customer_id'], 'cart_price': cart.total_cost})
        cid = temp[0][0]
        cursor.execute('SELECT ORDAR_NO FROM ORDAR WHERE CUSTOMER_ID = %s ORDER BY ORDAR_NO DESC', [cid])
    else:
        cursor.execute('SELECT ORDAR_NO FROM ORDAR ORDER BY ORDAR_NO DESC')

    result = cursor.fetchall()

    for row in result:
        ordar_no = row[0]
        cursor.execute('SELECT CUSTOMER_NAME FROM ORDER_INFO WHERE ORDAR_NO=%s', [ordar_no])
        temp = cursor.fetchall()
        if len(temp) == 0:
            continue
        customer_name = temp[0][0]
        cursor.execute('''
                        SELECT 
                            C.EMAIL 
                        FROM 
                            CUSTOMER C, ORDAR O 
                        WHERE
                            O.ORDAR_NO = %s AND
                            O.CUSTOMER_ID = C.CUSTOMER_ID 
                        ''', [ordar_no])
        result = cursor.fetchall()
        email = result[0][0]

        cursor.execute('SELECT STREET_NO FROM ORDER_INFO WHERE ORDAR_NO=%s', [ordar_no])
        street_no = (cursor.fetchall())[0][0]
        cursor.execute('SELECT HOUSE_NO FROM ORDER_INFO WHERE ORDAR_NO=%s', [ordar_no])
        house_no = (cursor.fetchall())[0][0]
        cursor.execute('SELECT APT_NO FROM ORDER_INFO WHERE ORDAR_NO=%s', [ordar_no])
        apt_no = (cursor.fetchall())[0][0]
        cursor.execute('SELECT TO_CHAR(PAYMENT_DATE) FROM PAYMENT WHERE ORDAR_NO=%s', [ordar_no])
        date = (cursor.fetchall())[0][0]

        sql = '''
            SELECT 
                P.PRODUCT_ID, P.PRODUCT_NAME, P.UNIT, P.PRICE_PER_UNIT, PIO.QUANTITY
            FROM
                PRODUCT P, PRODUCTS_IN_ORDER PIO
            WHERE 
                P.PRODUCT_ID IN (SELECT PRODUCT_ID FROM PRODUCTS_IN_ORDER WHERE ORDAR_NO = %s) AND
                PIO.ORDAR_NO = %s AND
                PIO.PRODUCT_ID = P.PRODUCT_ID
        '''
        cursor.execute(sql, [ordar_no, ordar_no])
        temp = cursor.fetchall()
        product_list = []
        for r in temp:
            pid = r[0]
            name = r[1]
            unit = r[2]
            ppu = connection.cursor().callfunc('GET_PRODUCT_PRICE', int, [pid])
            quantity = r[4]
            to_pay = quantity*ppu
            product_list.append({
                'name': name,
                'unit': unit,
                'price_per_unit': ppu,
                'quantity': quantity,
                'to_pay': to_pay
            })

        cursor.execute('SELECT CREDITS_REDEEMED FROM ORDER_INFO WHERE ORDAR_NO = %s', [ordar_no])
        credits_redeemed = (cursor.fetchall())[0][0]
        cursor.execute('SELECT CREDITS_DISCOUNT FROM ORDER_INFO WHERE ORDAR_NO = %s', [ordar_no])
        credits_discount = (cursor.fetchall())[0][0]
        cursor.execute('SELECT TOTAL_COST FROM PAYMENT WHERE ORDAR_NO = %s', [ordar_no])
        total = (cursor.fetchall())[0][0]

        payment_method = 'Cash'
        payment_no = total
        cursor.execute('SELECT CARD_NO FROM CREDIT_CARD WHERE ORDAR_NO=%s', [ordar_no])
        temp = cursor.fetchall()
        if len(temp):
            payment_method = 'Credit Card'
            payment_no = temp[0][0]
        else:
            cursor.execute('SELECT PHONE_NO FROM BKASH WHERE ORDAR_NO=%s', [ordar_no])
            temp = cursor.fetchall()
            if len(temp):
                payment_method = 'Bkash'
                payment_no = temp[0][0]

        history_data.append({
            'email': email,
            'customer_name': customer_name,
            'street_no': street_no,
            'house_no': house_no,
            'apt_no': apt_no,
            'date': date,
            'product_list': product_list,
            'credits_redeemed': credits_redeemed,
            'credits_discount': credits_discount,
            'total': total,
            'payment_method': payment_method,
            'payment_no': payment_no,
            'payment_id': ordar_no
        })

    context = {
        'cart_price': cart.total_cost,
        'customer_id': request.session['customer_id'],
        'history_data': history_data,
        'isCustomer': isCustomer
    }
    return render(request, 'history.html', context)
