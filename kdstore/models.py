
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now


# Create your models here.

PRODUCT_CHOICES = {
    ('Mobiles', 'Mobiles'),
    ('Electronics', 'Electronics'),
    ('Appliances', 'Appliances'),
    ('Fashion', 'Fashion')
}

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=300)
    category = models.CharField(choices=PRODUCT_CHOICES, max_length=100)
    subcategory = models.CharField(max_length=100, default="")
    brand = models.CharField(max_length=100, default="")
    description = models.TextField()
    price = models.IntegerField(default=0)
    slug = models.CharField(max_length=500)
    publish_date = models.DateTimeField(default=now)
    image = models.ImageField(upload_to="kdstore/images", default="loading")

    def __str__(self):
        return self.product_name



class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orderId = models.CharField(max_length=50)
    orderItem = models.CharField(max_length=5000)
    amount = models.IntegerField(default='')
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=111, default="")
    orderTime = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.user.username + ' : ' + self.orderId


ORDER = {
    ('Deliver', 'Deliver'),
    ('Pending', 'Pending')
}

class Order(models.Model):
    order = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    delivery = models.CharField(choices=ORDER, default='Pending', max_length=50)

    def __str__(self):
        return 'id' + self.order.orderId + ', ' + self.delivery + ' | ' + self.order.user.username


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, default="")
    subject = models.CharField(max_length=100, default="")
    message = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.user.username + ' : ' + self.subject

class ProductComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now) 

    def __str__(self):
        return self.comment[0:15] + "..." + " by " + self.user.username

class ProductRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(default='0')
    
    def __str__(self):
        return f"{self.user.username} ... {self.product.product_name[0:20]} ... Rating:{self.rate}"

class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    head1 = models.TextField(max_length=100)
    head2 = models.TextField(max_length=100)
    image = models.ImageField(upload_to="kdstore/offers", default="loading")
     
    def __str__(self):
        return self.product.product_name