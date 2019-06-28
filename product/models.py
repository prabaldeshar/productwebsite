from django.db import models


# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    manufacturer = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.IntegerField(default=0)
