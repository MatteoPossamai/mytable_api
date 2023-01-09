from django.db import models

from restaurant.models.restaurant import Restaurant

class Order(models.Model):
    payment_method = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255) # 1: Submitted, 2: Received, 3: Preparing, 4: Ready, 5: Delivered
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return "Order: " + str(self.id) + " - " + self.restaurant.name + " - " + str(self.date)
