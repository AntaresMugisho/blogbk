from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_status(request):
    return Response({"status": "API is running"})
