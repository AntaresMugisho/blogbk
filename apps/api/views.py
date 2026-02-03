import os
from random import random

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.mail import send_mail
from utils import random_filename

from .serializers import ContactSerializer

class FileUploadAPIView(GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('image')
        
        if not file_obj:
            return Response({"success": False, "error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the file manually
        save_path = default_storage.save(os.path.join('uploads', random_filename(file_obj, file_obj.name)), file_obj)
        file_url = default_storage.url(save_path)

        return Response({
            "success": True,
            "file": {
                "url": request.build_absolute_uri(file_url)
            }
        }, status=status.HTTP_201_CREATED)


class ContactAPIView(GenericAPIView):
    authentication_classes = [] 
    permission_classes = [] 

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            send_mail(
                subject=data["subject"],
                message=f"""
Nom: {data['name']}
Email: {data['email']}

Message:
{data['message']}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return Response(
                {"success": True, "message": "Message sent successfully"},
                status=status.HTTP_200_OK,
            )

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

