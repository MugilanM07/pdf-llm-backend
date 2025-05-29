import os
import pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    api_key=os.getenv("GEMINI_API_KEY")
)

openai_key = os.getenv("OPENAI_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
index_name = os.getenv("PINECONE_INDEX_NAME")


embedding = OpenAIEmbeddings(openai_api_key=openai_key,model = "text-embedding-ada-002")

def insert_documents(docs):
    PineconeVectorStore.from_documents(docs, 
                                 embedding, 
                                 index_name=index_name,
                                 namespace="test")

def run_rag_query(query: str):
    vectorstore = PineconeVectorStore.from_existing_index(
                          index_name=index_name,
                          embedding=embedding,
                          pool_threads=40,
                          namespace="test",
                      )
    filter = None
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",
                        search_kwargs={
                            "score_threshold": 0.875,
                            "filter": filter,
                        })
    qa = RetrievalQA.from_chain_type(
      llm=llm, 
      chain_type="stuff",
      retriever=retriever, 
      return_source_documents=True)
    return qa(query)
