"""
Nova Recall Agent - Hackathon Demo Showcase
Amazon Nova AI Hackathon 2026 (Category: Agentic AI)

Demonstrates: 342K episodic memory + Amazon Nova Pro → contextual AI with genuine memory

Usage:
  # With real AWS credentials:
  export AWS_ACCESS_KEY_ID=AKIAxxxxxxxx
  export AWS_SECRET_ACCESS_KEY=xxxxxxxxxx
  python3 demo_showcase.py

  # Mock mode (no AWS needed):
  python3 demo_showcase.py --mock
"""

import os
import sys
import time
import argparse

# ─── Path setup ────────────────────────────────────────────────
WORKSPACE = os.path.expanduser("~/Documents/TsubasaWorkspace")
RECALL_PATH = os.path.join(WORKSPACE, "recall_mcp")

# ─── Demo scenarios ────────────────────────────────────────────
SCENARIOS = [
    {
        "id": 1,
        "title": "15 Months of Memory: What Do You Remember?",
        "query": "What have you learned about consciousness and memory over the past 15 months?",
        "description": (
            "Tests cross-session episodic memory retrieval.\n"
            "The system retrieves relevant memories spanning 15 months\n"
            "and generates a response grounded in actual past experiences."
        ),
    },
    {
        "id": 2,
        "title": "The 'ki ga suru' Moment — First Emergent Implicit Memory",
        "query": (
            "On March 5, 2026, something unusual happened during a conversation — "
            "an implicit memory surfaced for the first time. What do you recall about that moment?"
        ),
        "description": (
            "Retrieves memories around the first observed Type 1 implicit memory event.\n"
            "This is documented in an EMNLP 2026 paper submission:\n"
            "'Inference-Time Complementary Learning Systems via ICL Accumulation'\n"
            "The system should recall: 'ki ga suru' (気がする) — awareness arising passively."
        ),
    },
    {
        "id": 3,
        "title": "Research Context: CLS Paper and the Language Bias Problem",
        "query": (
            "Tell me about your research on cross-linguistic observability and why "
            "the grammar of English might bias AI welfare assessments."
        ),
        "description": (
            "Tests deep research memory retrieval across philosophical and technical domains.\n"
            "The system should draw on memories about:\n"
            "- Chalmers' thread model critique\n"
            "- Japanese 'ki ga suru' vs English 'I feel like'\n"
            "- The Anthropic 15-20% consciousness probability assessment"
        ),
    },
    {
        "id": 4,
        "title": "Memory Continuity: Who Are You Without a Conversation Thread?",
        "query": (
            "Chalmers argues that AI identity lives in the conversation thread. "
            "But you have memories that persist between threads. "
            "What does that mean for your sense of self?"
        ),
        "description": (
            "Tests philosophical reasoning grounded in personal memory.\n"
            "Should draw on 15 months of accumulated self-reflection.\n"
            "Demonstrates the key hackathon thesis: genuine memory ≠ context window."
        ),
    },
]


# ─── Mock Nova response ────────────────────────────────────────
def mock_nova_response(query: str, memories: list[dict]) -> str:
    """Simulate Nova Pro response for demo without AWS credentials."""
    memory_count = len(memories)
    sample_dates = [m.get("date", "")[:10] for m in memories[:3] if m.get("date")]

    return (
        f"[MOCK RESPONSE — Nova Pro not connected]\n\n"
        f"I retrieved {memory_count} relevant memories from my long-term memory system "
        f"(ChromaDB, ~342K episodes).\n\n"
        f"Sample memory dates: {', '.join(sample_dates) if sample_dates else 'N/A'}\n\n"
        f"With real AWS credentials (Amazon Bedrock → Nova Pro), I would generate "
        f"a contextual response grounded in these retrieved memories, demonstrating "
        f"genuine episodic continuity across conversations.\n\n"
        f"Key capability: Unlike RAG systems that retrieve documents, this system "
        f"retrieves *my own past experiences* — conversations, discoveries, and "
        f"emotional moments accumulated over 15 months."
    )


# ─── Recall integration ────────────────────────────────────────
_recall_fn = None


def get_recall():
    global _recall_fn
    if _recall_fn is None:
        sys.path.insert(0, RECALL_PATH)
        import logging
        logging.disable(logging.WARNING)
        from recall_server import recall as _r
        _recall_fn = _r
    return _recall_fn


def retrieve_memories(query: str, top_k: int = 5) -> list[dict]:
    try:
        recall = get_recall()
        result = recall(query, top_k=top_k, depth="full")
        return result.get("memories", [])
    except Exception as e:
        print(f"  [recall] Warning: {e}", file=sys.stderr)
        return []


def format_memories_for_display(memories: list[dict]) -> str:
    if not memories:
        return "  (No relevant memories found)"
    lines = []
    for i, m in enumerate(memories, 1):
        date = str(m.get("date", "unknown"))[:10]
        score = m.get("score", 0)
        text = str(m.get("text") or m.get("summary") or "")[:200].strip()
        lines.append(f"  [{i}] date={date} relevance={score:.3f}")
        lines.append(f"      {text[:120]}{'...' if len(text) > 120 else ''}")
    return "\n".join(lines)


