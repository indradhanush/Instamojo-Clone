"""
Model definitions for the app clone.
"""

from django.db import models
from django.contrib.auth.models import User


CURRENCY_CHOICES = [
    ("INR", "Indian Rupee"),
    ("USD", "US Dollar"),
]


class Product(models.Model):
    username = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    description = models.TextField()
    currency = models.CharField(max_length=20, choices=CURRENCY_CHOICES)
    base_price = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=500)
    sold = models.BooleanField(default=False)
