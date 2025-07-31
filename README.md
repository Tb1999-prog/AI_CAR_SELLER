# AI_CAR_SELLER

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Model](https://img.shields.io/badge/Model-Gemini-blueviolet)](https://deepmind.google/technologies/gemini/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-red)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Streamlit-orange)](https://streamlit.io/)

An AI-powered conversational assistant that helps users find the best car deals based on preferences like price, brand, body style, and condition. The system uses a combination of:

- Retrieval-Augmented Generation (RAG) for relevant car matching
- Google Gemini Models for Conversations about Car suggestion
- Custom tools for finance calculations and fallback handling
- Streamlit frontend and FastAPI backend with streaming

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/AI_CAR_SELLER.git
cd AI_CAR_SELLER
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Step 1: Start the Backend (FastAPI)

```bash
uvicorn main:app --reload
```

Runs at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Step 2: Launch the Frontend (Streamlit)

```bash
streamlit run app.py
```

Visit: [http://localhost:8501](http://localhost:8501)

## Sample Conversation Log

```txt
User: Hi
Assistant:
Hello there! Thanks for stopping by. I'm your AI Car-Buying Assistant, ready to help you find the perfect ride.
What can I help you with today?

User: I want sedan under 30k
Assistant:
Excellent! A sedan under $30,000 gives you a lot of fantastic options, from nearly-new models packed with tech to more luxurious trims with a few miles on them.

To help me zero in on the perfect car for you, are you leaning towards a newer model year, or are features like leather seats and premium sound systems more of a priority?

Based on what we have in stock right now, I've found a couple of great deals that fit your budget.
Here are two top contenders for you to consider:

1. 2021 Hyundai Elantra

Condition: Used

Body Style: Sedan

Price: $19,840

Details: This one's a fantastic value. It's a recent model year with a zippy turbo engine, excellent fuel economy, and all the modern tech you could want, including a navigation system and Apple CarPlay.

2. 2019 Nissan Altima

Condition: Used

Body Style: Sedan

Price: $23,227

Details: If you're looking for a touch more luxury, this one's a fantastic find. It's a one-owner vehicle in a premium trim, featuring a sunroof, leather seats, and advanced safety features like lane assist.
```

## Project Structure

```
AI CAR SELLER/
├── data/
│   ├── chat_history.db
│   ├── fais_index.index
│   ├── fais_metadata.pkl
│   └── vehicle_inventory.json
├── db/
│   └── history.py
├── generator/
│   ├── genrate.py
├── prompts/
│   ├── generator.py
│   └── guardrail.py
├── retriver/
│   └── embedings.py
├── schemas/
│   ├── input_guardrail.json
│   └── output_guardrail.json
├── utils/
│   └── guardrail.py
├── app.py
├── config.py
├── main.py
├── populate_data.py
├── README.md
└── requirments.txt
```
