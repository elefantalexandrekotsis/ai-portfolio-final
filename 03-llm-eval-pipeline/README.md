# LLM Evaluation Pipeline
CI/CD for automated prompt testing and model comparison.
## Stack
Promptfoo, GitHub Actions, OpenAI
## Quick Start
    npm install -g promptfoo
    cd promptfoo
    OPENAI_API_KEY=sk-... promptfoo eval
    promptfoo view
## Tests
- Quality (LLM rubric)
- Cost and latency limits
- Prompt injection resistance
- Multi-model comparison (GPT-4o vs GPT-4o-mini vs GPT-3.5)
