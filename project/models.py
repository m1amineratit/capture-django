from django.db import models

# Create your models here.

class Image(models.Model):
    img = models.ImageField(upload_to='uploaded_images/')    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Image {self.id} created on {self.created_at}"
    

class Location(models.Model):
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)


class DeviceInfo(models.Model):
    user_agent = models.TextField()
    platform = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    screen_width = models.IntegerField()
    screen_height = models.IntegerField()
    timezone = models.CharField(max_length=100)
    online = models.BooleanField()
    cookies_enabled = models.BooleanField()
    touch_support = models.BooleanField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DeviceInfo from {self.created_at}"
    

class Screenshot(models.Model):
    image = models.ImageField(upload_to='screenshots/')  # Save the image in a 'screenshots' directory
    timestamp = models.DateTimeField(auto_now_add=True)  # Track when the screenshot was taken

    def __str__(self):
        return f"Screenshot taken at {self.timestamp}"
    


    

class VisitorInfo(models.Model):
    fingerprint = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=50)
    screen_width = models.IntegerField()
    screen_height = models.IntegerField()
    color_depth = models.IntegerField()
    timezone_offset = models.IntegerField()
    referrer = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=50)
    is_new_visitor = models.BooleanField(default=False)
    cookies_enabled = models.BooleanField(default=False)
    operating_system = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Visitor: {self.fingerprint}"
    


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
