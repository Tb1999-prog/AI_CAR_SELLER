import json
from prompts.repharse_query import repharse_query_prompt
import config
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def repharse_query(user_query, chat_history, json_file_path="schemas\\repharse_query.json"):
    generation_config = config.GENERATION_CONFIG[0]
    with open(json_file_path, "r") as f:
        response_schema = json.load(f)
    generation_config.response_schema = response_schema
    rephrased_prompt = repharse_query_prompt.format(
    chat_history=chat_history,
    user_query=user_query
    )
    response = config.client.models.generate_content(
    model="gemini-2.5-pro", contents=[rephrased_prompt], config=generation_config)
    return json.loads(response.text)["repharsed_user_query"]

