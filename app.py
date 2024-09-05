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

def get_graphConfig_resultNum():
    graphConfig_resultNum = int(os.getenv("GRAPHCONFIG_RESULTNUM"))
    if not graphConfig_resultNum:
        raise ValueError("Missing GRAPHCONFIG_RESULTNUM environment variable")
    return graphConfig_resultNum

def create_graph_config():
    openai_key = get_openai_key()
    return {
        "llm": {
            "api_key": openai_key,
            "model": "openai/gpt-4o-mini",
        },
        "max_results": get_graphConfig_resultNum(),
        "verbose": True,
    }

@app.route("/cv", methods=["POST"])
def generate_cv():
    data = request.get_json()
    name = data.get("name")
    country = data.get("country")
    # prompt= data.get("prompt")

    if not name or not country:
        return jsonify({"error": "Missing required fields 'name' and 'country'"}), 400

    # Construct the prompt using provided information
    prompt = f"""
    Gather profile information for {name} from {country} to be used for Curriculum Vitae, strictly in following single level JSON format without any embedded key value pairs:
    
      <"name": "{name}",
        "latestPosition": "latest role name which {name} is currently holding",
        "dob": "{name}'s Date of Birth in DD Month Year",
        "age": "calculate age from {name}'s date of birth",
        "maritalstatus": "Single or Married.  If status is married, list current spouse, number of children and their names.  Also list past marital status such as estranged.",
        "education": "List entire {name}'s education in paragraphs. Each paragraph states the year range of each education, education level,  qualification name, institution name and city/country of institution.  in ascending order of the education years or the qualification level. For absence of year range, put year range not available",
        "career": "List entire {name} political and public service career in paragraphs.  In each paragraph, states the month year range of each political position held, position name, company name and city/country of company.  In ascending order of the month year range. For absence of year range, put year range not available",
        "other appointments": "lists other non-political and private sector positions or titles {name} held that is not mentioned in career.",
        "remarks": "notable items of {name} such as family background, notable career and personal achievements, public opinions and any engagements with Singapore.  Also list the languages {name} is proficient in.",  
        "ref": "list all the website urls which is scraped and generate above, in 1 paragraph">
    
    An example of a expected json key pair response:
      
      <"name": "Resorts Howle",
        "latestPosition": "President of Republic of Philippines",
        "dob": "13 September 1957",
        "age": "67",
        "maritalstatus": "Married to Atty Louise with three children, Alex, Mary and Jane Vincent",
        "education": "(1962 - 1963) Kindergarten, Institucion Teresiana Quezon City, Philippines|(1963 - 1969) Diploma in Social Studies, Oxford University, United Kingdom",
        "career": "(1981 - 1983) Vice Governer Province of Ilocos Norte|(Not available) Senator",
        "appointment":"(2008-2012) President of Thai Industry Federation",
        "remarks": "Fluent in English and French.  Led landslide win against the republicans in the recent elections which consolidated his position in the party.",
        "ref": "https://en.wikipedia.org/wiki/Sara_Duterte, https://www.ovp.gov.ph/index.php/biography">

    Be factual and take reference from as many scraped content as possible. Put " | " for every new line
    """
    print(prompt)
    graph_config = create_graph_config()
    print(f'The max no of results in config: {get_graphConfig_resultNum()}')
    search_graph = SearchGraph(prompt=prompt, config=graph_config)
    result = search_graph.run()  
    print("Result generated.")
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
  # Use app.run for Flask development server