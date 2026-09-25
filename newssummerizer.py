from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser   
from langchain_groq import ChatGroq

search_tools=TavilySearchResults(max_results=5)

llm=ChatGroq(model="openai/gpt-oss-20b")

prompt=ChatPromptTemplate.from_template(
    """
you are a helpful assistant

summerize the following news into clear bullets points

{news}
  """
)

chain=prompt | llm | StrOutputParser()

news_result=search_tools.run("Latest AI news of 2026")

result=chain.invoke({"news":news_result})

print(result)

