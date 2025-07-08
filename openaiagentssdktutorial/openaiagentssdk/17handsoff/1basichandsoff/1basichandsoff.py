from agents import Agent, Runner, handoff
import asyncio

# 🧾 Specialized agents
billing_agent = Agent(name="Billing agent", instructions="You handle billing queries.")
refund_agent = Agent(name="Refund agent", instructions="You handle refund-related issues.")

# 🤝 Triage agent with handoffs to billing and refund agents
triage_agent = Agent(
    name="Triage agent",
    instructions="You route the user's query to the correct department.",
    handoffs=[
        billing_agent,  # Direct agent handoff (tool name will be auto-generated)
        handoff(refund_agent)  # Customizable handoff with default behavior
    ]
)

# 🚀 Test the handoff
async def main():
    print("🧪 Running Handoff Demo...\n")

    result = await Runner.run(
        triage_agent,
        input="I would like a refund for my last purchase."
    )

    print("🧠 Final Output:")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
