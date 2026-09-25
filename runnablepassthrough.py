from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel,RunnableLambda,RunnablePassthrough, chain

model = ChatGroq(model="openai/gpt-oss-20b")
parser = StrOutputParser()

code_prompt = ChatPromptTemplate.from_messages([ 
    ( "system", "You are a code generation assistant." ),
    ( "human",  "{topic}" )
])   
explain_prompt = ChatPromptTemplate.from_messages([ 
    ( "system", "You are a helpful assistant that explains code in simple terms." ),
    ( "human", "Explain the following code snippet in simple terms: {code_snippet}" )
])   

#runnablethrough
seq1 = code_prompt | model |parser
seq2 = RunnableParallel({
    "code_generation":RunnablePassthrough() | code_prompt | model |parser,
    "explanation":explain_prompt | model | parser
})

chain = seq1 | seq2

result = chain.invoke({"topic": "Write a python code to calculate palindrome number"})

print(result["code_generation"])
print(result["explanation"])

