import time

from loguru import logger
from openai import OpenAI

from ai_code_summary.env_variables import OPENAI_API_KEY, OPENAI_MODEL, SUMMARY_PROMPT


def _get_open_ai_client() -> OpenAI:
    """
    Initializes and returns an OpenAI client using the provided API key.

    Returns:
        OpenAI: An instance of the OpenAI client.
    """
    return OpenAI(api_key=OPENAI_API_KEY)


def summarize_content(content: str) -> str:
    """
    Summarizes the given content using the OpenAI API.

    Args:
        content (str): The content to be summarized.

    Returns:
        str: The summarized content.
    """
    start_time = time.time()  # Record the start time to measure the duration of the API call
    completion = _get_open_ai_client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": f"Summarize the following code:\n\n{content}"},
        ],
    )
    end_time = time.time()  # Record the end time to measure the duration of the API call
    logger.debug(f"Summarized content in {end_time - start_time:.2f} seconds")  # Log the duration of the API call
    return completion.choices[0].message.content  # Return the summarized content
