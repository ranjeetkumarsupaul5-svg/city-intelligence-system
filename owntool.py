from langchain.tools import tool

@tool
def get_greeting(name :str)->str:
    """Generate a greeting message for a user  """

    return f"hello {name} , Welcome to the AI world"

result=get_greeting.invoke({"name":"Ranjeet"})

print(result)

print(get_greeting.name)
print(get_greeting.description)
print(get_greeting.args)


