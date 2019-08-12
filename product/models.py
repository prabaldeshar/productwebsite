from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Products(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    manufacturer = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField(default=3.0)


    def __str__(self):
        return (self.title+"-"+str(self.id))

class Comment(models.Model):
    comment = models.CharField(max_length=300)
    polarity = models.IntegerField(default = 0)
    product = models.ForeignKey(Products, on_delete = models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user')
