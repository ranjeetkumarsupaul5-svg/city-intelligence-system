from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# 1. Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "Explain {topic} in simple terms.")
    ]
)

# 2. Model initialization
model = ChatGroq(
    model="openai/gpt-oss-20b"
)

# 3. Output parser
parser = StrOutputParser()
#runnable
chain = prompt | model | parser #promt ka output ko model me bhejega aur model ka output parser me bhejega aur parser ka output ko chain me save ho jayega

result = chain.invoke("Machine Learning")
print(result)