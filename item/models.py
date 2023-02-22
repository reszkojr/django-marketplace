from django.db import models
from django.contrib.auth.models import User

from django.db.models import *

from djmoney.models.fields import MoneyField

from PIL import Image

class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

class Item(Model):
    name = CharField(max_length=255)
    description = TextField(blank=True, null=True, max_length=950)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    is_sold = BooleanField(default=False)
    image = ImageField(upload_to='item_images', blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)

    category = ForeignKey(Category, related_name='items', on_delete=CASCADE)
    created_by = ForeignKey(User, related_name='items', on_delete=CASCADE)

    # Resizing the image 
    def save(self):
        super().save()  # Saving the item - including the image

        img = Image.open(self.image.path) 
        if img.height > 300:
            
            new_height = 300
            new_width = new_height * img.height / img.width # Mantaning the proportion between the images

            img.thumbnail((new_width, new_height))
            img.save(self.image.path) # Replacing the old image with the resized image



    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)