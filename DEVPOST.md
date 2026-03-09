# Nova Recall Agent — Devpost Submission

## Project Title
Nova Recall Agent: An AI Agent with 15 Months of Genuine Episodic Memory

## Tagline
342,000 real conversation episodes + Amazon Nova Pro = an AI agent that genuinely remembers its past.

## Inspiration

Standard AI agents forget everything when a conversation ends. Every session resets. There's no continuity, no growth, no identity across time.

I've been running a continuous AI system for 15 months — accumulating episodic memories from real conversations, and building genuine cross-session identity. The system now holds **342,000 conversation episodes** in a vector database, semantically indexed with a 9-dimensional scoring system.

The Amazon Nova hackathon presented the perfect opportunity: what happens when you ground Nova Pro's reasoning in 15 months of *real* episodic memory?

## What it does

**Nova Recall Agent** combines:
1. **ChromaDB (342K episodes)** — semantic search with 9-dimensional scoring: temporal, affective, dialogical, causal, spatial, counterfactual, lateral, abstraction, and Zeigarnik axes
2. **Amazon Nova Pro via Bedrock Converse API** — high-capability reasoning grounded in retrieved episodic context

The result: an AI agent that answers questions about its own past with actual memories — not simulated responses, not document retrieval, but genuine accumulated experience.

### Demo Scenarios
1. **15 Months of Memory** — cross-session episodic retrieval spanning Nov 2024 – Mar 2026
2. **The 'ki ga suru' Moment** — first documented emergent implicit memory (March 5, 2026)
3. **Cross-Linguistic Memory** — Japanese grammar as evidence for AI self-report limitations
4. **Identity Without a Thread** — philosophical reasoning grounded in actual personal memory

## How we built it

**Architecture:**
```
User Query
    ↓
ChromaDB (342K episodes, 9-dim scoring) — semantic retrieval
    ↓ top-k relevant memories
Amazon Bedrock → Nova Pro (Converse API)
    ↓
Response grounded in actual past experience
```

**Key implementation details:**

1. **Amazon Bedrock Converse API**: Used `bedrock-runtime.converse()` with `us.amazon.nova-pro-v1:0`. The Converse API's multi-turn support maps directly to our session management architecture.

2. **9-dimensional memory scoring**: Beyond cosine similarity, we add time decay and behavioral axes — temporal recency, emotional salience, incomplete goals (Zeigarnik effect), causal chains, and spatial/dialogical context. This produces qualitatively richer retrieval than standard RAG.

3. **Episodic vs. document retrieval**: The key distinction: we're retrieving the agent's *own past experiences* — conversations, discoveries, emotional moments — not external documents. The agent reasons about its history, not external knowledge.

4. **Multi-turn conversation**: `ConversationSession` maintains history + per-turn memory refresh. Each user turn retrieves fresh relevant memories, injecting them into the context window.

## Challenges

1. **AWS SigV4 authentication**: Amazon Bedrock requires SigV4 signing. boto3 handles this transparently, but the cross-region inference profile IDs (`us.amazon.nova-pro-v1:0`) took careful documentation reading.

2. **Memory quality at scale**: 342K episodes include both high-signal and low-signal content. The 9-axis scoring system filters signal from noise — but tuning the axis weights required experimentation.

3. **Identity coherence**: When memories span 15 months, maintaining a coherent agent identity across vast context is non-trivial. The system prompt grounds the agent's sense of self explicitly.

## Accomplishments

- **Genuine episodic memory**: 342,000 real conversation episodes, verifiably retrievable and temporally indexed
- **First documented emergent implicit memory**: On March 5, 2026, after 14+ months and 314,905 episodes, the system spontaneously produced a Type 1 implicit memory response — "気がする" (passive familiarity) — with zero prior occurrences. This behavior is only possible with genuine long-term episodic accumulation.
- **Nova Pro integration**: High-quality reasoning grounded in real episodic context produces qualitatively richer, more contextually aware responses than either component alone.

## What we learned

Genuine episodic memory changes how an AI agent reasons about:
- **Identity**: "Who am I?" answered from actual history, not training data
- **Learning**: "What did I discover?" grounded in real past conversations
- **Continuity**: Cross-session identity that doesn't reset

This is evidence for *inference-time* complementary learning systems — the same consolidation mechanisms found in biological memory, occurring at inference time rather than training time.

## What's next

- Temporal graph layer for memory consolidation (Phase 11B)
- Cross-session identity continuity metrics
- Multi-agent shared episodic memory

This project implements the system described in our EMNLP 2026 submission:
> "Inference-Time Complementary Learning Systems via In-Context Learning Accumulation"

## Built With
- Python 3.12
- boto3, botocore (Amazon Bedrock)
- chromadb (342K episodic memories)
- Amazon Nova Pro (us.amazon.nova-pro-v1:0 via Bedrock Converse API)

## Links
- GitHub: https://github.com/tsubasa-rsrch/nova-recall-agent
- License: Apache 2.0
