from retriver.embedings import search_cars
from prompts.genrator import SYSTEM_PROMPT
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
    model="gemini-2.5-pro", contents=final_prompt)
    return response.text