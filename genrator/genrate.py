from retriver.embedings import search_cars
from prompts.genrator import SYSTEM_PROMPT
from utils.guardrail import input_validator,output_validator
import config




def format_car_options(results):
    car_data = []
    for _, meta in results:
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
    
    response = config.client.models.generate_content(
    model="gemini-2.5-flash", contents=final_prompt)
    return response.text


# if __name__ == "__main__":
#     history=""
#     while True:
#         query = input("\n🚗 User:")
#         history+=f"\nUser : {query}\n"
#         if query.lower() in ["exit", "quit"]:
#             break
#         input_validator_response=input_validator(history)
#         if input_validator_response["status"]=="VALID":
#             reply = generate_response(history)
#         else:
#             reply = "⚠ Please ask a question related to car buying (e.g., price, brand,  or body type)."
#             print("\n🤖 Gemini Assistant:\n", reply)
#             history += f"\n🤖 Gemini Assistant:\n {reply}"
#             continue
                
#         output_validator_response = output_validator(reply)
#         if output_validator_response["status"]=="FAIL":
#             reply = "⚠ Sorry, I couldn't generate a reliable answer. Please try again or rephrase your question."
#         history+=f"\nGemini Assistant:\n {reply}"
#         print("\n🤖 Gemini Assistant:\n", reply)
