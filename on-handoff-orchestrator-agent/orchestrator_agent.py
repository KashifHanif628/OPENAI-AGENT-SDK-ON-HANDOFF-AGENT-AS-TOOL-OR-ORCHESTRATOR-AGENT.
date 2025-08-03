
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
#from agents.tool import default_tool_error_function
import asyncio

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup external OpenAI client for Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Setup model
external_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Setup run configuration
config = RunConfig(
    model=external_model,
    model_provider=external_client,
    tracing_disabled=True,
)

# Creating sub-agents means agents works inside the agents.
spanish_agent = Agent(
    name= "Spanish Agent",
    instructions="You translate the user message into Spanish",
    model=external_model
)


french_agent = Agent(
    name= "French Agent",
    instructions="You translate the user message into French",
    model=external_model
)

arabic_agent = Agent(
    name= "Arabic Agent",
    instructions=" the user message into Arabic",
    model=external_model
)

# creating main agent who will take work from the sub agents.
orchestrator_agent = Agent(
    name= "orchestrator agent",
    instructions="You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools.",
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to french",
        ),
        arabic_agent.as_tool(
            tool_name="translate_to_arabic",
            tool_description="Translate the user's message to arabic",
        ),
    ],
    model=external_model
)

async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    orchestrator_result = await Runner.run(orchestrator_agent, msg)
    print(f"\n\nFinal response:\n{orchestrator_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
