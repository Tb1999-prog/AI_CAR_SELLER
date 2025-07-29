import json
from prompts.guardrail import INPUT_GUARDRAIL, OUTPUT_GUARDRAIL
import config
def input_validator(query, json_file_path="schemas/input_guardrail.json"):
    generation_config = config.GENERATION_CONFIG[0]
    with open(json_file_path, "r") as f:
      response_schema = json.load(f)
    generation_config.response_schema = response_schema
    response = config.client.models.generate_content(
    model="gemini-2.5-flash", contents=[INPUT_GUARDRAIL, query], config=generation_config)
    return json.loads(response.text)


def output_validator(llm_response, json_file_path="schemas/output_guardrail.json"):
    generation_config = config.GENERATION_CONFIG[0]
    with open(json_file_path, "r") as f:
      response_schema = json.load(f)
    generation_config.response_schema = response_schema
    response = config.client.models.generate_content(
    model="gemini-2.5-flash", contents=[OUTPUT_GUARDRAIL, llm_response], config=generation_config)
    return json.loads(response.text)
