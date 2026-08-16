"""Direct debug test - calls orchestrator directly to see full error."""
import asyncio
import sys
sys.path.insert(0, 'backend')

async def main():
    try:
        from orchestrator import create_agent_from_prompt
        print("Calling create_agent_from_prompt...")
        result = await create_agent_from_prompt("A helpful customer support agent that answers questions politely")
        print(f"SUCCESS! Agent: {result.name}")
        print(f"Validation: {result.validation.valid}")
    except Exception as e:
        import traceback
        print(f"ERROR: {e}")
        print("Full traceback:")
        traceback.print_exc()

asyncio.run(main())
