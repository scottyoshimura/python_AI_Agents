"""
Chapter 8 — Planning and Decomposition — Example 2
The Agentic AI Bible (Revised & Expanded Edition 2026)
Companion repository: github.com/agentic-ai-bible/code

Setup:
    pip install -r requirements.txt
    pip install pytest
    export ANTHROPIC_API_KEY=your_key_here

Run:
    python ch08_02_run_tests.py
"""
# ch08_tot_code.py
# Tested against Claude Sonnet 4.6 (claude-sonnet-4-6-20250514),
# Anthropic SDK 0.49.0, as of April 2026.
# Requires: anthropic>=0.49

import json
import os
import re
import subprocess
import tempfile

import anthropic

client = anthropic.Anthropic()

GENERATE_SYSTEM = """
You are a Python expert. Given a function specification, produce a complete Python implementation.
Output ONLY the function definition, no imports unless essential, no explanation.
"""

def sanitize_code(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:python)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()

def run_tests(code: str, tests: str) -> tuple[int, str]:
    """Run tests against a code implementation. Returns (tests_passed, output)."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code + "\n\n" + tests)
        fname = f.name

    try:
        result = subprocess.run(
            ["python", "-m", "pytest", fname, "-v", "--tb=short", "-q"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        combined = (result.stdout + "\n" + result.stderr).strip()
        passed = combined.count(" PASSED")
        return passed, combined[-800:]
    except subprocess.TimeoutExpired:
        return 0, "Timeout: implementation ran for more than 10 seconds"
    finally:
        os.unlink(fname)

def generate_candidates(spec: str, n: int = 3) -> list[str]:
    """Generate N independent implementation candidates for the given spec."""
    candidates = []
    for i in range(n):
        temp_hint = ["standard", "more concise", "more defensive"][i % 3]

        payload = {
            "model": "claude-sonnet-4-6",
            "max_tokens": 512,
            "system": GENERATE_SYSTEM,
            "messages": [
                {
                    "role": "user",
                    "content": f"Spec (write a {temp_hint} implementation):\n{spec}",
                }
            ],
        }

        print("\n=== ANTHROPIC REQUEST PAYLOAD ===")
        print(json.dumps(payload, indent=2))
        print("================================\n")

        response = client.messages.create(**payload)

        print("\n=== ANTHROPIC RAW RESPONSE ===")
        print(response)
        print("================================\n")

        text = sanitize_code(response.content[0].text.strip())
        print("\n=== EXTRACTED TEXT ===")
        print(text)
        print("====================\n")

        candidates.append(text)
    return candidates

def tot_code_generation(spec: str, tests: str, rounds: int = 2) -> str:
    """Use Tree-of-Thoughts to select the best implementation of a function."""
    best_code = None
    best_score = -1
    candidates = []

    for round_num in range(rounds):
        print(f"\n=== ROUND {round_num + 1} ===")
        candidates = generate_candidates(spec)
        print(f"Generated {len(candidates)} candidates")

        for i, candidate in enumerate(candidates):
            print(f"\n--- Candidate {i} ---")
            print(candidate)

        results = [run_tests(c, tests) for c in candidates]
        scores = [r[0] for r in results]
        outputs = [r[1] for r in results]

        print("\n=== TEST RESULTS ===")
        for i, (score, out) in enumerate(zip(scores, outputs)):
            print(f"Candidate {i}: {score} tests passed")
            print(out[:400])
            print()

        round_best_idx = scores.index(max(scores))
        if scores[round_best_idx] > best_score:
            best_score = scores[round_best_idx]
            best_code = candidates[round_best_idx]

        total_tests = tests.count("def test_")
        if best_score >= total_tests:
            print(f"\nBest score reached: {best_score}/{total_tests}")
            break

        spec = spec + "\n\n# Previous attempts and their failures:\n"
        for i, (score, out) in enumerate(zip(scores, outputs)):
            spec += f"# Candidate {i}: {score}/{total_tests} tests passed\n# {out[:200]}\n"

    if best_code is not None:
        return best_code
    return candidates[0] if candidates else ""

if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY env var to run this example.")
        print("  export ANTHROPIC_API_KEY=your_key_here")
    else:
        spec = "Write a function add(a, b) that returns the sum of two numbers."
        tests = """
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
"""
        result = tot_code_generation(spec, tests, rounds=2)
        print("\n=== FINAL WINNER ===")
        print(result)