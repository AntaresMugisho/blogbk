from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from antares_dotenv import env
from pydantic import BaseModel, Field

from .prompt import INSTRUCTIONS
from .tools import get_current_date, get_current_time


MODEL = LiteLlm(
    model=env('OPENROUTER_MODEL'),
    api_key=env("OPENROUTER_API_KEY")
)

class AnswerSchema(BaseModel):
   answer: str = Field(description="The answer to the question")
   confidence: float = Field(description="The confidence level of the answer from 0.0 to 1.0")
   needs_human: bool = Field(description="Whether the answer needs a human to intervene")
   reason: str = Field(description="The reason for the answer low_confidence: out_of_scope | sensitive_topic | user_request | ok")

class ChatBotAgent:
    """
    An agent that can answer questions based on the provided context.
    """
    def __init__(self):
        self.agent = LlmAgent(
            name="chatbot",
            model=MODEL,
            description="A chatbot that can as client support by answering questions based on the provided context.",
            instruction=INSTRUCTIONS,
            output_schema=AnswerSchema,
            output_key="resp",
            # tools=[get_current_date, get_current_time]
        )
    
    def get_agent(self) -> LlmAgent:
        return self.agent


root_agent = ChatBotAgent().get_agent()
