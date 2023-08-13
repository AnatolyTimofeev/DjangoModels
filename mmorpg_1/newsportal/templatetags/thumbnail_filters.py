import os

from django import template
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings

register = template.Library()


@register.filter
def thumbnail_url(image_url, size):
    width, height = [int(x) for x in size.split('x')]
    image_path = os.path.join(settings.MEDIA_ROOT, image_url[len(settings.MEDIA_URL):])

    image = Image.open(image_path)
    image.thumbnail((width, height), Image.ANTIALIAS)

    thumb_io = BytesIO()
    image.save(thumb_io, format='JPEG')
    thumbnail = ContentFile(thumb_io.getvalue())

    return settings.MEDIA_URL + thumbnail.name