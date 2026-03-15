import os
from endee import Endee, Precision
from sentence_transformers import SentenceTransformer

# Initialize Endee Client
# Defaults to localhost:8080 or as provided by environment
client = Endee()
if "ENDEE_URL" in os.environ:
    client.set_base_url(os.environ["ENDEE_URL"])
index_name = "hr_index"

# Load Embedding Model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_index():
    return client.get_index(index_name)

def search_employees(query: str, top_k: int = 5, **kwargs):
    """
    Semantically search employee records for any natural language query.
    """
    try:
        index = get_index()
        query_vector = model.encode(query).tolist()
        results = index.query(vector=query_vector, top_k=top_k)
        
        # Format results for the LLM - return the raw text metadata
        return [res["meta"].get("text", "No details available") for res in results]
    except Exception as e:
        return [f"Error during search: {str(e)}"]

def flag_attrition_risk(department: str | None = None, **kwargs):
    """
    Search for employees with Attrition: Yes.
    """
    query = "Employees with Attrition: Yes"
    if department:
        query += f" in {department} department"
    return search_employees(query, top_k=10)

def summarize_department(department: str, **kwargs):
    """
    Get all employees in a department or 'all'.
    """
    if str(department).lower() in ["all", "any", "everyone"]:
        query = "list of all employees in the company"
    else:
        query = f"all employees in {department} department"
    return search_employees(query, top_k=20)

def find_low_satisfaction(top_k: int = 10, department: str | None = None, **kwargs):
    """
    Search for employees with satisfaction scores of 1 or 2.
    """
    query = "Employees with low job satisfaction (satisfaction score 1 or 2)"
    if department:
        query += f" in the {department} department"
    return search_employees(query, top_k=top_k)

def find_high_earners(top_k: int = 10, department: str | None = None, **kwargs):
    """
    Search for highest monthly income employees.
    """
    query = "Employees with the highest monthly income / compensation"
    if department:
        query += f" in the {department} department"
    return search_employees(query, top_k=top_k)
