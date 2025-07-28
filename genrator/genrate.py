from flask_migrate import history
from retriver.embedings import search_cars  
from google import genai

client = genai.Client(api_key="AIzaSyC6_BxvOzwB24K2tj7c70CHr220kpnswjY")
SYSTEM_PROMPT = """
You're a helpful car-buying assistant. Based on the user's query and the car options below,
recommend 1–2 suitable vehicles. If the query is vague, ask helpful clarifying questions
like: preferred brand, condition (new/used), price range, year, or body style.
"""


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
    response = response = client.models.generate_content(
    model="gemini-2.5-flash",contents=final_prompt)
    return response.text


if __name__ == "__main__":
    history=""
    while True:
        query = input("\n🚗 Ask your car buying question: ")
        history+=f"\nUser : {query}\n"
        if query.lower() in ["exit", "quit"]:
            break
        print(history)
        reply = generate_response(history)
        print("\n🤖 Gemini Assistant:\n", reply)
        history+=f"\n🤖 Gemini Assistant:\n {reply}"
