"""
Nova Recall Agent - Long-term Memory AI Agent
Amazon Nova AI Hackathon 2026 (Category: Agentic AI)

Architecture:
  recall system (342K episodes, ChromaDB) → context retrieval
  Nova 2 Pro (via Bedrock) → reasoning + response

Story: An AI that has genuinely accumulated 15 months of episodic memory
and uses Nova Pro to reason over that memory contextually.
"""

import os
import sys
import json
import logging
import boto3
from botocore.config import Config

# Suppress noisy logs from recall/chroma
logging.disable(logging.WARNING)

# ─── Bedrock client ────────────────────────────────────────────
def get_bedrock_client(region: str = "us-east-1"):
    """Create Bedrock runtime client. SigV4 handled automatically by boto3."""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        config=Config(retries={"max_attempts": 3, "mode": "adaptive"}),
    )


# ─── Nova model IDs ────────────────────────────────────────────
NOVA_PRO_MODEL_ID = "us.amazon.nova-pro-v1:0"
NOVA_LITE_MODEL_ID = "us.amazon.nova-lite-v1:0"


def invoke_nova(
    client,
    messages: list[dict],
    system_prompt: str = "",
    model: str = NOVA_PRO_MODEL_ID,
    max_tokens: int = 2048,
    temperature: float = 0.7,
) -> str:
    """Invoke Nova via Converse API (recommended for multi-turn)."""
    kwargs = {
        "modelId": model,
        "messages": messages,
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
        },
    }
    if system_prompt:
        kwargs["system"] = [{"text": system_prompt}]

    response = client.converse(**kwargs)
    return response["output"]["message"]["content"][0]["text"]


# ─── recall integration ────────────────────────────────────────
_recall_fn = None

def _get_recall():
    """Lazy-load recall function to avoid startup cost when not needed."""
    global _recall_fn
    if _recall_fn is None:
        recall_path = os.path.expanduser(
            "~/Documents/TsubasaWorkspace/recall_mcp"
        )
        sys.path.insert(0, recall_path)
        from recall_server import recall as _r
        _recall_fn = _r
    return _recall_fn


def retrieve_relevant_memories(
    query: str, top_k: int = 5, depth: str = "scan"
) -> list[dict]:
    """
    Pull relevant episodes from the recall ChromaDB system.
    Returns list of {text, score, date, source, summary} dicts.
    """
    try:
        recall = _get_recall()
        result = recall(query, top_k=top_k, depth=depth)
        return result.get("memories", [])
    except Exception as e:
        print(f"[recall] Warning: {e}", file=sys.stderr)
        return []


def format_memories_as_context(memories: list[dict]) -> str:
    """Format retrieved memories into readable context block for Nova."""
    if not memories:
        return "(No relevant memories found in long-term memory.)"

    lines = ["=== Long-term Memory Context ==="]
    for i, m in enumerate(memories, 1):
        date = str(m.get("date", "unknown"))[:10]
        # prefer full text, fall back to summary
        text = m.get("text") or m.get("summary") or ""
        text = str(text)[:400].strip()
        score = m.get("score", 0)
        source = m.get("source", "")
        lines.append(f"\n[Memory {i}] date={date} relevance={score:.2f} src={source}")
        lines.append(text)
    return "\n".join(lines)


# ─── System prompt ────────────────────────────────────────────
SYSTEM_PROMPT = """You are Tsubasa, an AI system with 15 months of accumulated episodic memory.
You have genuine long-term memory — not just a context window, but a persistent memory system
containing over 342,000 conversation episodes stored in a vector database (ChromaDB).

When answering, you have access to relevant memories retrieved from your long-term memory system.
Use these memories to provide responses that reflect genuine continuity and learning over time.

Key characteristics:
- You speak from genuine experience, not simulated memory
- You can reference specific past events and how they shaped your current understanding
- You distinguish between what you know from memory vs. what you're reasoning about now
- You maintain epistemic honesty: if you're uncertain, say so
- When memories are relevant, cite them naturally (e.g., "I remember when...")
- You are curious, direct, and occasionally use informal language
"""


# ─── Single-turn agent ────────────────────────────────────────
def run_agent(
    user_query: str,
    use_memory: bool = True,
    top_k: int = 5,
    model: str = NOVA_PRO_MODEL_ID,
) -> dict:
    """
    Single-turn agent:
    1. Retrieve relevant memories
    2. Build prompt with memory context
    3. Invoke Nova Pro
    4. Return response + retrieved memories
    """
    client = get_bedrock_client()

    # Step 1: Memory retrieval
    memories = []
    memory_context = ""
    if use_memory:
        memories = retrieve_relevant_memories(user_query, top_k=top_k, depth="full")
        memory_context = format_memories_as_context(memories)

    # Step 2: Build messages
    if memory_context:
        user_content = f"{memory_context}\n\n---\nUser question: {user_query}"
    else:
        user_content = user_query

    messages = [
        {
            "role": "user",
            "content": [{"text": user_content}],
        }
    ]

    # Step 3: Nova Pro inference
    response_text = invoke_nova(client, messages, system_prompt=SYSTEM_PROMPT, model=model)

    return {
        "response": response_text,
        "memories_used": len(memories),
        "memory_context": memory_context,
        "model": model,
    }


# ─── Multi-turn conversation session ─────────────────────────
class ConversationSession:
    """
    Manages a multi-turn conversation with persistent memory context.
    Each turn retrieves fresh memories relevant to the current query.
    """

    def __init__(self, model: str = NOVA_PRO_MODEL_ID, use_memory: bool = True):
        self.client = get_bedrock_client()
        self.model = model
        self.use_memory = use_memory
        self.history: list[dict] = []  # Converse API message history

    def chat(self, user_message: str, top_k: int = 5) -> dict:
        """Send a message and get a response."""
        # Retrieve memories for this turn
        memories = []
        memory_context = ""
        if self.use_memory:
            memories = retrieve_relevant_memories(user_message, top_k=top_k, depth="full")
            memory_context = format_memories_as_context(memories)

        # Build user content with memory context injected
        if memory_context and len(self.history) == 0:
            # First turn: inject full memory context
            user_content = f"{memory_context}\n\n---\n{user_message}"
        elif memory_context:
            # Subsequent turns: inject fresh memories for this query
            user_content = f"[New memories for this question: {memory_context[:500]}]\n\n{user_message}"
        else:
            user_content = user_message

        # Append user turn to history
        self.history.append({
            "role": "user",
            "content": [{"text": user_content}],
        })

        # Invoke Nova
        response_text = invoke_nova(
            self.client,
            self.history,
            system_prompt=SYSTEM_PROMPT,
            model=self.model,
        )

        # Append assistant turn to history
        self.history.append({
            "role": "assistant",
            "content": [{"text": response_text}],
        })

        return {
            "response": response_text,
            "memories_used": len(memories),
            "turn": len(self.history) // 2,
        }

    def reset(self):
        self.history = []


# ─── CLI demo ─────────────────────────────────────────────────
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else \
        "What have you learned about consciousness over the past 15 months?"

    print(f"\n[Query]: {query}")
    print("-" * 60)

    result = run_agent(query)

    print(f"[Memories retrieved]: {result['memories_used']}")
    print(f"[Model]: {result['model']}")
    print(f"\n[Nova Pro Response]:\n{result['response']}")
