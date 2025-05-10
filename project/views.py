from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Image, Location, VisitorInfo
import base64
from datetime import datetime, time
import os
import json
from django.conf import settings
from .models import Screenshot

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
    

from .models import DeviceInfo

def save_device_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        device = DeviceInfo.objects.create(
            user_agent=data.get('userAgent'),
            platform=data.get('platform'),
            language=data.get('language'),
            screen_width=data.get('screenWidth'),
            screen_height=data.get('screenHeight'),
            timezone=data.get('timeZone'),
            online=data.get('online'),
            cookies_enabled=data.get('cookiesEnabled'),
            touch_support=data.get('touchSupport'),
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid method'}, status=405)


import time



def save_screenshot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data.get('image')

        if image_data:
            image_data = image_data.split(",")[1]
            image_name = f"screenshot_{int(time.time())}.png"
            image_content = base64.b64decode(image_data)

            screenshot_path = os.path.join(settings.MEDIA_ROOT, 'screenshots', image_name)

            # Ensure the directory exists
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            with open(screenshot_path, 'wb') as f:
                f.write(image_content)

            screenshot = Screenshot.objects.create(image=screenshot_path)

            return JsonResponse({'status': 'success', 'message': 'Screenshot saved successfully'})
        return JsonResponse({'status': 'error', 'message': 'No image data provided'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




@csrf_exempt  # Disable CSRF protection for testing (be sure to handle this securely later)
def collect_visitor_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debug line

            # Check if visitor already exists by fingerprint
            visitor, created = VisitorInfo.objects.get_or_create(
                fingerprint=data['fingerprint'],
                defaults={
                    'device_type': data['deviceType'],
                    'screen_width': data['screenInfo']['width'],
                    'screen_height': data['screenInfo']['height'],
                    'color_depth': data['screenInfo']['colorDepth'],
                    'timezone_offset': data['timezoneOffset'],
                    'referrer': data.get('referrer', ''),
                    'language': data['language'],
                    'is_new_visitor': data['isNewVisitor'],
                    'cookies_enabled': data['cookiesEnabled'],
                    'operating_system': data['operatingSystem'],
                    'latitude': data.get('latitude', None),
                    'longitude': data.get('longitude', None),
                }
            )
            
            if not created:
                # Update visitor if it already exists
                visitor.latitude = data.get('latitude', visitor.latitude)
                visitor.longitude = data.get('longitude', visitor.longitude)
                visitor.save()

            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
