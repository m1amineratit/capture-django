from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .models import Image
import base64
from datetime import datetime
import os

def index(request):
    return render(request, 'pages/camera1.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image', None)
        if image_data:
            try:
                # Extract the base64 string and file extension
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]

                # Generate a file name
                file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.' + ext
                file_path = os.path.join('media', file_name)

                # Decode the base64 image data and save it as a file
                img_data = base64.b64decode(imgstr)
                file_content = ContentFile(img_data)

                # Create and save the image object
                image_instance = Image.objects.create(img=file_content)

                # Save the image file in the media directory
                with open(file_path, 'wb') as f:
                    f.write(img_data)

                return JsonResponse({'status': 'success', 'file': file_name})

            except Exception as e:
                return JsonResponse({'status': 'failed', 'error': str(e)})

    return JsonResponse({'status': 'failed', 'error': 'No image provided.'})
