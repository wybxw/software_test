from django.db import models

class List(models.Model):
    # items = models.ManyToManyField(Item, blank=True)
    # This is a placeholder for the list model.
    # It can be extended with additional fields as needed.
    pass
# Create your models here.
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
    pass