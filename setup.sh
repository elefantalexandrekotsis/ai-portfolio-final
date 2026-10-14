#!/bin/bash
echo "Creating AI Portfolio..."

mkdir -p 01-enterprise-rag/src/{ingestion,retrieval,generation,api,monitoring}
mkdir -p 01-enterprise-rag/{evaluation/datasets,evaluation/reports,tests,data/raw,data/processed,docs}
mkdir -p 02-ai-agent-workflow/src/agents/{nodes,tools}
mkdir -p 02-ai-agent-workflow/src/{api,monitoring}
mkdir -p 02-ai-agent-workflow/{tests,docs}
mkdir -p 03-llm-eval-pipeline/promptfoo/{prompts,datasets}
mkdir -p 03-llm-eval-pipeline/{scripts,reports,docs,.github/workflows}
mkdir -p 04-ai-support-platform/backend/src/{models,ai,api/routes,services}
mkdir -p 04-ai-support-platform/backend/tests
mkdir -p 04-ai-support-platform/frontend/src/{app/chat,app/admin,components,lib}
mkdir -p 04-ai-support-platform/{frontend/public,docs}

for f in \
  01-enterprise-rag/src/__init__.py 01-enterprise-rag/src/ingestion/__init__.py \
  01-enterprise-rag/src/retrieval/__init__.py 01-enterprise-rag/src/generation/__init__.py \
  01-enterprise-rag/src/api/__init__.py 01-enterprise-rag/src/monitoring/__init__.py \
  01-enterprise-rag/evaluation/__init__.py 01-enterprise-rag/tests/__init__.py \
  02-ai-agent-workflow/src/__init__.py 02-ai-agent-workflow/src/agents/__init__.py \
  02-ai-agent-workflow/src/agents/nodes/__init__.py 02-ai-agent-workflow/src/agents/tools/__init__.py \
  02-ai-agent-workflow/src/api/__init__.py 02-ai-agent-workflow/src/monitoring/__init__.py \
  02-ai-agent-workflow/tests/__init__.py \
  04-ai-support-platform/backend/src/__init__.py 04-ai-support-platform/backend/src/models/__init__.py \
  04-ai-support-platform/backend/src/ai/__init__.py 04-ai-support-platform/backend/src/api/__init__.py \
  04-ai-support-platform/backend/src/api/routes/__init__.py \
  04-ai-support-platform/backend/src/services/__init__.py 04-ai-support-platform/backend/tests/__init__.py; do
  touch "$f"
done

touch 01-enterprise-rag/data/raw/.gitkeep 01-enterprise-rag/data/processed/.gitkeep
touch 01-enterprise-rag/evaluation/reports/.gitkeep 03-llm-eval-pipeline/reports/.gitkeep

echo "Directories done"