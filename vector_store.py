import cohere
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise EnvironmentError("COHERE_API_KEY not set in .env")

co = cohere.Client(COHERE_API_KEY)
client = chromadb.Client()

def store_chunks(chunks):
    
    try:
        client.delete_collection("contracts")
        print("Old data cleared")
    except Exception:
        pass  


    collection = client.create_collection(name="contracts")

    print("Storing embeddings...")
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embeddings = response.embeddings

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    print(f" {len(chunks)} chunks stored fresh")

def search_chunks(query, n_results=5):

    try:
        collection = client.get_collection(name="contracts")
    except Exception:
        print(" No contract loaded yet. Please run store_chunks first.")
        return []

    response = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_embedding = response.embeddings[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results["documents"][0]

if __name__ == "__main__":
    from pdf_loader import load_pdf, split_into_chunks
    text = load_pdf("sample.pdf")
    chunks = split_into_chunks(text)
    store_chunks(chunks)
    results = search_chunks("liability and payment terms")
    print("\nSearch results:")
    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(result)


