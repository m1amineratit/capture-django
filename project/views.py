from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64
import os
from datetime import datetime

def index(request):
    return render(request, 'pages/camera1.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image_data = request.POST['image']
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.' + ext
        file_path = os.path.join('media', file_name)

        os.makedirs('media', exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(imgstr))

        return JsonResponse({'status': 'success', 'file': file_name})
    return JsonResponse({'status': 'failed'})
