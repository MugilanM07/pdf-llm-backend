# 📄 PDF LLM Backend

A FastAPI-based backend to upload PDFs, extract their content, generate LLM summaries, and answer questions using Gemini (Google Generative AI). Built for asynchronous scalability with MongoDB.

---

## 🚀 Features

- ✅ Upload and extract text from PDFs
- ✅ Store documents and metadata in MongoDB
- ✅ Generate 2-sentence summaries using Gemini (via LangChain)
- ✅ Ask contextual questions about documents
- ✅ Pagination support for document listing
- ✅ Docker-ready for easy deployment

---

## 🛠️ Tech Stack

- **FastAPI** (Backend API)
- **MongoDB** with **Motor** (Async DB)
- **Gemini via LangChain** (LLM integration)
- **PyPDF2** (PDF text extraction)
- **Docker** (Containerization)

---

## 📦 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/pdf-llm-backend.git
cd pdf-llm-backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add `.env` file

Create a `.env` file in the root:

```env
MONGO_URI=mongodb://localhost:27017
GEMINI_API_KEY=your_google_gemini_api_key
```

> 🔑 You can get a free Gemini API key from: https://makersuite.google.com/app

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

API will run at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📡 API Endpoints

### 📤 Upload PDF

```
POST /upload
```

**Form-data:** `file=@/path/to/file.pdf`
Returns: `doc_id`

---

### 📄 Get Document by ID

```
GET /documents/{doc_id}
```

---

### 📃 List Documents (with pagination)

```
GET /documents?page=1&limit=10
```

---

### 🧠 Summarize Document

```
POST /summarize/{doc_id}
```

---

### ❓ Ask a Question (RAG-style)

```
POST /query/{doc_id}/{question}
```

---

## 🐳 Docker Setup (Optional)

```bash
docker build -t pdf-llm-backend .
docker run -p 8000:8000 --env-file .env pdf-llm-backend
```

---

## ✅ Assumptions

- PDFs are simple text-based files (no OCR required)
- Using Gemini's `gemini-pro` model via LangChain
- Default pagination is `page=1&limit=10`

---


## 🧪 Testing

- Run `curl` or Postman tests
- Include at least 5 test cases covering:
  - PDF upload
  - Invalid file
  - Summarization
  - Question answering
  - Pagination behavior
