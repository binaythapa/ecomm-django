from django.db import models

from store.models import *

# Create your models here.

class userReview(models.Model):
    userComment= models.CharField(max_length=1000)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete= models.CASCADE)