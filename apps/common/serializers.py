import uuid
import base64

from rest_framework import serializers
from django.core.files.base import ContentFile

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith('data:image'):
            # Split the header and the actual data
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            # Generate a unique file name
            file_name = str(uuid.uuid4()) + '.' + ext
            data = ContentFile(base64.b64decode(imgstr), name=file_name)

        return super().to_internal_value(data)