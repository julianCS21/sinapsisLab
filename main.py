import os
from typing import List

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.tools import  tool


import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.tools import tool
from langchain.vectorstores.pinecone import Pinecone
from load_documents import load_documents

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENVIRONMENT'))

embeddings = OpenAIEmbeddings()
texts = load_documents()

data = Pinecone.from_texts(texts=texts, embedding=embeddings, index_name="vectordb")


@tool("documents",return_direct=True)
def documents(career : str) -> str:
    """
    Answer a query from ECI careers
    :param name:
    :return:
    """
    docsearch = Pinecone.from_existing_index("vectordb", embeddings)
    docs = docsearch.similarity_search(career)
    return docs.pop().page_content
    



@tool("SayHello",return_direct=True)
def say_hello(name : str) -> str:
    """
    Answer when someone say hello
    :param name:
    :return:
    """
    return "Hello " + name + " My name is Sainapsis"


def main():
    llm = ChatOpenAI(temperature=0)
    tools = [
        say_hello,
        documents

    ]
    agent = initialize_agent(
        tools = tools,
        llm = llm,
        agent = AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    print(agent.run("Hello!, My Name Is Julian"))
    print(agent.run("ingeniería  industrial"))






if __name__ == '__main__':
    main()

