import streamlit as st
import time
import os
import requests
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
# from langchain.agents import create_tool_calling_agent, AgentExecutor
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from helper import get_weather, generate_image

if os.path.exists(".env"):
    load_dotenv(find_dotenv())

LANGCHAIN_API_KEY = st.secrets.get("LANGCHAIN_API_KEY",os.getenv('LANGCHAIN_API_KEY'))
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
if LANGCHAIN_API_KEY:
    os.environ['LANGCHAIN_API_KEY'] = LANGCHAIN_API_KEY
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
groq_api_key = GROQ_API_KEY

@tool
def function_call(city:str) -> str:
    """
    calls a function in helper module with
    ability to call a weather update using an API
    """
    if city:
        return get_weather(city)
    return

@tool
def image_creation_tool(prompt:str):
    """
    It calls a generate_image function from helper module
    """
    if prompt:
        return generate_image(prompt)
    return 


prompt = ChatPromptTemplate(
    messages = [
        ('system', "you're a helpful Assistant, please give a detailed response to the user"),
        ('user', "Question:{question}"),
        ('placeholder', "{agent_scratchpad}")
    ]
)

def generate_response(question, api_key, llm, temperature, max_tokens):
    model = ChatGroq(
        model=llm, 
        groq_api_key=api_key, 
        temperature=temperature, 
        # max_tokens=max_tokens
    )
    
    tools = [function_call, image_creation_tool]

    model_with_tools = model.bind_tools(tools)
    messages = [
        ('system', "You're a helpful Assistant, please give a detailed response to the user."),
        ('user', f"Question: {question}")
    ]
    first_response = model_with_tools.invoke(messages)

    if first_response.tool_calls:
        for tool_call in first_response.tool_calls:
            if tool_call['name'] == 'function_call':
                tool_output = function_call.invoke(tool_call['args'])

            elif tool_call['name'] == 'image_creation_tool':
                tool_output = function_call.invoke(tool_call["args"])
            else:
                continue

            messages.append(first_response)
            messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))

            for chunk in model_with_tools.stream(messages):
                if chunk.content:
                    yield chunk.content
                    time.sleep(0.04)
    else:
        # If no tool call is requested, simply stream the initial LLM output smoothly
        for chunk in model_with_tools.stream(messages):
            if chunk.content:
                yield chunk.content
    

# Title  of the app
st.sidebar.title('Settings')
try:
    api_key = st.sidebar.text_input('Enter your groq api key here:', type='password')
    llm = st.sidebar.selectbox('Select an LLM model', ['openai/gpt-oss-20b', 'openai/gpt-oss-120b', 'qwen/qwen3.8-27b'])
    if not api_key:
        st.sidebar.write('API Key cannot be empty, using the developer key')
        api_key = groq_api_key

    temperature = st.sidebar.slider('Temperature (0.0 -> 1.0)', min_value=0.0, max_value=1.0, value=0.4)
    max_tokens = st.sidebar.slider('Max Tokens', min_value=50, max_value=300, value=150)

    st.write('Hey, Welcome!!!')
    user_input = st.text_input('How can I help you today?: ')
    if user_input:
        if st.button('Go >>>'):
            response = generate_response(
                question=user_input, api_key=api_key, llm=llm,
                temperature=temperature, max_tokens=max_tokens
                )
            print(response)
            st.write_stream(response)
        
    else:
        st.write('Please, provide something to talk about')
    
except Exception as E:
    st.sidebar.write(str(E))