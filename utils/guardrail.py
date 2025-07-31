import json
from prompts.guardrail import INPUT_GUARDRAIL, OUTPUT_GUARDRAIL
import config
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def input_validator(query, json_file_path="schemas/input_guardrail.json"):
    generation_config = config.GENERATION_CONFIG[0]
    with open(json_file_path, "r") as f:
      response_schema = json.load(f)
    generation_config.response_schema = response_schema
    response = config.client.models.generate_content(
    model="gemini-2.5-pro", contents=[INPUT_GUARDRAIL, query], config=generation_config)
    return json.loads(response.text)


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def output_validator(llm_response, json_file_path="schemas/output_guardrail.json"):
    generation_config = config.GENERATION_CONFIG[0]
    with open(json_file_path, "r") as f:
      response_schema = json.load(f)
    generation_config.response_schema = response_schema
    response = config.client.models.generate_content(
    model="gemini-2.5-pro", contents=[OUTPUT_GUARDRAIL, llm_response], config=generation_config)
    return json.loads(response.text)
