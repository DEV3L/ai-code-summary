import time

from loguru import logger
from openai import OpenAI

client = OpenAI()


def summarize_content(content: str) -> str:
    start_time = time.time()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are code summary expert. You summarize code in a short way that is easy to understand.",
            },
            {"role": "user", "content": f"Summarize the following code:\n\n{content}"},
        ],
    )
    end_time = time.time()
    logger.debug(f"Summarized content in {end_time - start_time:.2f} seconds")
    return completion.choices[0].message.content
