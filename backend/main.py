import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.createAgents import agent


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://city-intelligence-system-1.onrender.com"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "City Intelligence Backend is running"
    }


def _extract_weather(messages):
    """Extract structured weather info if get_weather tool was executed."""
    for msg in messages:
        if getattr(msg, "name", None) == "get_weather":
            content = str(getattr(msg, "content", ""))

            m = re.search(
                r"Weather in (.*?):\s*(.*?),\s*([+-]?\d+(?:\.\d+)?)\s*°?C",
                content,
                re.IGNORECASE
            )

            if m:
                return {
                    "city": m.group(1).strip(),
                    "condition": m.group(2).strip(),
                    "temperature": m.group(3).strip()
                }

    return None


@app.post("/chat")
def chat(user_input: str):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    response_text = result["messages"][-1].content

    weather_data = _extract_weather(
        result.get("messages", [])
    )

    response_payload = {
        "response": response_text
    }

    if weather_data:
        response_payload["weather"] = weather_data

    return response_payload