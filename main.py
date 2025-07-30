from fastapi import FastAPI
import uuid
from pydantic import BaseModel
from genrator.genrate import generate_response
from utils.guardrail import input_validator, output_validator
from db.history import get_history, save_history

app = FastAPI()


class Query(BaseModel):
    query: str
    session_id: str | None = None  # Optional session_id


@app.post("/generate/{user_id}")
def get_car_recommendation(user_id: str, request: Query):
    session_id = request.session_id or str(uuid.uuid4())
    history = get_history(session_id)
    
    history += f"\nUser: {request.query}\n"

    # Step 1: Validate input
    input_valid = input_validator(history)
    if input_valid["status"] != "VALID":
        response= "⚠ Please ask a question related to car buying (e.g., price, brand, or body type)."
        history += f"\nGemini Assistant: {response}\n"
        return {
        "response": response,
        "session_id": session_id,
        "history": history
    }

    # Step 2: Generate using Gemini
    response = generate_response(history)

    # Step 3: Output validation
    print("AI Response: ", response)
    output_valid = output_validator(response)
    if output_valid["status"] == "FAIL":
        response="⚠ Sorry, I couldn't generate a reliable answer. Please try again or rephrase your question."

    # Step 4: Update session history
    history += f"\nGemini Assistant: {response}\n"
    save_history(session_id, history)

    return {
        "response": response,
        "session_id": session_id,
        "history": history
    }
