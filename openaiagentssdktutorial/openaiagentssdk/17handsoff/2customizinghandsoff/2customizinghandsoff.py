from agents import Agent, Runner, handoff, RunContextWrapper
import asyncio

# ✅ Define a custom action to perform during handoff
def on_handoff(ctx: RunContextWrapper[None]):
    print("🔄 Handoff triggered! Logging event...")

# 🎯 Target agent for the handoff
specialist_agent = Agent(
    name="Specialist agent",
    instructions="You handle specialized tasks."
)

# 🔧 Customized handoff configuration
custom_handoff = handoff(
    agent=specialist_agent,
    on_handoff=on_handoff,
    tool_name_override="custom_handoff_tool",
    tool_description_override="Custom tool to transfer to a specialist agent."
)

# 🤖 Orchestrator agent that uses the customized handoff
main_agent = Agent(
    name="Main agent",
    instructions="Delegate complex tasks using custom handoffs.",
    handoffs=[custom_handoff]
)

# 🚀 Run it
async def main():
    result = await Runner.run(
        main_agent,
        input="This seems like a complex task. Can you handle it?"
    )
    print("🧠 Final Output:")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
