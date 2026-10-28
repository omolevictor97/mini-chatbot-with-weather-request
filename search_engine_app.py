import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

import arxiv as arxiv_library

# Force the underlying client wrapper to use secure HTTPS endpoints natively
arxiv_library.Client.query_url_format = "https://export.arxiv.org/api/query?{}"


## Arxiv and wikipedia Tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

search = DuckDuckGoSearchRun(name="Search")

st.title("🔎 LangChain - Chat with search")
"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [://github.com](https://://github.com).
"""

## Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

if prompt := st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not api_key:
        st.info("Please add your Groq API key to continue.")
        st.stop()

    llm = ChatGroq(groq_api_key=api_key, model_name="openai/gpt-oss-120b", streaming=True, temperature=0.4)
    tools = [search, arxiv, wiki]

    # Define the ReAct prompt explicitly to avoid importing 'hub'
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant equipped with web search and data retrieval tools."),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        ('human', '{input}'),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ])

    # Construct the modern ReAct agent using the local template
    agent = create_tool_calling_agent(llm, tools, prompt_template)

    # Create the executor
    search_agent = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        
        # Invoke the executor cleanly with the text prompt string
        response_dict = search_agent.invoke({"input": prompt}, callbacks=[st_cb])
        response = response_dict["output"]
        
        st.session_state.messages.append({'role': 'assistant', "content": response})
        st.write(response)
