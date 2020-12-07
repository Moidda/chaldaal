from django.db import connection


cursor = connection.cursor()


class RatingSystem:
    rating = {}

    def createRatingSystem(self, product_list):
        for pid in product_list:
            self.rating[pid] = 0

    def increase_rating(self, pid):
        self.rating[pid] = min(self.rating[pid]+1, 5)

    def decrease_rating(self, pid):
        self.rating[pid] = max(self.rating[pid]-1, 0)

    def clear(self):
        self.rating.clear()

    def save_rating(self):
        for pid in self.rating:
            cursor.callproc('UPDATE_PRODUCT_RATING', [pid, self.rating[pid]])
        self.clear()