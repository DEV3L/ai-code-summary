import time

from loguru import logger
from openai import OpenAI

from ai_code_summary.env_variables import OPENAI_MODEL, SUMMARY_PROMPT

client = OpenAI()


def summarize_content(content: str) -> str:
    start_time = time.time()
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": f"Summarize the following code:\n\n{content}"},
        ],
    )
    end_time = time.time()
    logger.debug(f"Summarized content in {end_time - start_time:.2f} seconds")
    return completion.choices[0].message.content
