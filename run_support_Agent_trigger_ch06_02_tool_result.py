"you can use this script to run the support agent example from Chapter 6, Section 2 of the Agentic AI Bible. It will attempt to process a refund request for an order and demonstrate how the support agent handles the task using its defined tools and reasoning capabilities."


from ch06_02_tool_result import run_support_agent

if __name__ == "__main__":
    import os

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY env var to run this example.")
        print("  export ANTHROPIC_API_KEY=your_key_here")
    else:
        result = run_support_agent(
            "I want a refund for a order ch-39."
        )
        print(result)