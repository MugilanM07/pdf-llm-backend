import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.pdf_db
collection = db.documents

async def save_document(doc):
    await collection.insert_one(doc)

async def get_document(doc_id):
    return await collection.find_one({"doc_id": doc_id})

async def list_documents(page: int, limit: int):
    skip = (page - 1) * limit
    cursor = collection.find().skip(skip).limit(limit)
    return [doc async for doc in cursor]