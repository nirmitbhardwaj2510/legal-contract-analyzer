import fitz
# import path
from langchain_text_splitters import RecursiveCharacterTextSplitter
def load_pdf(file_path):
    doc=fitz.open(file_path)
    full_text=""
    for page in doc:
        full_text += page.get_text()
    return full_text
def split_into_chunks(text):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks=splitter.split_text(text)
    return chunks
if __name__ == "__main__":
    text=load_pdf("sample.pdf")
    chunks=split_into_chunks(text)
    print(f"Total chunks:{len(chunks)}")
    print(f"first chunk:\n{chunks[0]}")
