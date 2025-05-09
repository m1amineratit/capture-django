from django.db import models

# Create your models here.

class Image(models.Model):
    img = models.ImageField(upload_to='media1/')    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Image {self.id} created on {self.created_at}"