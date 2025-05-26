import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_summary(text: str):
    prompt = f"Summarize this in 2 sentences:\n{text}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

def ask_question(text: str, question: str):
    prompt = f"""
        You are a helpful AI assistant with access to the following document content. Use it strictly to answer the user’s question.

        --- Document Context ---
        {text}
        ------------------------

        Instructions:
        - Answer only based on the content provided above.
        - If the answer is not found in the context, respond with: "The answer is not available in the document."
        - Be concise, clear, and factual.

        Question: {question}
        """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
