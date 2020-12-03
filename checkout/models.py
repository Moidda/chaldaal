from django.db import connection


cursor = connection.cursor()


class Credit:
    total_credits = 0
    redeemed_credits = 0
    per_credit_discount = 2

    def __init__(self, customer_id):
        self.total_credits = int(cursor.callfunc('GET_CREDIT_CARD', str, [customer_id, 'CUSTOMER_CREDIT']))

    def redeem(self, credit):
        credit = min(credit, self.total_credits)
        self.redeemed_credits = credit
