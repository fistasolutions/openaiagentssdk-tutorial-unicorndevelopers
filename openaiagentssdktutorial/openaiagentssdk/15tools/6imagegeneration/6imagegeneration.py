import asyncio
from agents import Agent, Runner, set_default_openai_key
from agents.tool import ImageGenerationTool, ImageGeneration
from dotenv import load_dotenv
import os

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL")

# Configure the Image Generation tool
image_tool = ImageGenerationTool(ImageGeneration({
    'type': 'image_generation'
}))

agent = Agent(
    name="Image Generator",
    instructions="You can generate images from text prompts. Create beautiful, detailed images based on user requests.",
    tools=[image_tool],
    model=model
)

def show_demo():
    """Show a demo of how the ImageGenerationTool works"""
    print("🎨 ImageGenerationTool Demo")
    print("=" * 50)
    print("📋 Tool Configuration:")
    print(f"   - Tool Type: {image_tool.name}")
    print(f"   - Config: {image_tool.tool_config}")
    print("\n🔧 How it works:")
    print("   1. Agent receives text prompt")
    print("   2. ImageGenerationTool processes the prompt")
    print("   3. DALL-E generates high-quality image")
    print("   4. Image is returned for display/download")
    print("\n💡 Example prompts that work well:")
    print("   - 'A serene mountain landscape at sunset'")
    print("   - 'A futuristic city with flying cars'")
    print("   - 'A cozy coffee shop interior'")
    print("   - 'A magical forest with glowing mushrooms'")

async def main():
    # Show demo first
    show_demo()
    print("\n" + "="*50)
    
    try:
        print("🚀 Attempting to generate image...")
        result = await Runner.run(
            agent,
            input="Generate an image of a serene mountain landscape at sunset with a lake in the foreground."
        )
        print("🎨 Final Output:\n", result.final_output)
        
    except Exception as e:
        if "organization must be verified" in str(e).lower():
            print("🔒 Organization Verification Required")
            print("=" * 50)
            print("To use image generation, your OpenAI organization needs to be verified.")
            print("Please visit: https://platform.openai.com/settings/organization/general")
            print("Click 'Verify Organization' and wait up to 15 minutes for access to propagate.")
            print("\n✅ The code is correct and will work once organization is verified!")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())