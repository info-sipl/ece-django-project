from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    college = models.CharField(max_length=250)
    # price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.email


class Product(models.Model):
    pname = models.CharField(max_length=200)
    bname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.pname