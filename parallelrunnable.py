from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel,RunnableLambda

#components 
model = ChatGroq(model="openai/gpt-oss-20b")
parser = StrOutputParser()
#short prompt template
sort_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "Explain {topic} in 1-2 lines.")
    ]
)

#long prompt template
long_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "Explain {topic} in detail.")
    ]
)

#input from user


#parallel runnable
chain = RunnableParallel({ 
    "short_explanation":RunnableLambda(lambda x:x["sort_explanation"]) | sort_prompt | model | parser,
    "long_explanation":RunnableLambda(lambda x:x["long_explanation"]) | long_prompt | model | parser
}
)
result = chain.invoke({
    "sort_explanation": {"topic": "Machine Learning"},
    "long_explanation": {"topic": "Deep Learning"}
})
print(result["short_explanation"])
print(result["long_explanation"])