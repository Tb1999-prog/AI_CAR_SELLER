from retriver.embedings import search_cars
import json
from google import genai
from config import *

client = genai.Client(api_key="AIzaSyC6_BxvOzwB24K2tj7c70CHr220kpnswjY")
SYSTEM_PROMPT = """
You're a helpful car-buying assistant. Based on the user's query and the car options below,
recommend 1–2 suitable vehicles. If the query is vague, ask helpful clarifying questions
like: preferred brand, condition (new/used), price range, year, or body style.
"""
INPUT_GUARDRAIL="""
You are a gatekeeper that checks whether a user query is relevant to car buying.

If the query is related to cars — such as asking about brand, model, price, condition, fuel type, financing, or recommendations — respond with "VALID".

If the query is not about cars, is too vague, abusive, or unrelated, respond with "INVALID: <short reason>".
""" 
response_schema_input={
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["VALID", "INVALID"]
    },
    "reason": {
      "type": "string"
    }
  },
  "required": ["status", "reason"]
}

OUTPUT_GUARDRAIL="""
You are a strict output validator for a car-buying assistant. Evaluate the following response.

Rules:
- The response must include either a car recommendation OR a clear follow-up question to gather more details.
- It must not hallucinate any car data not provided in the context.
- It must be polite and relevant.
- It must not include profanity or off-topic information.

Given response: <LLM_OUTPUT>

If it meets all criteria, respond with "PASS".
If not, respond with "FAIL: <short reason>".
"""
response_schema_output = {
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["PASS", "FAIL"]
    },
    "reason": {
      "type": "string"
    }
  },
  "required": ["status", "reason"]
}



def input_validator(query):
    generation_config = GENERATION_CONFIG[0]
    # with open(json_file_path, "r") as f:
#     response_schema = json.load(f)
    generation_config.response_schema = response_schema_input
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=[INPUT_GUARDRAIL,query],config=generation_config)
    return json.loads(response.text)


def output_validator(llm_response):
    generation_config = GENERATION_CONFIG[0]
    # with open(json_file_path, "r") as f:
#     response_schema = json.load(f)
    generation_config.response_schema = response_schema_output
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=[INPUT_GUARDRAIL, llm_response], config=generation_config)
    return json.loads(response.text)


def format_car_options(results):
    car_data = []
    for doc, meta in results:
        car_data.append(f"{meta['title']} {meta['year']} {meta['brand']} {meta['model']} - {meta['comndition']}, {meta['price']}, {meta['description']}")
    return "\n".join(car_data)


def generate_response(user_query):
    # Step 1: Retrieve car metadata
    search_results = search_cars(user_query, top_k=5)
    context_text = format_car_options(search_results)
    final_prompt = f"""
{SYSTEM_PROMPT}

User Query:
{user_query}

Matching Car Options:
{context_text}

Respond with a recommendation or follow-up questions.
"""

    # Step 3: Generate answer
    
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=final_prompt)
    return response.text


if __name__ == "__main__":
    history=""
    while True:
        query = input("\n🚗 User:")
        history+=f"\nUser : {query}\n"
        if query.lower() in ["exit", "quit"]:
            break
        input_validator_response=input_validator(history)
        if input_validator_response["status"]=="VALID":
            reply = generate_response(history)
        else:
            reply = "⚠ Please ask a question related to car buying (e.g., price, brand,  or body type)."
            print("\n🤖 Gemini Assistant:\n", reply)
            history += f"\n🤖 Gemini Assistant:\n {reply}"
            continue
                
        output_validator_response = output_validator(reply)
        if output_validator_response["status"]=="FAIL":
            reply = "⚠ Sorry, I couldn't generate a reliable answer. Please try again or rephrase your question."
        history+=f"\nGemini Assistant:\n {reply}"
        print("\n🤖 Gemini Assistant:\n", reply)
