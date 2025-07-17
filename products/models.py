from django.db import models
# ode assists from geeks for geeks https://www.geeksforgeeks.org/python/e-commerce-product-catalog-using-django/?utm_
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)


    def __str__(self):
        return self.name
