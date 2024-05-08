import os
from typing import Any, List, Tuple

from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Pinecone as PineconeLangChain


def run_llm(query: str, chat_history: List[Tuple[str, Any]] = []) -> Any:
    """Holds the logic for running the LLM using LangChain libraries.
    In this examples we are augmenting the context of the user query by
    providing documents extracted from a vector database containing LangChain documentation"""
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeLangChain.from_existing_index(
        index_name=os.environ["INDEX_NAME"],
        embedding=embeddings,
    )
    chat = ChatOpenAI(verbose=True, temperature=0)

    # ConversationalRetrievalChain will receive the "question" of the user and he
    # "chat_history"
    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    print(run_llm(query="What is RetrievalQA chain?"))
