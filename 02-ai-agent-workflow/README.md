# AI Agent Workflow

Multi-step agent: Classify -> Research -> Write -> Review (with retry loop).

## Stack
LangGraph, OpenAI GPT-4o, FastAPI, Docker

## Quick Start
    cp .env.example .env
    docker-compose up -d
    curl -X POST http://localhost:8001/api/v1/run -H "Content-Type: application/json" -d '{"input_text":"Analyze this CV: John Doe, 5y Python at Google...","task_type":"cv_analysis"}'
