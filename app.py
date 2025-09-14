import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import chainlit as cl
from agents import (
    Agent,
    InputGuardrail,
    GuardrailFunctionOutput,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled
)
from agents.exceptions import InputGuardrailTripwireTriggered

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Disable tracing
set_tracing_disabled(disabled=True)

# Initialize Gemini API client
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Pydantic model for guardrail
class TravelOutput(BaseModel):
    is_travel_question: bool = Field(..., description="True if the question is about travel services.")
    reasoning: str

# Guardrail agent
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about travel-related services "
                 "(Hotels, Transport, Food, etc.). "
                 "If yes, set is_travel_question=True, else False. Also give a reasoning.",
    output_type=TravelOutput,
    model=llm_model
)

# Department agents
hotel_agent = Agent(
    name="Hotel Representative",
    handoff_description="Hotel Representative",
    instructions="Help with Hotel queries, explain each step clearly.",
    model=llm_model
)
transport_agent = Agent(
    name="Transport Representative",
    handoff_description="Transport Representative",
    instructions="Help with Transport queries, provide context and step-by-step guidance.",
    model=llm_model
)
food_agent = Agent(
    name="Food Representative",
    handoff_description="Food Representative",
    instructions="Help with Food queries, give detailed and clear answers.",
    model=llm_model
)

# Guardrail function
async def travel_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(TravelOutput)

    print("[Guardrail_function output]", final_output)

    # Block if not travel related
    if not final_output.is_travel_question:
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=False
    )

# Triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="Decide which category the question belongs to: 'Hotels', 'Transport', or 'Food'. "
                 "Respond ONLY with the category name.",
    input_guardrails=[InputGuardrail(guardrail_function=travel_guardrail)],
    model=llm_model
)

# Chainlit events
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hi! I am your Travel Assistant, Ask me about Hotels, Transport, or Food.").send()

@cl.on_message
async def on_message(message: cl.Message):
    try:
        # Step 1: Triage
        await cl.Message(content=f"🕵️ *Triage Agent* is analyzing your question: '{message.content}'").send()
        triage_result = await Runner.run(triage_agent, message.content)
        
        print("[Triage raw result]", triage_result.final_output)

        category = triage_result.final_output.strip().lower()
        print("[Triage decision]", category)

        # Step 2: Choose correct agent (lowercase matching)
        if "hotel" in category:
            chosen_agent = hotel_agent
        elif "transport" in category:
            chosen_agent = transport_agent
        elif "food" in category:
            chosen_agent = food_agent
        else:
            await cl.Message(content="❓ Sorry, I couldn't categorize your question.").send()
            return

        # Step 3: Announce handoff
        await cl.Message(content=f"📡 Triage Agent is handing off to *{chosen_agent.name}*").send()

        # Step 4: Get agent response
        travel_result = await Runner.run(chosen_agent, message.content)
        await cl.Message(content=f"🤖 *{chosen_agent.name}* says: {travel_result.final_output}").send()

    except InputGuardrailTripwireTriggered as e:
        reason = getattr(e, "args", ["No reason provided"])[0]
        await cl.Message(content=f"🚫 *Guardrail Activated!*\nReason: {reason}").send()
