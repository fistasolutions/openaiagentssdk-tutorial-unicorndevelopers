from agents import Agent, Runner, set_default_openai_key, ModelSettings, RunConfig
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))

agent = Agent(
    name="Poet Agent",
    instructions="You are a poetic assistant.",
    model="gpt-3.5-turbo"  # This will be overridden by run_config if set
)

run_config = RunConfig(
    model="gpt-4o",  # Overrides agent's default if needed
    model_settings=ModelSettings(temperature=0.8),  # More creative responses
    workflow_name="creative_poem_run",  # Good for trace organization
    trace_metadata={"project": "poetry", "env": "dev"}
)

result = Runner.run_sync(agent, "Write a haiku about spring.", run_config=run_config)

print(result.final_output)
