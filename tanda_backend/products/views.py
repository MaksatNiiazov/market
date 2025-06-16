from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tanda_backend.products.models.image import Image


@csrf_exempt
def upload_file_api(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Post method only allowed'
        }, status=400)

    if 'file' not in request.FILES:
        return JsonResponse({
            'success': False,
            'error': 'Файл не предоставлен'
        }, status=400)

    file = request.FILES['file']

    uploaded_file = Image(
        file=file
    )
    uploaded_file.save()

    return JsonResponse({
        'success': True,
        'id': uploaded_file.id,
        'file_url': uploaded_file.file.url,
    })
