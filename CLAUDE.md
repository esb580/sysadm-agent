# sysadm-agent — Project Context

## What This Is

A CLI sysadmin agent built from scratch in Python using the Anthropic SDK.
The user types plain English questions; the agent uses tools to inspect the Mac and answer them.

## Learning Goals (in order)

1. Tool/function calling with the Anthropic SDK
2. The ReAct loop (Reason → Act → Observe → repeat)
3. Feeding tool results back to the model correctly
4. Prompt engineering for agents
5. Splitting into subagents with an orchestrator

## Stack

- Python 3.14.3 (pyenv), venv at `.venv/`
- `anthropic` SDK only — no LangChain or agent frameworks
- Agent loop built by hand so the mechanics are visible

## Planned Tools

- `check_disk_usage()` — df output
- `list_top_processes()` — top/ps output
- `check_listening_ports()` — lsof output
- `read_log_file(path)` — tail a log file
- `run_shell_command(cmd)` — general escape hatch

## Key Files

- `agent.py` — main agent loop and tool dispatch
- `tools.py` — tool implementations
- `requirements.txt` — pinned dependencies

## Conventions

- Always activate venv before running: `source .venv/bin/activate`
- API key expected in environment: `ANTHROPIC_API_KEY` (set in `~/.zshrc`)
- Step-by-step development — one concept at a time

## Current Status (as of 2026-03-17)

Scaffolding complete. Both files written and verified. Ready to run.

**Blocked on:** Anthropic API credits — free tier does not allow actual API calls.
First thing next session: buy minimum credits at platform.claude.ai → Billing.

**To test once credits are loaded:**
```bash
source .venv/bin/activate
python agent.py
# ask: "how much disk space do I have?"
```
