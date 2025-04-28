from django.shortcuts import render
from rest_framework.views import APIView    
from rest_framework.response import Response


class UploadFileView(APIView):
    def create():
        return Response({"success": True}, status=200)
