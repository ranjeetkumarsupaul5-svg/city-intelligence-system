from dotenv import load_dotenv

load_dotenv()

import os
import requests

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print


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

    print("DEBUG:", data)

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
# Tools
# =========================

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

llm_with_tool = llm.bind_tools(
    [get_weather, get_news]
)


# =========================
# Agent Loop
# =========================

message = []

print("City Intelligence System")
print("Type exit to quit")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    message.append(
        HumanMessage(content=user_input)
    )

    while True:

        result = llm_with_tool.invoke(message)

        message.append(result)

        # If tool is required
        if result.tool_calls:

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                # Human in the loop
                confirm = input(
                    f"Agent wants to call {tool_name}. Approve (yes/no): "
                )

                if confirm.lower() == "no":
                    print("Tool call denied.")
                    break

                # Tool execute
                tool_result = tools[tool_name].invoke(
                    tool_call["args"]
                )

                message.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call["id"]
                    )
                )

            else:
                continue

            break

        else:
            print(result.content)
            break

### `.env`

# ```env
# OPENWEATHER_API_KEY=your_openweather_api_key
# TAVILY_API_KEY=your_tavily_api_key
# GROQ_API_KEY=your_groq_api_key
# ```

# ### Flow

# ```text
#                     USER
#                       |
#                       v
#               "Give me update
#                 about Bhopal"
#                       |
#                       v
#                    LLM
#                       |
#              +--------+--------+
#              |                 |
#              v                 v
#        get_weather          get_news
#              |                 |
#              v                 v
#        OpenWeather           Tavily
#              |                 |
#              v                 v
#        Weather Data         News Data
#              |                 |
#              +--------+--------+
#                       |
#                       v
#                  ToolMessage
#                       |
#                       v
#                     LLM
#                       |
#                       v
#               Final Response
#                       |
#                       v
#                     USER
# ```

# **Working flow:** User query → LLM decides tool → Human approval → Tool executes → result goes back to LLM → LLM gives final answer.
