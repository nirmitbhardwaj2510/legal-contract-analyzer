import cohere
from dotenv import load_dotenv
import os
from vector_store import search_chunks

load_dotenv()
co=cohere.Client(os.getenv("COHERE_API_KEY"))
RISK_CATEGORIES=[
    "liability and damanges",
    "termination condition",
    "intellectual property ownership",
    "payment terms and penalties",
    "non compete and confindential",
    "indemnification obligations"
]
def analyze_risk(chunks_text):
    prompt=f"""you are a legal expert analyzer a contract for risk.
Analyze this contract clause and provide:
1. RISK LEVEL: HIGH,MEDIUM,LOW
2. RISK TYPE:  what kind of risk is this
3. PLAIN ENGLISH: explain in simple words what this means 
4. WARNINGS: what should the person be careful about 
contract Clause:
{chunks_text}
Respond in this exact format with each field on its own line:
RISK LEVEL: [HIGH/MEDIUM/LOW]

RISK TYPE: [type]

PLAIN ENGLISH: [explanation]

WARNING: [warning]"""
    response=co.chat(
        message=prompt,
        model="command-r-plus-08-2024"
    )
    return response.text
def analyze_contract(pdf_path):
    from pdf_loader import load_pdf,split_into_chunks
    print("contract analyzer ")
    print("="*50)
    text=load_pdf(pdf_path)
    chunks=split_into_chunks(text)
    from vector_store import store_chunks
    store_chunks(chunks)
    all_risks=[]
    for category in RISK_CATEGORIES:
        relevant_chunks=search_chunks(category,n_results=2)
        combined_text="\n".join(relevant_chunks)
        print(f"analyzing:{category.upper()}")
        risk_analysis=analyze_risk(combined_text)
        all_risks.append({
            "category":category,
            "analysis":risk_analysis,
            "chunks":relevant_chunks
        })
        print(risk_analysis)
        print("-"*40)
    return all_risks
if __name__ == "__main__":
    results=analyze_contract("sample.pdf")
    print("\n analysis complete")