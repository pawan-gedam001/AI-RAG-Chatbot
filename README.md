# AI RAG Chatbot with Flask + FAISS + Gemini

## Project Overview

This project is an AI chatbot that can answer questions from an uploaded PDF using **Retrieval-Augmented Generation (RAG)**.

Instead of answering from general knowledge, the chatbot first searches the uploaded PDF for relevant information and then uses **Google Gemini** to generate an answer based only on that information.

---

# Technologies Used

* Python
* Flask
* HTML
* CSS
* JavaScript
* PyPDF
* LangChain
* Sentence Transformers
* FAISS
* Google Gemini API
* Python Dotenv

---

# Project Structure

```text
AI-RAG-Chatbot/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── uploads/
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── rag/
    ├── pdf_loader.py
    ├── chunking.py
    ├── embedding.py
    ├── vector_store.py
    ├── retriever.py
    └── gemini.py
```

---

# RAG Workflow

```text
User Uploads PDF
        │
        ▼
Read PDF
        │
        ▼
Extract Text
        │
        ▼
Split into Chunks
        │
        ▼
Create Embeddings
        │
        ▼
Store in FAISS Vector Database
        │
        ▼
User Asks Question
        │
        ▼
Convert Question into Embedding
        │
        ▼
Search Similar Chunks in FAISS
        │
        ▼
Retrieve Relevant Context
        │
        ▼
Send Context + Question to Gemini
        │
        ▼
Gemini Generates Answer
        │
        ▼
Answer Displayed on Website
```

---

# How the Project Works

## Step 1 - Upload PDF

The user selects a PDF and clicks **Upload**.

The PDF is saved in the `uploads/` folder.

---

## Step 2 - Read PDF

`pdf_loader.py`

Uses:

```python
PdfReader()
```

to extract all text from the uploaded PDF.

Example:

```text
Python was created by Guido van Rossum.

Python supports OOP.

Python is used for AI.
```

---

## Step 3 - Chunking

Large documents cannot be sent directly to the LLM.

The extracted text is divided into smaller pieces called **chunks**.

Example:

```text
Chunk 1

Python was created by Guido van Rossum.

Python supports OOP.
```

---

## Step 4 - Create Embeddings

Each chunk is converted into numbers (vectors).

Example:

```text
Chunk

↓

[0.24, -0.91, 0.53, ...]
```

Model used:

```
sentence-transformers/all-MiniLM-L6-v2
```

Embedding size:

```
384
```

---

## Step 5 - Create FAISS Vector Database

The embeddings are stored inside FAISS.

FAISS performs similarity search.

Example:

```text
Question

↓

Embedding

↓

FAISS

↓

Most Similar Chunk
```

---

## Step 6 - Ask Question

User types:

```text
Who created Python?
```

---

## Step 7 - Retrieve Relevant Chunks

FAISS searches the stored vectors.

Example:

```text
Result

Python was created by Guido van Rossum.
```

---

## Step 8 - Gemini

Prompt format:

```text
Context:

Python was created by Guido van Rossum.

Question:

Who created Python?

Answer:
```

Gemini answers only from the provided context.

---

## Step 9 - Display Answer

JavaScript receives the answer and displays it on the webpage.

Example:

```text
Python was created by Guido van Rossum.
```

---

# Files Explanation

## app.py

Main Flask application.

Responsibilities:

* Home page
* Upload PDF
* Read PDF
* Chunk text
* Create embeddings
* Create FAISS database
* Retrieve chunks
* Ask Gemini
* Return answer

---

## pdf_loader.py

Reads PDF using PyPDF.

Input:

```
PDF
```

Output:

```
Extracted Text
```

---

## chunking.py

Splits long text into smaller chunks.

Input:

```
Text
```

Output:

```
Chunks
```

---

## embedding.py

Creates embeddings using Sentence Transformers.

Input:

```
Chunks
```

Output:

```
Vectors
```

---

## vector_store.py

Stores vectors inside FAISS.

Input:

```
Embeddings
```

Output:

```
FAISS Index
```

---

## retriever.py

Searches the FAISS index.

Input:

```
Question
```

Output:

```
Relevant Chunks
```

---

## gemini.py

Loads:

* API Key
* Gemini Model

Receives:

* Context
* Question

Returns:

* AI Answer

---

## index.html

Frontend.

Contains:

* Upload button
* Question input
* Send button
* Answer section

---

## script.js

Handles:

* Upload PDF
* Send Question
* Display Answer

---

# Installation

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# Environment Variables

Create `.env`

```text
GOOGLE_API_KEY=YOUR_API_KEY
```

---

# .gitignore

```text
venv/
__pycache__/
.env
uploads/
```

---

# Current Features

* Upload PDF
* Extract PDF text
* Chunk text
* Generate embeddings
* Store vectors in FAISS
* Semantic search
* Gemini integration
* Answer questions from uploaded PDF

---

# Current Limitations

* Only one PDF at a time.
* FAISS database exists only while the app is running.
* Upload again after restarting.
* No chat history.
* No multiple-document support.

---

# Future Improvements

* Save FAISS index to disk.
* Load vector database automatically.
* Multiple PDF support.
* Chat history.
* Streaming responses.
* Better UI.
* Source citations.
* Docker support.
* Deploy on Render or Railway.
* User authentication.
* Admin dashboard.

---

# Example

PDF contains:

```text
Python was created by Guido van Rossum.

Python supports OOP.

Python is used for AI.
```

Question:

```text
Who created Python?
```

Retrieved Context:

```text
Python was created by Guido van Rossum.
```

Gemini Answer:

```text
Python was created by Guido van Rossum.
```

---

# Learning Outcome

This project demonstrates:

* Flask backend development
* Frontend integration
* PDF processing
* Text chunking
* Embeddings
* Vector databases (FAISS)
* Semantic search
* Retrieval-Augmented Generation (RAG)
* Google Gemini API integration
* End-to-end AI application development
