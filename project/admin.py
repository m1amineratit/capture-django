from django.contrib import admin
from .models import Image, Location, DeviceInfo, VisitorInfo, Screenshot

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'created_at')  # Make sure 'created_at' is included here
    search_fields = ('img',)

admin.site.register(Image, ImageAdmin)
admin.site.register(Location)
admin.site.register(DeviceInfo)
admin.site.register(VisitorInfo)
admin.site.register(Screenshot)