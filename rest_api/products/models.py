from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator

class Product(models.Model):
    sku = name = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0.01)])
  
    def get_absolute_url(self):
      return reverse('product-detail-view', args=[str(self.id)])
  
class Meta:
    ordering = ['sku']

    def __str__(self):
      return self.sku
