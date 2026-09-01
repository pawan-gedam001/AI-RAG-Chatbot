from flask import Flask, render_template, request, jsonify
import os

from rag.pdf_loader import load_pdf
from rag.chunking import split_text
from rag.embedding import create_embeddings
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_chunks
from rag.gemini import ask_gemini

app = Flask(__name__)
# Global variables
vector_db = None
chunks = None

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -------------------- Home Page --------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------- Chat Route --------------------
@app.route("/chat", methods=["POST"])
def chat():

    global vector_db
    global chunks

    # Check if PDF has been uploaded
    if vector_db is None or chunks is None:
        return jsonify({
            "answer": "Please upload a PDF first."
        })

    data = request.get_json()
    question = data["question"]

    # Retrieve relevant chunks
    results = retrieve_chunks(
        vector_db,
        chunks,
        question
    )

    # Combine retrieved chunks
    context = "\n\n".join(results)

    # Ask Gemini
    answer = ask_gemini(
        context,
        question
    )

    return jsonify({
        "answer": answer
    })


# -------------------- Upload PDF --------------------
@app.route("/upload", methods=["POST"])
def upload_pdf():
    
    global vector_db
    global chunks
    # Check PDF
    if "pdf" not in request.files:
        return jsonify({
            "message": "No PDF uploaded"
        }), 400

    pdf = request.files["pdf"]

    if pdf.filename == "":
        return jsonify({
            "message": "Please select a PDF"
        }), 400

    # Save PDF
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        pdf.filename
    )

    pdf.save(file_path)

    # Read PDF
    pdf_text = load_pdf(file_path)

    if pdf_text is None:
        return jsonify({
            "message": "Invalid or corrupted PDF"
        }), 400

    # Print PDF Text
    print("\n========== PDF TEXT ==========\n")
    print(pdf_text)

    # Split into chunks
    chunks = split_text(pdf_text)

    # Create embeddings
    embeddings = create_embeddings(chunks)

    # Create FAISS Vector Store
    vector_db = create_vector_store(
        chunks,
        embeddings
    )

    print("\n===== VECTOR DATABASE =====")
    print("Total vectors stored:", vector_db.ntotal)

    # ---------------- Retrieval Test ----------------

    question = "Who created Python?"

    results = retrieve_chunks(
        vector_db,
        chunks,
        question
    )

    print("\n===== RETRIEVED CHUNKS =====\n")

    for i, chunk in enumerate(results):
        print(f"Result {i+1}")
        print(chunk)
        print("-" * 60)

    # -----------------------------------------------

    print("\n===== EMBEDDINGS =====")
    print(f"Number of Chunks : {len(chunks)}")
    print(f"Number of Embeddings : {len(embeddings)}")
    print(f"Embedding Dimension : {len(embeddings[0])}")

    print("\n========== CHUNKS ==========\n")

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}")
        print(chunk)
        print("-" * 60)

    return jsonify({
        "message": "PDF Uploaded Successfully"
    })


# -------------------- Run Flask --------------------
if __name__ == "__main__":
    app.run(debug=True)
