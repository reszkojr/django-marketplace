from django.db import models
from django.contrib.auth.models import User

from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_sold = models.BooleanField(default=False)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)

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