from django.shortcuts import render
from rest_framework.views import APIView    
from rest_framework.response import Response


class UploadFileView(APIView):
    def create():
        print(self.request.data)
        
        return Response({
            "success": 1,
            "file": "url_placeholder"
        }, status=200)
