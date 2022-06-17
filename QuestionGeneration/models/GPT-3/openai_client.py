import logging
import os

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

logging.getLogger("openai").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Client(object):
    """OpenAI Client."""

    def __init__(self):
        """Init."""

    def query(
        self,
        engine: str,
        prompt: str,
        temperature: float,
        max_tokens: int,
        top_p: int,
        frequency_penalty: int,
        presence_penalty: int,
        n: int,
    ) -> str:
        """Query OpenAI with cache."""
        request_params = {
            "engine": engine,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "n": n,
        }
        # cache_key = request_params.copy()
        try:
            response = openai.Completion.create(**request_params)
            return response
        except openai.error.OpenAIError as e:
            logger.error(e)
            raise e