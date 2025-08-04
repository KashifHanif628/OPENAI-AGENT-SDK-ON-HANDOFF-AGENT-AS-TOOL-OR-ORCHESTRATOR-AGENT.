"""EXTENSIONS IN HANDOFF WITH RECOMMENDED_PROMPT_PREFIX"""
# YANI HAM APNI MARZI SE TRIAGE AGENT KO INSTRUCTION DE KER EK BEHTAR OUTPUT HASIL KER SAKTE HE. JIS TERHA KA HAM CHAHTE HE.

from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

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
)


french_agent = Agent(
    name= "French Agent",
    instructions="You translate the user message into French",
)


receptionest_agent = Agent (
    name="Receptionest Agent",
    instructions=(f"""{RECOMMENDED_PROMPT_PREFIX}
    You are like a receptionist agent. If someone asks something in or about Spanish, send them to the Spanish Agent.
    If it's in or about French, send to the French Agent.
    If it's about something else (like history, science, etc.), answer it yourself.
    Always be clear and confident in deciding who should respond.
    """),
    handoffs=[spanish_agent, french_agent]
)

result = Runner.run_sync(receptionest_agent,input="students are asking that when their english class will be start ?", run_config=config)

print(result.final_output)
# print(result.last_agent)
# print(RECOMMENDED_PROMPT_PREFIX)



"""
🔹 ->. RECOMMENDED_PROMPT_PREFIX Kya Hai?
✅ Ye Kya Hai?
RECOMMENDED_PROMPT_PREFIX ek pre-defined string hoti hai jo agent prompt ke start mein daali jaati hai. Ye mostly general guidance aur standardized setup instructions deta hai har agent ke liye, taake model ka behavior predictable aur coherent ho.

🎯 Example Use-Cases:
Reinforces that the agent is supposed to follow a specific role or set of behavior patterns.
Adds useful instructions like: "You are an AI assistant," "Stay within your domain," etc.
Ensures agents follow best practices and use safe/expected response formats.

✨ Benefits:
Consistency: Har agent ek standard tone aur role follow karta hai.
Alignment: Model zyada achhe se samajhta hai ki usay kis context mein operate karna hai.
Reusability: Agar aap multiple agents banate ho, aapko har baar woh base prompt likhne ki zarurat nahi.
"""


# EXAMPLES

# 🧠 1. RECOMMENDED_PROMPT_PREFIX — Socho Ye Ek "Teacher Ki Guidance" Hai
"""🎓 Misaal:"""
# Sochiye aap ek school mein ho aur har teacher ko ek note milta hai class lene se pehle:

"Aap aik zimmedar teacher hain. Aapka kaam sirf apnay subject par focus karna hai. Students ko clear, respectful aur" 
"accurate jawab dena hai. Aur agar koi student doosray subject ka sawal kare to usay related teacher ke paas bhejna hai."

# Ye note sab teachers ke liye common hai. Har teacher ke pass apna apna subject-specific instruction bhi hota hai, 
# lekin ye common prefix unki base soch aur behavior ko guide karta hai.

"""💡 Asan Alfaz me matlab:"""
# RECOMMENDED_PROMPT_PREFIX bhi wahi guidance hoti hai — ye AI agent ko batata hai:
# Tum ek responsible AI ho.
# Har sawal ka sachai se jawab do.
# Apni boundary mein raho.
# Agar kisi aur specialist agent ki zarurat ho, to usey handoff karo.
#Isse AI agents consistent, tameezdaar aur domain-focused bante hain.


"""🧠 2. triage_agent — Socho Ye Ek "School Ka Receptionist" Hai"""
# 🎓 Misaal:
# Ek school ke receptionist ka kaam hota hai decide karna:
# Agar koi student Spanish class ka sawal le kar aaye ➡️ usay Spanish teacher ke paas bhej do.
# Agar koi French class ka sawal ho ➡️ usay French teacher ke paas bhej do.
# Agar koi bole "Water cooler kahan hai?" ➡️ khud jawab de do.
# Aapka triage_agent bhi exactly yehi kaam karta hai:
# Spanish agent ko Spanish wale sawal.
# French agent ko French wale.
# Baaki sab ka jawab khud deta hai.

# ✅ To Aap Kya Karein?
# triage_agent ke prompt ko thoda clear aur professional banayein — jaise school receptionist ko training dete hain: