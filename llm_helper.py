from langchain_groq import ChatGroq
from secrets_config import groq_apikey
import os
os.environ['GROQ_API_KEY'] = groq_apikey

llm = ChatGroq(
    groq_api_key = os.environ['GROQ_API_KEY'],
    model_name = 'meta-llama/llama-4-scout-17b-16e-instruct', temperature=1.0
)

if __name__ == "__main__":
    response = llm.invoke('What are the two main ingredients of a pizza?')
    print(response.content)

