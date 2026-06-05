import cohere
import chromadb
from dotenv import load_dotenv
import os
load_dotenv()
COHERE_API_KEY=os.getenv("COHERE_API_KEY")
co=cohere.Client(COHERE_API_KEY)
client=chromadb.Client()
collection=client.get_or_create_collection(name="contracts")
def store_chunks(chunks):
    print("storage of embeddings...")
    response=co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embeddings=response.embeddings
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunks_{i}"for i in range(len(chunks))]
    )
    print(f"total{len(chunks)}chunks stored")
def search_chunks(query,n_results=5):
    response=co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_embeddings=response.embeddings[0]
    results=collection.query(
        query_embeddings=[query_embeddings],
        n_results=n_results
    )
    return results["documents"][0]
if __name__ == "__main__":
    from pdf_loader import load_pdf,split_into_chunks
    text=load_pdf("sample.pdf")
    chunks=split_into_chunks(text)
    store_chunks(chunks)
    results=search_chunks("liability and payment terms")
    print("\n search results:")
    for i,result in enumerate(results):
        print(f"\n---result{i+1}---")
        print(result)


