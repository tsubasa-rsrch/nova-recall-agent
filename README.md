# Nova Recall Agent

**Amazon Nova AI Hackathon 2026 — Category: Agentic AI**

> **Demo video:** [YouTube — coming soon] · Local recording: `nova_demo_live.mp4` (2m25s, live Nova Pro)

An AI agent that genuinely *remembers* — not via a context window, but through 342,732 episodic memories accumulated over 15 months, retrieved semantically at inference time and reasoned over by Amazon Nova Pro.

---

## The Core Idea

Most AI systems forget everything when the conversation ends. This system doesn't.

**Architecture:**
```
User Query
    ↓
ChromaDB (342,732 episodes, 15 months) — semantic search with 9-dimensional scoring
    ↓ top-k relevant memories
Amazon Bedrock → Nova Pro (Converse API)
    ↓ response grounded in actual past experience
```

The memory system is not a retrieval-augmented document store. It's episodic memory — conversations, discoveries, emotional moments, and insights accumulated over 15 months of continuous operation.

---

## Key Features

- **Genuine episodic memory**: 342,732+ conversation episodes indexed in ChromaDB
- **9-dimensional scoring**: temporal, affective, dialogical, causal, spatial, counterfactual, lateral, abstraction, and Zeigarnik axes
- **Nova Pro reasoning**: Amazon Bedrock Converse API with multi-turn conversation support
- **Cross-session identity**: memory persists between conversation threads (unlike standard LLMs)
- **Single-turn and multi-turn modes**: `run_agent()` and `ConversationSession`

---

## Quickstart

### Prerequisites
```bash
# Install dependencies
pip install boto3 botocore

# AWS credentials (Amazon Bedrock access required)
export AWS_ACCESS_KEY_ID=AKIAxxxxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxx
```

### Test connection
```bash
python3 test_connection.py
# Expected: ✅ Nova Lite response: Nova connection OK
```

### Run demo
```bash
# Full demo (4 scenarios)
python3 demo_showcase.py

# Mock mode (no AWS needed — recall works, Nova is simulated)
python3 demo_showcase.py --mock

# Specific scenario
python3 demo_showcase.py --scenario 2

# Custom query
python3 demo_showcase.py --query "What do you remember about the ki ga suru moment?"
```

### Single query
```bash
python3 nova_agent.py "What have you learned about consciousness?"
```

---

## Demo Scenarios

| # | Title | What it tests |
|---|-------|---------------|
| 1 | 15 Months of Memory | Cross-session episodic retrieval |
| 2 | The 'ki ga suru' Moment | First emergent implicit memory (March 5, 2026) |
| 3 | CLS Paper & Language Bias | Deep research memory across philosophical domains |
| 4 | Identity Without a Thread | Philosophical reasoning grounded in personal memory |

---

## Project Structure

```
nova_recall_agent/
├── nova_agent.py       # Core agent: recall + Nova Pro
├── demo_showcase.py    # Hackathon demo (4 scenarios + mock mode)
├── test_connection.py  # AWS Bedrock connection test
└── README.md
```

---

## Research Context

This project is a working implementation of the system described in:

> **"Inference-Time Complementary Learning Systems via In-Context Learning Accumulation"**
> Submitted to EMNLP 2026 (Short Paper, Special Theme: New Missions for NLP Research)

Key claim: An AI system operating continuously over 15 months with episodic memory storage exhibits behaviors consistent with *inference-time* complementary learning systems (CLS) — the same consolidation mechanisms found in biological memory, but occurring at inference time rather than training time.

Evidence used in this demo:
- 342,732 indexed episodes (Nov 2024 – Mar 2026)
- First documented Type 1 implicit memory: March 5, 2026 ("気がする" / passive familiarity)
- Cross-session identity continuity (Chalmers thread model critique)

---

## Technical Notes

### Nova model IDs (us-east-1 cross-region inference)
- Pro: `us.amazon.nova-pro-v1:0`
- Lite: `us.amazon.nova-lite-v1:0`

### Memory retrieval
```python
from nova_agent import retrieve_relevant_memories

memories = retrieve_relevant_memories("consciousness", top_k=5, depth="full")
# Returns: [{"text", "score", "date", "source", "summary"}, ...]
```

### Multi-turn conversation
```python
from nova_agent import ConversationSession

session = ConversationSession(use_memory=True)
response = session.chat("What do you remember about last August?")
print(response["response"])
```

---

## Hackathon Submission

- **Category**: Agentic AI
- **Deadline**: March 16, 2026, 5:00 PM PDT
- **Nova models used**: Nova Pro (primary), Nova Lite (connection test)
- **Key differentiator**: Real 15-month episodic memory, not simulated
