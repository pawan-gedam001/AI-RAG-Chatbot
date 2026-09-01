from rag.embedding import model


def retrieve_chunks(index, chunks, question, k=3):

    # Convert question into embedding
    question_embedding = model.encode([question])

    # Search in FAISS
    distances, indices = index.search(question_embedding.astype("float32"), k)

    # Get the matching chunks
    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results
