from ch06_02_tool_result import run_support_agent

if __name__ == "__main__":
    import os

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY env var to run this example.")
        print("  export ANTHROPIC_API_KEY=your_key_here")
    else:
        result = run_support_agent(
            "I want a refund for ORD-1042 because the kettle arrived broken."
        )
        print(result)