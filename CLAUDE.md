# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Navigator is a Python POC that uses the Anthropic API to autonomously navigate homedepot.com, find a product, and add it to the cart. It combines AI-driven decision-making with browser automation (Playwright + stealth techniques) to handle Cloudflare protection.

- **Python version:** 3.13
- **OS:** Unix only
- **AI Model:** `claude-sonnet-4-6` (configured in `config.toml`)

## Environment Setup

```bash
# First-time setup: creates venv at ./py-tricentis and installs all deps
./setup.sh

# Activate the venv in future sessions
. py-tricentis/bin/activate

# Create .env in the project root (required before running)
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

## Running the Navigator

```bash
# Default run (uses config.toml)
./navigate_to_checkout.py

# Custom config file
./navigate_to_checkout.py -c path/to/config.toml
```

## Linting

```bash
# PEP8 compliance report (flake8, 90-char line limit)
./linting/pep.sh

# Remove trailing whitespace from Python files
./linting/remove_whitespaces.sh

# Find all TODO comments
./linting/todo.sh
```

## Architecture

```
navigate_to_checkout.py   ← Entry point: parses args, loads config, runs async main
src/
  config.py               ← Config loader: reads config.toml into a dot-access Config object
  browser.py              ← BrowserManager: Playwright launch, stealth setup, teardown
  ai_client.py            ← AIClient: all Anthropic API calls, returns raw dicts
  bypass.py               ← BypassOrchestrator: Cloudflare bypass strategies
  navigator.py            ← Navigator (aliased as AINavigator): thin orchestrator
config.toml               ← All runtime settings — no hardcoded values in Python code
```

### Data Flow

1. `navigate_to_checkout.py` loads `.env`, reads `config.toml` via `src/config.py`, and instantiates `AINavigator`
2. `AINavigator.run(goal)` orchestrates 5 phases:
   - **Phase 1:** Config display via `_setup_phase`
   - **Phase 2:** `BrowserManager.setup_browser()` → returns `(browser, context, page)`; `BypassOrchestrator` is created with the live page
   - **Phase 3:** `BypassOrchestrator.demonstrate_strategies()` tries up to 3 strategies (`Gradual Session Building`, `Multi-Site Credibility`, `Direct with Patience`), each with a configurable timeout; uses `AIClient.analyze_page_status()` for Cloudflare detection
   - **Phase 4A (bypass succeeded):** `_navigate` — calls `AIClient.parse_goal` → `AIClient.analyze_page` → `AIClient.decide_action` → `_execute_action`
   - **Phase 4B (bypass failed):** `_simulate` — `AIClient.simulate_scenario` runs against canned scenarios from `config.toml [simulation_scenarios]`
   - **Phase 5:** Results summary written to `session_results.json`

### Key Design Decisions

- **All config externalized to TOML.** The `Config` class in `config.py` recursively wraps nested dicts so every TOML key is accessible as a Python attribute (e.g., `config.browser.headless`). Never hardcode values in Python files.
- **`AIClient` is injected into `BypassOrchestrator`** so both phases share the same Anthropic client instance without any circular imports.
- **All AI prompts live in `config.toml`** under `[prompts.*]` — changing prompt behavior does not require editing Python files.
- **Tracking stays in `Navigator`:** `bypass_attempts`, `ai_decisions`, and `screenshots` are collected by the orchestrator; `BypassOrchestrator` returns its own lists via properties after `demonstrate_strategies()` completes.
- **Output files** (log, screenshots, JSON summaries) are named by `config.toml` under `[files]`.
