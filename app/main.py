from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from app import database, utils, llm, schemas, auth
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
from app.auth import create_access_token, verify_token
from app.schemas import UserLogin
import logging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Invalid file type. Only PDF files are accepted.')

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        logger.error(f"Failed to save uploaded file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")

    try:
        text = utils.extract_text(content)
        if not text:
            raise HTTPException(status_code=400, detail='Failed to extract text from the PDF file.')
    except Exception as e:
        logger.error(f"Text extraction error: {e}")
        raise HTTPException(status_code=500, detail='Error occurred while extracting text from the PDF.')

    doc_id = str(uuid.uuid4())
    doc = {
        "_id": doc_id,
        "doc_id": doc_id,
        "filename": file.filename,
        "file_path": file_location,
        "upload_time": datetime.utcnow(),
        "text": text
    }

    try:
        await database.save_document(doc)
    except Exception as e:
        logger.error(f"Database save error: {e}")
        raise HTTPException(status_code=500, detail='Failed to save document in the database.')

    return {"doc_id": doc_id}


@app.get('/documents/{doc_id}')
async def get_document(doc_id: str):
    try:
        doc = await database.get_document(doc_id)
    except Exception as e:
        logger.error(f"Database retrieval error for doc_id {doc_id}: {e}")
        raise HTTPException(status_code=500, detail='Failed to retrieve document from the database.')

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc

@app.get("/documents")
async def list_documents(page: int = 1, limit: int = 10):
    try:
        docs = await database.list_documents(page, limit)
    except Exception as e:
        logger.error(f"Database list documents error: {e}")
        raise HTTPException(status_code=500, detail='Failed to list documents from the database.')
    return docs

@app.post("/summarize/{doc_id}")
async def summarize(doc_id: str, _: dict = Depends(verify_token)):
    try:
        doc = await database.get_document(doc_id)
    except Exception as e:
        logger.error(f"Database retrieval error for doc_id {doc_id}: {e}")
        raise HTTPException(status_code=500, detail='Failed to retrieve document from the database.')

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        summary = llm.get_summary(doc["text"])
    except Exception as e:
        logger.error(f"LLM summary error: {e}")
        raise HTTPException(status_code=500, detail='Failed to generate summary.')

    return {"summary": summary}

@app.post("/query/{doc_id}/{question}")
async def query_doc(doc_id: str, question: str):
    try:
        doc = await database.get_document(doc_id)
    except Exception as e:
        logger.error(f"Database retrieval error for doc_id {doc_id}: {e}")
        raise HTTPException(status_code=500, detail='Failed to retrieve document from the database.')

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        answer = llm.ask_question(doc["text"], question)
    except Exception as e:
        logger.error(f"LLM query error: {e}")
        raise HTTPException(status_code=500, detail='Failed to get an answer from the LLM.')

    return {"answer": answer}

@app.post("/login")
def login(user: UserLogin):
    try:
        if user.username != "admin" or user.password != "password":
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token({"sub": user.username})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during login")
    return {"access_token": access_token}
