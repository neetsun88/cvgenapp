from flask import Flask, request, jsonify
from scrapegraphai.graphs import SearchGraph
from scrapegraphai.utils import convert_to_csv, convert_to_json, prettify_exec_info
import os
from dotenv import load_dotenv
import nest_asyncio 

app = Flask(__name__)
# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Load environment variables from .env file (optional)
load_dotenv()

@app.route('/')
def hello_world():
    return "Homepage for Generator"

def get_openai_key():
    openai_key = os.getenv("OPENAI_APIKEY")
    if not openai_key:
        raise ValueError("Missing OPENAI_APIKEY environment variable")
    return openai_key

def create_graph_config():
    openai_key = get_openai_key()
    return {
        "llm": {
            "api_key": openai_key,
            "model": "openai/gpt-4o-mini",
        },
        "max_results": 2,
        "verbose": True,
    }

@app.route("/cv", methods=["POST"])
def generate_cv():
    data = request.get_json()
    name = data.get("name")
    country = data.get("country")

    if not name or not country:
        return jsonify({"error": "Missing required fields 'name' and 'country'"}), 400

    # Construct the prompt using provided information
    prompt = f"""
    Generate Curriculum Vitae for {name} from {country} with following JSON fields and sequence:
    "name" : "Name in capital letters", 
    "dob": "Date of Birth in DD Month Year",
    "age": <Calculate his age this year, derive from his Date of Birth (assuming it's available)> ,
    "education": Each paragraph contains below information and sorted in descending years
    - "qualification" which indicates the qualification which {name} attained
    - "institution" which indicates the name and Country of institution that {name} graduates from
    - "yrs" which indicates the years that {name} spent in institution
    "career": Each paragraph contains below and sorted in descending years
    - "yrs" e.g. 2009-2011 of each career
    - "position" position name that {name} holds
    - "company" name of company
    - "desc" a paragraph on what {name} does in this job scope

    "ref": Array of URLs where the information is retrieved
    If no data can be found for field, return field name with value "Not found"
    """

    graph_config = create_graph_config()
    search_graph = SearchGraph(prompt=prompt, config=graph_config)
    result = search_graph.run()  # Flask doesn't require `await` for synchronous functions

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
  # Use app.run for Flask development server