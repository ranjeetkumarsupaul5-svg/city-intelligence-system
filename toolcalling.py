from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

from rich import print


# 1. creating a tool
@tool
def get_text_length(text: str) -> int:
    """Returns the number of character in a given text"""
    return len(text)


tools = {
    "get_text_length": get_text_length
}


llm = ChatGroq(model="openai/gpt-oss-20b")


# tool binding with llm
llm_with_tool = llm.bind_tools([get_text_length])


message = []

prompt = input("You: ")
query = HumanMessage(prompt)

message.append(query)

result = llm_with_tool.invoke(message)

message.append(result)



if result.tool_calls:
    print(result.tool_calls[0])

    tool_call = result.tool_calls[0]
    tool_name = tool_call["name"]

    tool_result = tools[tool_name].invoke(tool_call["args"])

    tool_message = ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call["id"]
    )

    message.append(tool_message)

    result = llm_with_tool.invoke(message)

    print(result.content)