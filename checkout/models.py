from django.db import connection


cursor = connection.cursor()


class Credit:
    total_credits = -1
    redeemed_credits = 0
    per_credit_discount = 2

    def set_credit(self, customer_id):
        self.total_credits = cursor.callfunc('GET_CUSTOMER', int, [customer_id, 'CUSTOMER_CREDIT'])
        self.redeemed_credits = 0

    def redeem(self, credit):
        credit = min(credit, self.total_credits)
        self.redeemed_credits = credit

    def clear_credit(self):
        self.total_credits = -1
        self.redeemed_credits = 0
