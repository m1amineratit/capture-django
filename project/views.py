from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Image, Location
import base64
from datetime import datetime
import os
import json

def index(request):
    return render(request, 'pages/camera1.html')  # Renders the page with webcam and upload UI

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image', None)
        if image_data:
            try:
                # Extract base64 and file extension
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]

                # Generate filename based on timestamp
                file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.' + ext
                file_path = os.path.join('uploaded_images', file_name)

                # Decode and save image
                img_data = base64.b64decode(imgstr)
                file_content = ContentFile(img_data)
                file_path_in_media = default_storage.save(file_path, file_content)

                # Save in DB
                image_instance = Image.objects.create(img=file_path_in_media)

                return JsonResponse({'status': 'success', 'file': file_path_in_media})
            except Exception as e:
                return JsonResponse({'status': 'failed', 'error': str(e)})

        return JsonResponse({'status': 'failed', 'error': 'No image provided.'})

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method.'})



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # first IP in list
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        ip_address = get_client_ip(request)

        print(f"User IP: {ip_address}, Location: {latitude}, {longitude}")
        # You can save it to your DB here
        save_location = Location.objects.create(latitude=latitude, longitude=longitude, ip_address=ip_address)
        return JsonResponse({'status': 'success'})