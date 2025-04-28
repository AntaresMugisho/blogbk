from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
import os

class FileUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('image')
        
        if not file_obj:
            return Response({"success": False, "error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the file manually
        save_path = default_storage.save(os.path.join('uploads', file_obj.name), file_obj)
        file_url = default_storage.url(save_path)

        print(file_url)

        return Response({
            "success": True,
            "file": {
                "url": request.build_absolute_uri(file_url)
            }
        }, status=status.HTTP_201_CREATED)
