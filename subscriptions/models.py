from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_months = models.IntegerField()

    def __str__(self):
        return self.name
