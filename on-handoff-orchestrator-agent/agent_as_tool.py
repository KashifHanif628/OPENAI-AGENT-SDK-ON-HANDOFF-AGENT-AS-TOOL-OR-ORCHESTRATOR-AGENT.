"""Agent as Tool / Orchestrator Agent"""

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
triage_agent = Agent(
    name= "triage agent",
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

result = Runner.run_sync(triage_agent, "translate the line hello kashif how are you in spanish & arabic ?", run_config=config)

print("result: ",  result.final_output)



"""Understanding the above code"""

"""
💡 1. Agent-as-Tool Kya Hota Hai?
Jab hum agent.as_tool(...) likhte he, to hum aik Agent ko ek tool banate he, jo kisi aur Agent ke liye kaam kare.
Yeh basically ek function ki tarah hota hai jo kisi specific task ke liye banaya jata he (jaise translation to Spanish).
Har tool (yaani agent-as-tool) ka apna ek mission hota hai — woh kisi aur Agent ke instruction par kaam karta hai.


💡 2. Orchestrator Agent Kya Hota Hai?
Orchestrator agent woh hota hai jo multiple agents/tools ko manage karta hai — yeh decide karta hai kis tool ko kis waqt 
call karna hai.

hamhare code mein triage_agent hi orchestrator agent hai, kyun ke:

Uske paas tools hain (translate_to_spanish, translate_to_french, etc.)

Uska kaam hai tools ko istemal karna, khud se translation nahi karna.

Instructions bhi yehi keh rahi hain:
"You never translate on your own, you always use the provided tools."

To, technical taur pe hamhara triage_agent already orchestrator agent hai.

Kya Hum Iska Naam orchestrator agent Rakh Sakte Hain?
Haan, naam ham kuch bhi rakh sakte he — triage_agent, main_agent, orchestrator_agent — 
lekin yeh semantic yaani maanay aur clarity ka masla hai.


🔄 Lekin Yeh triage agent/Orchestrator agent Naam as_tool Mein Q Nahi Istemaal Hota?
Jab hum agent.as_tool(...) likhte hain, hum sub-agents ko tool bana rahe hote hain.

orchestrator agent ko tool banana logical nahi hota, kyun ke:
Woh tools ko manage karta hai — khud tool nahi hota.
Tools ko call karne wale ko tool nahi banate, balke controller ya manager banate hain.
Is wajah se, orchestrator agent ka naam as_tool mein nahi chalta, aur woh kabhi kisi aur agent ka tool nahi hota — 
balke woh khud tools ko chalata hai.


🆚 Agent-as-Tool vs Orchestrator Agent
Feature	                Agent-as-Tool	                              Orchestrator Agent
Role	                Task-specific worker (e.g. translator)	      Coordinator/controller of other agents
Used with .as_tool()	✅ Yes	                                    ❌ No (makes no sense to call it as tool)
Has tools?	            ❌ No	                                    ✅ Yes
Used for orchestration?	❌ No	                                    ✅ Yes


📌 Conclusion
Hamne jo triage_agent banaya hai, woh orchestrator agent hi hai — aur uska naam triage_agent rakhna ek logical choice hai.

Agent-as-tool ka matlab hai kisi agent ko ek specific tool ke tor pe use karna.

Orchestrator agent kabhi bhi tool nahi banta — woh tools ko call karta hai, manage karta hai.

Agar ham chahe to triage_agent ka naam orchestrator_agent bhi rakh sakte he — functionally koi farq nahi padega, 
sirf readability aur clarity improve hogi.
"""
