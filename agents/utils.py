import json
import logging

from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.adk.agents import RunConfig
from google.adk.agents.run_config import StreamingMode
from google.genai import types
from uuid import uuid4

from .chatbot.agent import root_agent as chatbot_agent

APP_NAME = "ChatBot Fall Back"

INITIAL_STATE = {
    "enterprise": "Art Revolution Label", 
    "about": "Art Revolution Label est une entreprise de textile et de mode basée en République Démocratique du Congo dans la ville de Goma.",
    "ceo": "Antares Mugisho"
}

db_url = f"sqlite+aiosqlite:///./agents.db"
session_service = DatabaseSessionService(db_url)

logger = logging.getLogger(__name__)

async def get_session(user_id: str, session_id: str = None, app_name: str = APP_NAME) -> DatabaseSessionService:

    # Create a custom user_id if it's None
    user_id = user_id or  str(uuid4().hex)

    # If a session_id was provided, try to find it
    if session_id:
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
        if session:
            logger.info(f"Continue with existing session {session_id}")
            return session

    # If no session_id was provided or was provided but not found, create a new one
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state=INITIAL_STATE
    )

    logger.info(f"Created new session {session.id}")

    return session


async def get_runner(agent, app_name: str = APP_NAME):
    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )

    return runner


async def call_agent_async(runner, session, parts):
    """Call the agent asynchronously with the user's input."""

    content = types.Content(role="user", parts=parts)

    final_response = '{"answer": "", "confidence": 0.0, "needs_human": True, "reason": "error"}'

    try:
        async for event in runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            # Process each event and get the final response if available
            if event.is_final_response():
                if (
                    event.content
                    and event.content.parts
                    and event.content.parts[0].text
                ):
                    final_response = event.content.parts[0].text.strip()
    except Exception as e:
        logger.error(e)
        return {"error": str(e)}

    return {
        "session_id": session.id, 
        "user_id": session.user_id, 
        "app_name": session.app_name,
        "final_response": json.loads(final_response)
    }


def run_agent_live(runner, session, parts):
    """Call the agent synchronously with the user's input."""
    pass


async def start_chat():
    runner = Runner(agent=chatbot_agent)
    
    async for event in runner.run_async(
        input="Write a story about Django developers.",
    ):
        if event.content:
            print(event.content.parts[0].text, end="", flush=True)


if __name__ == "__main__":
    import asyncio
    asyncio.run(start_chat())