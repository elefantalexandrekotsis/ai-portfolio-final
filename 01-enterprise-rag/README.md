# Enterprise RAG System

Production RAG with evaluation, monitoring, and cost tracking.

## Architecture

Query -> Guardrails -> Embedding -> Qdrant -> Reranker -> LLM -> Response + Sources + Metrics

## Stack

LangChain, Azure OpenAI, Qdrant, RAGAS, LangSmith, FastAPI, Docker

## Quick Start

    cp .env.example .env
    docker-compose up -d
    curl -X POST http://localhost:8000/api/v1/ingest -H "Content-Type: application/json" -d '{"data_dir":"data/raw"}'
    curl -X POST http://localhost:8000/api/v1/query -H "Content-Type: application/json" -d '{"question":"What is the remote work policy?"}'

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/health | Health check |
| POST | /api/v1/query | Query RAG |
| POST | /api/v1/ingest | Ingest docs |
| GET | /api/v1/costs | Cost summary |
