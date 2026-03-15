import os
import threading
import pandas as pd
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from endee import Endee, Precision
from sentence_transformers import SentenceTransformer
from agent.agent import run_agent

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Endee Config
client = Endee()
if "ENDEE_URL" in os.environ:
    client.set_base_url(os.environ["ENDEE_URL"])
index_name = "hr_index"

# Embedding Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Ingestion state
ingestion_status = {"status": "idle", "progress": 0, "total": 0}

def create_hr_index():
    try:
        # Check if index exists
        indices = client.list_indexes()
        if not any(idx["name"] == index_name for idx in indices):
            print(f"Creating index: {index_name}")
            client.create_index(
                name=index_name,
                dimension=384,
                space_type="cosine",
                precision=Precision.INT8
            )
    except Exception as e:
        print(f"Error creating index: {e}")

def ingest_csv(file_path):
    global ingestion_status
    try:
        ingestion_status["status"] = "ingesting"
        df = pd.read_csv(file_path)
        ingestion_status["total"] = len(df)
        ingestion_status["progress"] = 0
        
        create_hr_index()
        index = client.get_index(index_name)
        
        batch_size = 50
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            upsert_data = []
            for _, row in batch.iterrows():
                # Create natural language profile
                profile_parts = []
                for col in df.columns:
                    profile_parts.append(f"{col}: {row[col]}")
                text_profile = ". ".join(profile_parts)
                
                # Embed
                vector = model.encode(text_profile).tolist()
                
                upsert_data.append({
                    "id": str(row.get('EmployeeID', row.get('ID', i + _))),
                    "vector": vector,
                    "meta": {"text": text_profile}
                })
            
            index.upsert(upsert_data)
            ingestion_status["progress"] += len(batch)
            
        ingestion_status["status"] = "completed"
    except Exception as e:
        ingestion_status["status"] = f"error: {str(e)}"
        print(f"Ingestion error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Start ingestion in background
    thread = threading.Thread(target=ingest_csv, args=(file_path,))
    thread.start()
    
    return jsonify({"message": "File uploaded and ingestion started", "filename": file.filename})

@app.route('/status')
def get_status():
    return jsonify(ingestion_status)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get("query")
    history = data.get("history", [])
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        response = run_agent(query, history)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
