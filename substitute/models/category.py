from django.db import models


class Category(models.Model):
    """this class is used to generate the category table"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.pk
