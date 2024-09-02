import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "${OPENAI_API_KEY}")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # default to mini to keep costs down

SUMMARY_PROMPT = os.getenv(
    "SUMMARY_PROMPT", ("You are code summary expert. You summarize code in a short way that is easy to understand.")
)
