import getpass
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from langchain import PromptTemplate, LLMChain 
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.memory import ConversationBufferMemory

import warnings 
warnings.filterwarnings("ignore")

if "GOOGLE_API_KEY" not in os.environ: os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")
if 'SERPAPI_API_KEY' not in os.environ: os.environ["SERPAPI_API_KEY"] = getpass.getpass("Provide your SerpAPI Key")

port = 5000

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
llm = ChatGoogleGenerativeAI(model ="gemini-pro")
model = genai.GenerativeModel('gemini-pro')

memory = ConversationBufferMemory()
agent = initialize_agent(
    llm = llm,
    tools = load_tools(["serpapi", "llm-math"], llm = llm),
    agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose = True,
    handle_parsing_errors=True, 
    memory = memory
)


def chat_with_ai_without_langchain(prompt):
  return model.generate_content(prompt).text

def chat_with_ai_with_langchain(prompt):
  return agent.run(prompt)

app = Flask(__name__)
cors = CORS(app)

@app.route('/chat', methods = ['GET', 'POST'])
def chat():
   data = request.get_json()['message']
   print(data)
   response = {
        "message": "POST request received",
        "data": chat_with_ai_with_langchain(data)
    }
   print(response)
   return jsonify(response)

if __name__ == '__main__':
    print(f"Server Running on port {port}")
    app.run(debug=True, port = port)

# prompt_1 = PromptTemplate(
#     input_variables=["location_description"],
#     template=" Suggest one to visit which satisfies these condiditons :{location_description} / just give me the location name",
# )
# print(chat_with_ai_with_langchain(prompt_1.format(location_description="Snowy area with nearby beach")))

# chain = LLMChain(llm = llm, prompt = prompt_1, output_key = "Location")
# chain.run("Hot and humid area with nearby forest")

# prompt_2 = PromptTemplate(
#     input_variables= ['Location'],
#     template = "Give me 5 good restaurants which is affordable in {Location} / give me only the name of the restaurant",
# )

# chain_2 = LLMChain(llm = llm, prompt = prompt_2, output_key = "Restaurants")
# chain_2.run(chain.run("Cold with moderate temperature"))

# seq_chain = SequentialChain(
#     chains = [chain, chain_2],
#     input_variables = ['location_description'],
#     output_variables = ['location_name', 'Restaurants']
# )

# print(seq_chain({'input': "Hot and humid area with nearby forest"}))