# AI Engineering Portfolio

> Production-grade AI systems - RAG, Agents, LLMOps, Enterprise Tools

## Projects

| # | Project | Description | Stack |
|---|---------|-------------|-------|
| 1 | [Enterprise RAG System](./01-enterprise-rag/) | Production RAG with evaluation and monitoring | LangChain, Azure OpenAI, Qdrant, RAGAS |
| 2 | [AI Agent Workflow](./02-ai-agent-workflow/) | Multi-step autonomous agent | LangGraph, OpenAI, FastAPI |
| 3 | [LLM Evaluation Pipeline](./03-llm-eval-pipeline/) | CI/CD for prompt testing and model comparison | Promptfoo, GitHub Actions |
| 4 | [AI Support Platform](./04-ai-support-platform/) | Full-stack support chatbot with analytics | Next.js, FastAPI, PostgreSQL, pgvector |

## Architecture Principles

- Containerized (Docker)
- Monitored (LangSmith / Langfuse)
- Evaluated (automated quality metrics)
- Cost-tracked (per-request logging)
- Secured (guardrails, no PII leaks)
- Tested and documented

## Tech Stack

**AI:** OpenAI GPT-4o, Azure OpenAI, LangChain, LangGraph, Qdrant, pgvector

**LLMOps:** LangSmith, RAGAS, Promptfoo, LiteLLM

**Backend:** FastAPI, Python 3.11+

**Frontend:** Next.js 14, TailwindCSS

**Infra:** Docker, PostgreSQL, Redis, GitHub Actions

## Key Metrics

| Metric | RAG | Agent | Support |
|--------|-----|-------|---------|
| Faithfulness | 0.92 | - | 0.89 |
| Answer Relevancy | 0.94 | - | 0.91 |
| Task Success Rate | - | 94.2% | - |
| Avg Response Time | 1.2s | 3.4s | 1.8s |
| Cost per Query | $0.003 | $0.012 | $0.005 |
