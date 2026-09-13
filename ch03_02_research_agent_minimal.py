"""
Chapter 3 — Anatomy of an Agent — Example 2
The Agentic AI Bible (Revised & Expanded Edition 2026)
Companion repository: github.com/agentic-ai-bible/code
this is a diagram of an agent loop that illustrates how an agent can use a model, memory, and tools to iteratively reason about a task. It shows how the system prompt, model output, tool schemas, and tool runtime interact in a loop until a final answer is produced.

Setup:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=your_key_here

Run:
    python ch03_02_example_02.py
"""

# Agent loop diagram (ASCII art):
_DIAGRAM = """
                    +----------------------+
                    |   SYSTEM PROMPT      |
                    |   + TASK DESCRIPTION |
                    +----------+-----------+
                               |
                               v
      +--------+        +-------------+        +--------------+
      | MEMORY |<------>|    MODEL    |<------>| TOOL SCHEMAS |
      | (ctx)  |        |  (LLM call) |        +------+-------+
      +--------+        +------+------+               |
                               |                      |
                  text or tool |  v emitted           |
                               v                      v
                        +-------------+       +---------------+
                        |     LOOP    +------>|  TOOL RUNTIME |
                        | (this iter) |<------+   (executes)  |
                        +------+------+       +---------------+
                               |
                               | tool_result appended to memory
                               v
                        +--------------+
                        | TERMINATION  |
                        |  CHECK       |--- final_answer? -> return
                        +------+-------+
                               |
                               v
                        (loop again)
"""

if __name__ == '__main__':
    print(_DIAGRAM)
