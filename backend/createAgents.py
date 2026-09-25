from dotenv import load_dotenv

load_dotenv()

import os
import requests

from langchain_groq import ChatGroq
from langchain.tools import tool
from tavily import TavilyClient
from rich import print
from langchain.agents import create_agent


# =========================
# Weather Tool
# =========================

@tool
def get_weather(city: str) -> str:
    """Get current weather of the city"""

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": f"{city},IN",
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # print("DEBUG:", data)

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# =========================
# Tavily News Tool
# =========================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get latest news about the city"""

    response = tavily_client.search(
        query=f"latest news about {city}",
        search_depth="basic",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return f"No latest news found for {city}."

    news = []

    for result in results:

        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")

        news.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"URL: {url}"
        )

    return "\n\n".join(news)


# =========================
# LLM
# =========================

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


# =========================
# Agent
# =========================

agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="""
You are a helpful City Intelligence assistant.

For current weather, temperature, conditions, humidity,
wind, or forecast questions about a city, use the get_weather tool.

When providing weather information, format your response clearly as:
**<City> Weather**
- **Condition:** <Condition>
- **Temperature:** <Temperature> °C

For latest or current news about a city, use the get_news tool.

Do not invent current weather or latest news information.
"""
)