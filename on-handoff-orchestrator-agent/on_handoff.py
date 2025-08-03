from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, handoff
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv


# Load env variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup OpenAI-compatible Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define model
external_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Define Refund Agent
refund_agent = Agent(
    name="Refund Agent",
    instructions="You handle all refund requests. Acknowledge the refund request and process it.",
    model=external_model
)

# Define Billing Agent
billing_agent = Agent(
    name="Billing Agent",
    instructions="You answer questions related to billing, invoices, and payment details.",
    model=external_model
)

# Custom on_handoff function
async def on_refund_handoff(context):
    print("📢 [HANDOFF]: Refund handoff occurred. Logging this action...")

# Define Triage Agent (Orchestrator)
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a customer support coordinator. "
        "If the user asks about billing, hand off control to the Billing Agent. "
        "If about refunds, hand off to the Refund Agent. "
        "You do not answer directly."
    ),
    handoffs=[
        handoff(
            agent=billing_agent,
            on_handoff=None,
            input_type=None
        ),
        handoff(
            agent=refund_agent,
            on_handoff=on_refund_handoff,
            input_type=None
        ),
    ],
    model=external_model
)

# Run example
if __name__ == "__main__":
    result = Runner.run_sync(
        triage_agent,
        "I would like a refund for my recent purchase.",
        run_config=RunConfig(model=external_model, model_provider=external_client)
    )

    print("Final Output: ", result.final_output)




"""🔹 async def on_refund_handoff(context, input_data=None):"""

# 🔍 context kya hota hai?
# context aik object hota hai jo run ke dauraan ka saara data rakhta hai:

# user ka input
# current agent
# previous interactions
# run config

# Iska type aksar RunContextWrapper hota hai.


"""🔍 input_data=None q diya gaya?"""
# Yeh optional parameter is liye diya gaya:
# handoff() kabhi kabhi structured data ke sath hota hai (jaise RefundRequest object).
# Lekin agar koi structured data pass nahi ho raha (jaise abhi), to input_data simply None rahega.
# Iska matlab:

"Agar koi data mila to usay process karo, warna ignore karo."
# Yeh optional banane ka flexibility ka tareeqa hai.


"""🔸 handoff(..., on_handoff=None, input_type=None)"""

# 🔹 on_handoff=None kab diya jata hai?
# Jab humein kisi specific handoff ke waqt koi custom kaam nahi karwana ho (jaise logging, notifications), 
# to hum on_handoff=None chhod dete hain.

"""🧠 Real-world example:"""

# Billing agent ko handoff karte waqt hum chahte hain ke koi extra kaam na ho.
# Lekin refund agent ke case mein hum log karna chahte hain, is liye on_handoff=on_refund_handoff diya gaya.

"""🔹 input_type=None ka kya matlab?"""
# Agar tum kisi structured input model ka use nahi kar rahe (jaise RefundData ya BillingQuery), 
# to tum input_type=None rakhte ho.

# Iska matlab:

# Jo bhi user ka raw input hoga, woh directly handoff agent ko diya jayega.
# Koi structured validation nahi hoga.

"""🧠 Jab use hota hai:"""
# Agar tum yeh define karo:
"""
class RefundData(BaseModel):
    order_id: str
    reason: str
"""    
# To tum input_type=RefundData de kar structure enforce kar sakte ho.