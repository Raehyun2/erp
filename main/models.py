from django.db import models
from django.utils import timezone
from django.conf import settings

class Upload_Excel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='excel/')

class Receipts_page(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    product_number = models.CharField(max_length=100)
    product_place = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    remain_product = models.IntegerField()

    def __str__(self):
        return self.product_number

class Issue_page(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    product_number = models.CharField(max_length=100)
    product_place = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    remain_product = models.IntegerField()

    def __str__(self):
        return self.product_number

class Stock_page(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    product_number = models.CharField(max_length=100)
    product_place = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    remain_product = models.IntegerField()

    def __str__(self):
        return self.product_number