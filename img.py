from django.http import JsonResponse
from PIL import Image
import base64


def get_image_info_from_path(image_path):
    try:
        image = Image.open(image_path)
        image_data = image_to_base64(image)
        image_info = {
            'imageData': image_data,
            'width': image.width,
            'height': image.height,
            'format': image.format,
        }
        image.close()
        return image_info
    except Exception as e:
        print(f'Error in getting image info: {str(e)}')
        return {}


def image_to_base64(image):
    with open(image.filename, 'rb') as f:
        image_bytes = f.read()
        base64_data = base64.b64encode(image_bytes).decode('utf-8')
    return base64_data
