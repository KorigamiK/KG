import json

import google.ai.generativelanguage as glm
import google.generativeai as genai
from google.api_core import retry
from google.generativeai import GenerationConfig
from pyvis.network import Network

from declarations import add_to_database

# from IPython.display import display
# from IPython.display import Markdown


try:
    # from google.colab import userdata
    # GOOGLE_API_KEY=userdata.get('API_KEY')
    GOOGLE_API_KEY = ""
except ImportError:
    import os

    GOOGLE_API_KEY = os.environ["API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)


# Set up the model
generation_config = GenerationConfig(
    temperature=0.9, top_p=1, top_k=1, max_output_tokens=2048, candidate_count=1
)

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

user_prompt = (
    """The architecture of a CRUD REST API with Node.js, Express, and MongoDB"""
)

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    tools=[add_to_database],
)

# model = genai.GenerativeModel(model_name='gemini-1.0-pro')

response = model.generate_content(
    f"""Please try to explain in detail everything about the following topic explaining \
      each component and how they relate to each other:
      {user_prompt}
      """,
    request_options={"retry": retry.Retry()},
)
story = response.text
print(response.candidates[0].citation_metadata)


result = model.generate_content(
    f"""
Help me understand the following by describing the entities and relationships to create a knowledge graph:

{user_prompt}
"""
)

fc = result.candidates[0].content.parts[0].function_call
print(type(fc))

"""The `glm.FunctionCall` class is based on Google Protocol Buffers, convert it to a more familiar JSON compatible object:"""
print(json.dumps(type(fc).to_dict(fc), indent=4))



net = Network(
  notebook=True,
  directed=True,
  cdn_resources='in_line',
  width='1200px',
  height='900px',
  bgcolor='beige'
)

colors = [ '#ffcdb2ff', '#ffb4a2ff', '#e5989bff', '#b5838dff', '#6d6875ff', "#006d77","#83c5be","#edf6f9","#ffddd2","#e29578" ]

def get_color():
    try:
        return colors.pop()
    except IndexError:
        return '#ffcdb2ff'

for entity in fc.args['entities']:
    net.add_node(entity['name'], label=entity['name'], title=entity['description'], color=get_color())

for relation in fc.args['relationships']:
    net.add_edge(relation['from_entity_name'], relation['to_entity_name'], label=relation['relationship'])

net.repulsion(
    node_distance=100,
    central_gravity=0.20,
    spring_length=250,
    spring_strength=0.05,
    damping=0.09,
)

net.save_graph('KnowledgeGraph.html')