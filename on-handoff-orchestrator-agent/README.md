# 🧠 Multi-Language Translation Agent System / Orchestrator Agent

This project demonstrates a modular **AI agent orchestration system** built using sub-agents for translating user input into different languages. The system uses **OpenAI-compatible models (like Gemini)** and showcases how to use `agent-as-tool` design for scalable and reusable AI workflows.

---

## 🚀 Features

- 🔄 Translates user input into **Spanish**, **French**, and **Arabic**.
- 🧩 Uses **sub-agents** as tools for language-specific translation.
- 🧠 Central **Orchestrator Agent** (triage agent) intelligently routes translation tasks.
- 📦 Environment-driven setup using `.env` for API key security.
- ⚙️ Supports **Google Gemini API** via OpenAI-compatible client.

---

## 🏗️ Architecture

```text
           ┌─────────────────────┐
           │  Orchestrator Agent │
           │   (triage_agent)    │
           └────────┬────────────┘
                    │
      ┌─────────────┼────────────────────────────┐
      ▼             ▼                            ▼
┌────────────┐ ┌────────────┐             ┌────────────┐
│ Spanish    │ │ French     │             │ Arabic     │
│ Translator │ │ Translator │             │ Translator │
└────────────┘ └────────────┘             └────────────┘


result = Runner.run_sync(
    triage_agent,
    "translate the line hello kashif how are you in spanish & arabic ?",
    run_config=config
)

print("result: ", result.final_output)


## Expected Output:
Translations in both Spanish and Arabic, provided by their respective sub-agents.


## 🧠 Concept Inspiration
This system illustrates modular AI architecture using:

Agent-as-tool design

Clean orchestration patterns

Scalable AI pipeline modeling

________________________________________________________________________________________________________________________


## 🤖 Customer Support Agent Handoff System

This project demonstrates how to build a modular, intelligent **multi-agent customer support system** using the OpenAI-compatible Agents SDK and Gemini model. The system can **delegate customer queries** to appropriate specialist agents (like Billing or Refund) and includes custom behavior using the `on_handoff()` callback.

---

## 📌 Project Concept – in Simple Urdu

Yeh code aik **Customer Support Orchestrator Agent** banata hai jo user ka query analyze karta hai, aur usay relevant agent (Billing ya Refund) ko **handoff** karta hai. Jab handoff hota hai, hum custom logging bhi karte hain taake pata chale ke handoff kab aur kahan hua.

Iska faida yeh hai ke:
- Aik centralized agent multiple agents ko manage kar sakta hai.
- Har agent apna kaam specialize tareeqe se karta hai (Separation of Concerns).
- Custom logging ya notifications trigger kiye ja sakte hain via `on_handoff()`.

---

## 🎯 Use Cases

This system can be useful in:

- 🏢 Enterprise chat support automation
- 🛍️ E-commerce platforms (refund, billing, shipping queries)
- 📞 Call center AI agents
- 🤖 Internal company assistant with departmental routing
- 🎓 Educational projects exploring AI orchestration

---

## 🧠 Architecture

```text
               ┌────────────────────┐
               │  Triage Agent      │
               │  (Main Coordinator)│
               └────────┬───────────┘
                        │
        ┌───────────────┼──────────────────┐
        ▼                               ▼
┌───────────────┐              ┌────────────────┐
│ Billing Agent │              │ Refund Agent    │
└───────────────┘              └────────────────┘
                                ↑
                      [on_handoff logging occurs]


## 🧪 Example Usage

result = Runner.run_sync(
    triage_agent,
    "I would like a refund for my recent purchase.",
    run_config=RunConfig(model=external_model, model_provider=external_client)
)

print("Final Output:", result.final_output)

When you run this code:

The triage agent receives the query.

It identifies that it is a refund-related issue.

It hands off control to the Refund Agent.

Meanwhile, a message is printed in the console:


"""📢 [HANDOFF]: Refund handoff occurred. Logging this action..."""

🔧 Technologies Used
Python 3.9+

OpenAI Agents SDK

Gemini model (OpenAI-compatible)

Dotenv for environment management

Async I/O for smooth agent orchestration

✨ Key Features
🔁 Modular agent architecture

✅ On-demand handoff with custom hooks

📈 Scalable design for enterprise-grade systems

🧠 Orchestrator agent controls logic and routing

🔒 Secure API key loading with .env



📜 License
This project is licensed under the MIT License.