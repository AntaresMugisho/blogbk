import adrf.views as adrfviews
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4

from agents.chatbot.agent import root_agent as chatbot_agent
from agents.utils import get_session, get_runner, call_agent_async
from google.genai import types

from .serializers import ChatBotSerializer

# Create your views here.
class ChatBotView(adrfviews.APIView):

    async def post(self, request, *args, **kwargs):
        serializer = ChatBotSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Session management: create or retrieve session
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = serializer.validated_data.get("user_id", str(uuid4()))

        session_id = kwargs.get("session_id")
        app_name = serializer.validated_data.get("app_name")

        message = serializer.validated_data.get("message")
        
        # Get the session
        session = await get_session(user_id=user_id, session_id=session_id, app_name=app_name)

        # Get the runner
        runner = await get_runner(agent=chatbot_agent, app_name=app_name)

        # Send message and return the response
        parts=[types.Part(text=message)]
        agent_response = await call_agent_async(runner, session, parts)

        if agent_response.get("error"):
            return Response(agent_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(agent_response, status=status.HTTP_200_OK)