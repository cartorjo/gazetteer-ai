# GazetteerAI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> The 48 most-starred open-source AI projects, ranked by live GitHub stars across 15 lifecycle categories.

Last refreshed: 2026-11-03. Stars measure popularity, not quality or production readiness. This file is generated from `data/projects.yaml` by `scripts/build_readme.py`; never hand-edit it.

## Contents

- [Foundations](#foundations)
- [Data, Retrieval and RAG](#data-retrieval-and-rag)
- [Training and Post-Training](#training-and-post-training)
- [Evaluation and Interpretability](#evaluation-and-interpretability)
- [Inference and Local Runtimes](#inference-and-local-runtimes)
- [Agent Frameworks and Workflow Builders](#agent-frameworks-and-workflow-builders)
- [Coding Agents and Harnesses](#coding-agents-and-harnesses)
- [Personal and Multi-Agent Assistants](#personal-and-multi-agent-assistants)
- [Agent Skills and Methodologies](#agent-skills-and-methodologies)
- [Agent Memory and Code Understanding](#agent-memory-and-code-understanding)
- [Chat UIs and Workspaces](#chat-uis-and-workspaces)
- [Generative Media](#generative-media)
- [Vertical AI Apps](#vertical-ai-apps)
- [Safety and Guardrails](#safety-and-guardrails)
- [MLOps and Observability](#mlops-and-observability)
- [Near misses](#near-misses)
- [Rising skills](#rising-skills)
- [Learning and lists](#learning-and-lists)
- [Methodology and data](#methodology-and-data)

## Foundations

Core deep learning frameworks and model-definition libraries. Lifecycle stage: Build.

- [TensorFlow](https://github.com/tensorflow/tensorflow) - Google's end-to-end ML framework. ![stars](https://img.shields.io/github/stars/tensorflow/tensorflow?style=flat-square&label=stars)
- [Transformers](https://github.com/huggingface/transformers) - Model-definition framework for text, vision, audio and multimodal. ![stars](https://img.shields.io/github/stars/huggingface/transformers?style=flat-square&label=stars)
- [PyTorch](https://github.com/pytorch/pytorch) - Tensors and dynamic neural nets with GPU acceleration. ![stars](https://img.shields.io/github/stars/pytorch/pytorch?style=flat-square&label=stars)

## Data, Retrieval and RAG

Ingestion, crawling, OCR, retrieval and vector stores. Lifecycle stage: Data.

- [Firecrawl](https://github.com/firecrawl/firecrawl) - Web search, scrape and interact API for agents. ![stars](https://img.shields.io/github/stars/firecrawl/firecrawl?style=flat-square&label=stars)
- [Agent-Reach](https://github.com/Panniantong/Agent-Reach) - Web, social and repo access with routing. ![stars](https://img.shields.io/github/stars/Panniantong/Agent-Reach?style=flat-square&label=stars)
- [RAGFlow](https://github.com/infiniflow/ragflow) - RAG engine fused with agent capabilities. ![stars](https://img.shields.io/github/stars/infiniflow/ragflow?style=flat-square&label=stars)

Practitioner picks - chosen on adoption, not stars:

- [Docling](https://github.com/docling-project/docling) - Document preparation for gen AI. ![stars](https://img.shields.io/github/stars/docling-project/docling?style=flat-square&label=stars)
- [Milvus](https://github.com/milvus-io/milvus) - Cloud-native vector database. ![stars](https://img.shields.io/github/stars/milvus-io/milvus?style=flat-square&label=stars)
- [LightRAG](https://github.com/HKUDS/LightRAG) - Simple, fast RAG. ![stars](https://img.shields.io/github/stars/HKUDS/LightRAG?style=flat-square&label=stars)
- [GraphRAG](https://github.com/microsoft/graphrag) - Graph-based RAG. ![stars](https://img.shields.io/github/stars/microsoft/graphrag?style=flat-square&label=stars)

## Training and Post-Training

Fine-tuning, distributed training, RLHF/GRPO and PEFT. Lifecycle stage: Train/Align.

Practitioner picks - chosen on adoption, not stars:

- [Unsloth](https://github.com/unslothai/unsloth) - Fast local fine-tuning and training UI. ![stars](https://img.shields.io/github/stars/unslothai/unsloth?style=flat-square&label=stars)
- [LlamaFactory](https://github.com/hiyouga/LlamaFactory) - Unified fine-tuning of 100+ LLMs and VLMs. ![stars](https://img.shields.io/github/stars/hiyouga/LlamaFactory?style=flat-square&label=stars)
- [Ray](https://github.com/ray-project/ray) - Distributed AI compute engine (Train, Data, Serve). ![stars](https://img.shields.io/github/stars/ray-project/ray?style=flat-square&label=stars)
- [DeepSpeed](https://github.com/deepspeedai/DeepSpeed) - ZeRO and distributed training optimization. ![stars](https://img.shields.io/github/stars/deepspeedai/DeepSpeed?style=flat-square&label=stars)
- [verl](https://github.com/verl-project/verl) - RL post-training for LLMs. ![stars](https://img.shields.io/github/stars/verl-project/verl?style=flat-square&label=stars)
- [PEFT](https://github.com/huggingface/peft) - Parameter-efficient fine-tuning. ![stars](https://img.shields.io/github/stars/huggingface/peft?style=flat-square&label=stars)
- [TRL](https://github.com/huggingface/trl) - Post-training (SFT, DPO, GRPO). ![stars](https://img.shields.io/github/stars/huggingface/trl?style=flat-square&label=stars)
- [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) - Large-scale transformer training (Megatron Core). ![stars](https://img.shields.io/github/stars/NVIDIA/Megatron-LM?style=flat-square&label=stars)
- [ms-swift](https://github.com/modelscope/ms-swift) - PEFT, SFT, DPO and GRPO for 600+ LLMs. ![stars](https://img.shields.io/github/stars/modelscope/ms-swift?style=flat-square&label=stars)

## Evaluation and Interpretability

Benchmarks, eval harnesses and mechanistic interpretability. Lifecycle stage: Evaluate.

Practitioner picks - chosen on adoption, not stars:

- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) - The de facto LLM benchmark harness. ![stars](https://img.shields.io/github/stars/EleutherAI/lm-evaluation-harness?style=flat-square&label=stars)
- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) - Mechanistic interpretability library. ![stars](https://img.shields.io/github/stars/TransformerLensOrg/TransformerLens?style=flat-square&label=stars)

## Inference and Local Runtimes

Serving engines, local runtimes and quantization. Lifecycle stage: Serve.

- [Ollama](https://github.com/ollama/ollama) - Run open models locally with one command. ![stars](https://img.shields.io/github/stars/ollama/ollama?style=flat-square&label=stars)
- [llama.cpp](https://github.com/ggml-org/llama.cpp) - LLM inference in C/C++. ![stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat-square&label=stars)
- [vLLM](https://github.com/vllm-project/vllm) - High-throughput, memory-efficient LLM serving. ![stars](https://img.shields.io/github/stars/vllm-project/vllm?style=flat-square&label=stars)

Practitioner picks - chosen on adoption, not stars:

- [SGLang](https://github.com/sgl-project/sglang) - High-performance LLM and multimodal serving. ![stars](https://img.shields.io/github/stars/sgl-project/sglang?style=flat-square&label=stars)
- [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) - Optimized LLM inference on NVIDIA GPUs. ![stars](https://img.shields.io/github/stars/NVIDIA/TensorRT-LLM?style=flat-square&label=stars)
- [FlashInfer](https://github.com/flashinfer-ai/flashinfer) - Kernel library for LLM serving. ![stars](https://img.shields.io/github/stars/flashinfer-ai/flashinfer?style=flat-square&label=stars)

## Agent Frameworks and Workflow Builders

SDKs and visual builders for agents and workflows. Lifecycle stage: Apply.

- [n8n](https://github.com/n8n-io/n8n) - Fair-code workflow automation with native AI agents (license: fair-code). ![stars](https://img.shields.io/github/stars/n8n-io/n8n?style=flat-square&label=stars)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) - Platform for building and running autonomous agents (license: mixed). ![stars](https://img.shields.io/github/stars/Significant-Gravitas/AutoGPT?style=flat-square&label=stars)
- [Dify](https://github.com/langgenius/dify) - Agentic workflows and RAG pipelines in one workspace (license: modified-apache). ![stars](https://img.shields.io/github/stars/langgenius/dify?style=flat-square&label=stars)
- [Langflow](https://github.com/langflow-ai/langflow) - Visual builder for agents and workflows. ![stars](https://img.shields.io/github/stars/langflow-ai/langflow?style=flat-square&label=stars)
- [LangChain](https://github.com/langchain-ai/langchain) - The agent engineering framework. ![stars](https://img.shields.io/github/stars/langchain-ai/langchain?style=flat-square&label=stars)
- [browser-use](https://github.com/browser-use/browser-use) - Python library for AI browser agents. ![stars](https://img.shields.io/github/stars/browser-use/browser-use?style=flat-square&label=stars)

Practitioner picks - chosen on adoption, not stars:

- [CrewAI](https://github.com/crewAIInc/crewAI) - Role-playing multi-agent orchestration. ![stars](https://img.shields.io/github/stars/crewAIInc/crewAI?style=flat-square&label=stars)
- [LangGraph](https://github.com/langchain-ai/langgraph) - Resilient stateful agents. ![stars](https://img.shields.io/github/stars/langchain-ai/langgraph?style=flat-square&label=stars)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - OpenAI's multi-agent workflow SDK. ![stars](https://img.shields.io/github/stars/openai/openai-agents-python?style=flat-square&label=stars)

## Coding Agents and Harnesses

Terminal and IDE coding agents and harness runtimes. Lifecycle stage: Apply.

- [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) - "everything is a plugin" agent harness. ![stars](https://img.shields.io/github/stars/deepseek-ai/deepseek-harness?style=flat-square&label=stars)
- [OpenCode](https://github.com/anomalyco/opencode) - Provider-agnostic terminal coding agent. ![stars](https://img.shields.io/github/stars/anomalyco/opencode?style=flat-square&label=stars)
- [cc-switch](https://github.com/farion1231/cc-switch) - Desktop switcher for Claude Code, Codex, OpenCode and more. ![stars](https://img.shields.io/github/stars/farion1231/cc-switch?style=flat-square&label=stars)
- [Codex](https://github.com/openai/codex) - OpenAI's Rust terminal coding agent. ![stars](https://img.shields.io/github/stars/openai/codex?style=flat-square&label=stars)
- [pi](https://github.com/earendil-works/pi) - Unified LLM API, agent loop, TUI and coding CLI. ![stars](https://img.shields.io/github/stars/earendil-works/pi?style=flat-square&label=stars)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli) - Google's open-source Gemini terminal agent. ![stars](https://img.shields.io/github/stars/google-gemini/gemini-cli?style=flat-square&label=stars)

## Personal and Multi-Agent Assistants

Always-on assistants and agent fleet managers. Lifecycle stage: Apply.

- [OpenClaw](https://github.com/openclaw/openclaw) - Personal AI assistant on any OS and channel. ![stars](https://img.shields.io/github/stars/openclaw/openclaw?style=flat-square&label=stars)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - Self-improving agent with a learning loop. ![stars](https://img.shields.io/github/stars/NousResearch/hermes-agent?style=flat-square&label=stars)
- [Orca](https://github.com/stablyai/orca) - Desktop orchestrator running coding agents in parallel worktrees. ![stars](https://img.shields.io/github/stars/stablyai/orca?style=flat-square&label=stars)
- [Paperclip](https://github.com/paperclipai/paperclip) - Manage fleets of agents at work. ![stars](https://img.shields.io/github/stars/paperclipai/paperclip?style=flat-square&label=stars)

## Agent Skills and Methodologies

SKILL.md packs, personas and spec-driven methods. Lifecycle stage: Apply.

- [superpowers](https://github.com/obra/superpowers) - Spec, plan, TDD and subagent-driven development skills. ![stars](https://img.shields.io/github/stars/obra/superpowers?style=flat-square&label=stars)
- [mattpocock/skills](https://github.com/mattpocock/skills) - Small, composable engineering skills for coding agents. ![stars](https://img.shields.io/github/stars/mattpocock/skills?style=flat-square&label=stars)
- [ECC](https://github.com/affaan-m/ECC) - Skills, instincts, memory and security for agent harnesses. ![stars](https://img.shields.io/github/stars/affaan-m/ECC?style=flat-square&label=stars)
- [anthropics/skills](https://github.com/anthropics/skills) - Anthropic's public skills for Claude, from documents to MCP generation (license: mixed). ![stars](https://img.shields.io/github/stars/anthropics/skills?style=flat-square&label=stars)
- [ponytail](https://github.com/DietrichGebert/ponytail) - Simplicity and YAGNI decision discipline. ![stars](https://img.shields.io/github/stars/DietrichGebert/ponytail?style=flat-square&label=stars)
- [agency-agents](https://github.com/msitarzewski/agency-agents) - Roster of specialized expert agent personas. ![stars](https://img.shields.io/github/stars/msitarzewski/agency-agents?style=flat-square&label=stars)
- [spec-kit](https://github.com/github/spec-kit) - GitHub's spec-driven development toolkit. ![stars](https://img.shields.io/github/stars/github/spec-kit?style=flat-square&label=stars)
- [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - UI/UX design intelligence skill. ![stars](https://img.shields.io/github/stars/nextlevelbuilder/ui-ux-pro-max-skill?style=flat-square&label=stars)
- [gstack](https://github.com/garrytan/gstack) - Opinionated Claude Code role toolkit (CEO, eng, QA). ![stars](https://img.shields.io/github/stars/garrytan/gstack?style=flat-square&label=stars)
- [caveman](https://github.com/JuliusBrussee/caveman) - Token-cutting terse-output skill and proxy. ![stars](https://img.shields.io/github/stars/JuliusBrussee/caveman?style=flat-square&label=stars)
- [agent-skills](https://github.com/addyosmani/agent-skills) - Production-grade engineering skills. ![stars](https://img.shields.io/github/stars/addyosmani/agent-skills?style=flat-square&label=stars)
- [taste-skill](https://github.com/Leonxlnx/taste-skill) - Anti-generic "good taste" design skill. ![stars](https://img.shields.io/github/stars/Leonxlnx/taste-skill?style=flat-square&label=stars)
- [Impeccable](https://github.com/pbakaus/impeccable) - Design skills and a slop detector for coding agents. ![stars](https://img.shields.io/github/stars/pbakaus/impeccable?style=flat-square&label=stars)

## Agent Memory and Code Understanding

Persistent memory and code knowledge graphs. Lifecycle stage: Apply.

- [graphify](https://github.com/Graphify-Labs/graphify) - Queryable code and document knowledge graph. ![stars](https://img.shields.io/github/stars/Graphify-Labs/graphify?style=flat-square&label=stars)
- [claude-mem](https://github.com/thedotmack/claude-mem) - Persistent cross-session agent memory. ![stars](https://img.shields.io/github/stars/thedotmack/claude-mem?style=flat-square&label=stars)
- [archify](https://github.com/tt-a1i/archify) - Codebases and plans as interactive diagrams. ![stars](https://img.shields.io/github/stars/tt-a1i/archify?style=flat-square&label=stars)

Practitioner picks - chosen on adoption, not stars:

- [Mem0](https://github.com/mem0ai/mem0) - Memory layer for AI agents. ![stars](https://img.shields.io/github/stars/mem0ai/mem0?style=flat-square&label=stars)

## Chat UIs and Workspaces

End-user chat front-ends. Lifecycle stage: Apply.

- [Open WebUI](https://github.com/open-webui/open-webui) - Self-hosted UI for Ollama and OpenAI-compatible APIs (license: modified-bsd). ![stars](https://img.shields.io/github/stars/open-webui/open-webui?style=flat-square&label=stars)

## Generative Media

Image, video and audio generation tooling. Lifecycle stage: Apply.

- [ComfyUI](https://github.com/Comfy-Org/ComfyUI) - Node-graph diffusion GUI, API and backend. ![stars](https://img.shields.io/github/stars/Comfy-Org/ComfyUI?style=flat-square&label=stars)
- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) - Topic-to-HD short video pipeline. ![stars](https://img.shields.io/github/stars/harry0703/MoneyPrinterTurbo?style=flat-square&label=stars)

## Vertical AI Apps

Domain applications. Lifecycle stage: Apply.

- [REA](https://github.com/morluto/rea) - Reverse engineering of apps and binaries through one MCP server. ![stars](https://img.shields.io/github/stars/morluto/rea?style=flat-square&label=stars)
- [TradingAgents](https://github.com/TauricResearch/TradingAgents) - Multi-agent LLM trading framework. ![stars](https://img.shields.io/github/stars/TauricResearch/TradingAgents?style=flat-square&label=stars)
- [open-design](https://github.com/nexu-io/open-design) - Coding agent as design engine (prototypes, slides, video). ![stars](https://img.shields.io/github/stars/nexu-io/open-design?style=flat-square&label=stars)
- [RuView](https://github.com/ruvnet/RuView) - WiFi signal sensing for pose, breathing and presence detection. ![stars](https://img.shields.io/github/stars/ruvnet/RuView?style=flat-square&label=stars)

## Safety and Guardrails

Input and output filtering and policy enforcement. Lifecycle stage: Govern.

Practitioner picks - chosen on adoption, not stars:

- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) - Programmable guardrails for LLM apps. ![stars](https://img.shields.io/github/stars/NVIDIA-NeMo/Guardrails?style=flat-square&label=stars)

## MLOps and Observability

Tracking, tracing, gateways and evals in production. Lifecycle stage: Operate.

Practitioner picks - chosen on adoption, not stars:

- [LiteLLM](https://github.com/BerriAI/litellm) - AI gateway for 100+ LLM APIs with cost tracking (license: mixed). ![stars](https://img.shields.io/github/stars/BerriAI/litellm?style=flat-square&label=stars)
- [Langfuse](https://github.com/langfuse/langfuse) - Open-source agent evals and observability (license: mixed). ![stars](https://img.shields.io/github/stars/langfuse/langfuse?style=flat-square&label=stars)
- [MLflow](https://github.com/mlflow/mlflow) - AI engineering platform for agents, LLMs and ML models. ![stars](https://img.shields.io/github/stars/mlflow/mlflow?style=flat-square&label=stars)

## Near misses

Ranks 49 to 53. They enter the list automatically when they overtake an entry above.

- [OpenHands](https://github.com/OpenHands/OpenHands) - AI-driven software development platform. ![stars](https://img.shields.io/github/stars/OpenHands/OpenHands?style=flat-square&label=stars)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - PDFs and images to LLM-ready structured data. ![stars](https://img.shields.io/github/stars/PaddlePaddle/PaddleOCR?style=flat-square&label=stars)
- [OpenCV](https://github.com/opencv/opencv) - Computer vision library with a deep learning module. ![stars](https://img.shields.io/github/stars/opencv/opencv?style=flat-square&label=stars)
- [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) - Interactive codebase knowledge graph. ![stars](https://img.shields.io/github/stars/Egonex-AI/Understand-Anything?style=flat-square&label=stars)
- [worldmonitor](https://github.com/koala73/worldmonitor) - AI-powered global news and situational dashboard. ![stars](https://img.shields.io/github/stars/koala73/worldmonitor?style=flat-square&label=stars)

## Rising skills

Niche agent skills that are growing fast but are well below the ranking threshold. Unranked.

- [last30days-skill](https://github.com/mvanhorn/last30days-skill) - Recent multi-source research. ![stars](https://img.shields.io/github/stars/mvanhorn/last30days-skill?style=flat-square&label=stars)
- [user-research-skill](https://github.com/cookiy-ai/user-research-skill) - Qualitative and quantitative user research. ![stars](https://img.shields.io/github/stars/cookiy-ai/user-research-skill?style=flat-square&label=stars)

## Learning and lists

Courses, books, curated lists and prompt collections. Reading material is never ranked.

- [prompts.chat](https://github.com/f/prompts.chat) - Curated prompt collection (formerly awesome-chatgpt-prompts). ![stars](https://img.shields.io/github/stars/f/prompts.chat?style=flat-square&label=stars)
- [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) - Collection of LLM app examples with agents and RAG. ![stars](https://img.shields.io/github/stars/Shubhamsaboo/awesome-llm-apps?style=flat-square&label=stars)
- [generative-ai-for-beginners](https://github.com/microsoft/generative-ai-for-beginners) - Microsoft's 21-lesson generative AI course. ![stars](https://img.shields.io/github/stars/microsoft/generative-ai-for-beginners?style=flat-square&label=stars)
- [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) - Build a GPT-style LLM step by step in PyTorch. ![stars](https://img.shields.io/github/stars/rasbt/LLMs-from-scratch?style=flat-square&label=stars)
- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) - Curated list of MCP servers. ![stars](https://img.shields.io/github/stars/punkpeye/awesome-mcp-servers?style=flat-square&label=stars)
- [ML-For-Beginners](https://github.com/microsoft/ML-For-Beginners) - 12-week classic machine learning curriculum. ![stars](https://img.shields.io/github/stars/microsoft/ML-For-Beginners?style=flat-square&label=stars)
- [hello-agents](https://github.com/datawhalechina/hello-agents) - Chinese tutorial on building agents from scratch. ![stars](https://img.shields.io/github/stars/datawhalechina/hello-agents?style=flat-square&label=stars)
- [awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) - Curated list of plugins for DeepSeek Harness. ![stars](https://img.shields.io/github/stars/awesome-dsh-plugin/awesome-dsh-plugin?style=flat-square&label=stars)

## Methodology and data

- [Full ranking](https://github.com/cartorjo/gazetteer-ai/blob/main/docs/RANKING.md) - Every ranked entry with stars, forks, license and last push, plus entries under review and exclusions.
- [Methodology](https://github.com/cartorjo/gazetteer-ai/blob/main/docs/METHODOLOGY.md) - Inclusion criteria, exclusions, data sources and caveats.
- [Claude Code tooling guide](https://github.com/cartorjo/gazetteer-ai/blob/main/docs/CLAUDE-TOOLING.md) - How to install and use the top Claude Code-installable projects from this list.
- [Weekly routine prompt](https://github.com/cartorjo/gazetteer-ai/blob/main/docs/ROUTINE_PROMPT.md) - The prompt the weekly refresh routine runs.

## Contributing

Read [CONTRIBUTING.md](https://github.com/cartorjo/gazetteer-ai/blob/main/CONTRIBUTING.md) first. Open an issue with the "Add a project" template or send a PR that edits `data/projects.yaml` only; the README is regenerated by CI.
