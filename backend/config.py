"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

# -- Paths ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills"
GENERATED_DIR = BASE_DIR / "generated"
AGENTS_DIR = GENERATED_DIR / "agents"
WORKFLOWS_DIR = GENERATED_DIR / "workflows"

# Ensure output dirs exist
AGENTS_DIR.mkdir(parents=True, exist_ok=True)
WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)

# -- Azure OpenAI -----------------------------------------------------------
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
# AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
# AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
# -- OpenRouter -----------------------------------------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
