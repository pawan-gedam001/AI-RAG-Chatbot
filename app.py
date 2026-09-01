from flask import Flask, render_template, request, jsonify
import os

from langchain import embeddings

from rag.pdf_loader import load_pdf
from rag.chunking import split_text
from rag.embedding import create_embeddings
from rag.vector_store import create_vector_store

app = Flask(__name__)

# Upload folder configuration
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

    data = request.get_json()

    question = data["question"]

    answer = f"You asked: {question}"

    return jsonify({
        "answer": answer
    })


# -------------------- Upload PDF --------------------
@app.route("/upload", methods=["POST"])
def upload_pdf():

    # Check whether PDF is uploaded
    if "pdf" not in request.files:
        return jsonify({
            "message": "No PDF uploaded"
        }), 400

    pdf = request.files["pdf"]

    # Check whether filename is empty
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

    # Check if PDF could be read
    if pdf_text is None:
        return jsonify({
            "message": "Invalid or corrupted PDF"
        }), 400

    # Print extracted text
    print("\n========== PDF TEXT ==========\n")
    print(pdf_text)

    # Split into chunks
    chunks = split_text(pdf_text)
    
    embeddings = create_embeddings(chunks)
    
    vector_db = create_vector_store(
        chunks,
        embeddings
    )

    print("\n===== VECTOR DATABASE =====\n")

    print("Total vectors stored:", vector_db.ntotal)
    
    print("\n===== EMBEDDINGS =====\n")

    print(f"Number of Chunks : {len(chunks)}")

    print(f"Number of Embeddings : {len(embeddings)}")

    print(f"Embedding Dimension : {len(embeddings[0])}")

    print("\n========== CHUNKS ==========\n")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}\n")
        print(chunk)
        print("-" * 60)

    print("\n=============================\n")

    return jsonify({
        "message": "PDF Uploaded Successfully"
    })


# -------------------- Run Flask --------------------
if __name__ == "__main__":
    app.run(debug=True)