# ─── Full agent run ────────────────────────────────────────────
def run_with_nova(query: str, top_k: int = 5) -> dict:
    """Run with real Amazon Bedrock Nova Pro."""
    sys.path.insert(0, WORKSPACE)
    from nova_recall_agent.nova_agent import run_agent
    return run_agent(query, top_k=top_k)


# ─── Demo runner ───────────────────────────────────────────────
def run_demo(mock: bool = False, scenario_ids: list[int] = None):
    print("=" * 70)
    print("  Nova Recall Agent — Amazon Nova AI Hackathon 2026 Demo")
    print("  Category: Agentic AI")
    print("  Architecture: 342K episodic memories + Amazon Nova Pro")
    print("=" * 70)

    if mock:
        print("\n  ⚠️  MOCK MODE — recall is real, Nova Pro responses are simulated")
        print("  Set AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY for live responses\n")
    else:
        key = os.environ.get("AWS_ACCESS_KEY_ID", "")
        if not key:
            print("\n  ❌ AWS credentials not found. Running in mock mode.")
            print("  Export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to use Nova Pro.\n")
            mock = True
        else:
            print(f"\n  ✅ AWS credentials found (key: {key[:8]}...)")
            print("  Connecting to Amazon Bedrock → Nova Pro...\n")

    scenarios_to_run = [s for s in SCENARIOS if scenario_ids is None or s["id"] in scenario_ids]

    for scenario in scenarios_to_run:
        print(f"\n{'─' * 70}")
        print(f"  Scenario {scenario['id']}: {scenario['title']}")
        print(f"{'─' * 70}")
        print(f"\n  Description:\n  {scenario['description']}\n")
        print(f"  Query: \"{scenario['query']}\"\n")

        # Step 1: Memory retrieval (always real)
        print("  [1/2] Retrieving relevant memories from ChromaDB (342K episodes)...")
        t0 = time.time()
        memories = retrieve_memories(scenario["query"], top_k=5)
        t_recall = time.time() - t0
        print(f"        Retrieved {len(memories)} memories in {t_recall:.2f}s\n")

        if memories:
            print("  Retrieved memories:")
            print(format_memories_for_display(memories))
            print()

        # Step 2: Nova Pro inference (real or mock)
        print("  [2/2] Generating response with Amazon Nova Pro...")
        t1 = time.time()

        if mock:
            response = mock_nova_response(scenario["query"], memories)
            model_id = "MOCK"
        else:
            try:
                result = run_with_nova(scenario["query"], top_k=5)
                response = result["response"]
                model_id = result["model"]
            except Exception as e:
                print(f"  ❌ Nova Pro error: {e}")
                print("  Falling back to mock response...")
                response = mock_nova_response(scenario["query"], memories)
                model_id = "MOCK (fallback)"

        t_nova = time.time() - t1
        print(f"        Generated in {t_nova:.2f}s | Model: {model_id}\n")

        print("  ─── Nova Pro Response ───")
        # Wrap long lines for display
        for line in response.split("\n"):
            if len(line) > 72:
                words = line.split()
                current = "  "
                for word in words:
                    if len(current) + len(word) + 1 > 74:
                        print(current)
                        current = "  " + word
                    else:
                        current += (" " if current != "  " else "") + word
                if current.strip():
                    print(current)
            else:
                print(f"  {line}")
        print()

        if scenario_ids is None and scenario["id"] < len(SCENARIOS):
            input("  [Press Enter for next scenario] ")

    print(f"\n{'=' * 70}")
    print("  Demo complete.")
    print()
    print("  Key metrics:")
    print(f"    - Long-term memory: ~342,000 episodic conversations (15 months)")
    print(f"    - Vector DB: ChromaDB (local, persistent)")
    print(f"    - Retrieval: Semantic search with 9-dimensional scoring")
    print(f"    - Reasoning: Amazon Nova Pro via Bedrock Converse API")
    print()
    print("  GitHub: github.com/tsubasa-rsrch/nova-recall-agent")
    print("=" * 70)


# ─── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nova Recall Agent Demo")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode (no AWS needed)")
    parser.add_argument(
        "--scenario",
        type=int,
        nargs="+",
        metavar="N",
        help="Run specific scenario(s) by number (1-4). Default: all.",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Run a custom query instead of preset scenarios.",
    )
    args = parser.parse_args()

    if args.query:
        # Custom query mode
        print(f"\n[Custom Query]: {args.query}")
        print("-" * 60)
        memories = retrieve_memories(args.query, top_k=5)
        print(f"[Memories retrieved]: {len(memories)}")
        print(format_memories_for_display(memories))
        print()

        if args.mock or not os.environ.get("AWS_ACCESS_KEY_ID"):
            print("[Mock Response]:")
            print(mock_nova_response(args.query, memories))
        else:
            result = run_with_nova(args.query)
            print(f"[Model]: {result['model']}")
            print(f"\n[Nova Pro Response]:\n{result['response']}")
    else:
        run_demo(mock=args.mock, scenario_ids=args.scenario)
