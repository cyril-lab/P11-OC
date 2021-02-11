from django.db import models
from substitute.models.category import Category
from substitute.models.user import User


class Product(models.Model):
    """this class is used to generate the product table"""
    name = models.CharField(max_length=200)
    store = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=100)
    nutriment_fat = models.CharField(max_length=100, default='inconnu')
    nutriment_saturated_fat = models.CharField(max_length=100,
                                               default='inconnu')
    nutriment_sugars = models.CharField(max_length=100, default='inconnu')
    nutriment_salt = models.CharField(max_length=100, default='inconnu')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, related_name="user_favorite",
                                      blank=True)

    def __str__(self):
        return self.pk
