from endee import Endee, Precision
from sentence_transformers import SentenceTransformer
import pandas as pd

EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 outputs 384-dim vectors
INDEX_NAME = "hr_index"

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_client():
    return Endee()  # connects to http://localhost:8080 by default

def ingest_csv(filepath: str) -> int:
    df = pd.read_csv(filepath).fillna("N/A")

    # Build text profiles per employee
    if "JobRole" in df.columns and "Department" in df.columns:
        def smart_text(r):
            base = f"{r.get('JobRole','Employee')} in {r.get('Department','Unknown')} department."
            if "Attrition" in r:       base += f" Attrition: {r['Attrition']}."
            if "MonthlyIncome" in r:   base += f" Income: ${r['MonthlyIncome']}."
            if "JobSatisfaction" in r: base += f" Satisfaction: {r['JobSatisfaction']}/4."
            if "YearsAtCompany" in r:  base += f" Years at company: {r['YearsAtCompany']}."
            if "Age" in r:             base += f" Age: {r['Age']}."
            if "EmployeeNumber" in r:  base += f" ID: {r['EmployeeNumber']}."
            return base
        df["_text"] = df.apply(smart_text, axis=1)
    else:
        df["_text"] = df.apply(
            lambda r: " | ".join([f"{col}: {val}" for col, val in r.items()]), axis=1
        )

    client = get_client()

    # Create index (delete old one if exists)
    try:
        client.delete_index(INDEX_NAME)
    except:
        pass

    client.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIM,
        space_type="cosine",
        precision=Precision.INT8
    )

    index = client.get_index(INDEX_NAME)

    texts = df["_text"].tolist()
    print("🔄 Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    # Upsert in batches of 100
    batch = []
    for i, (text, vector) in enumerate(zip(texts, embeddings)):
        batch.append({
            "id": str(i),
            "vector": vector,
            "meta": {"text": text}
        })
        if len(batch) == 100:
            index.upsert(batch)
            batch = []
    if batch:
        index.upsert(batch)

    print(f"✅ Ingested {len(texts)} records into Endee!")
    return len(texts)