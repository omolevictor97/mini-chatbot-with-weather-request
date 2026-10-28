import streamlit as st
import time

st.set_page_config(page_title="WhatsApp Style Chat", layout="centered")
st.title("💬 WebChat")

# 1. Initialize session state to store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# 2. Create a scrollable container for the chat history (above the input)
# Setting a height gives it that contained chat-app feel. 
chat_container = st.container(height=500, width=800)

# 3. Render existing messages inside the chat container
with chat_container:
    for msg in st.session_state.messages:
        # st.chat_message handles the left/right chat bubble layout and avatar icons
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 4. Create the chat input box. 
# It comes built-in with a right-aligned text area and a small send icon button.
if prompt := st.chat_input("Type a message...", width=1000, accept_file=True, accept_audio=True):
    
    # Display user message instantly in the container above
    with chat_container:
        with st.chat_message("user"):
            st.write(prompt)
            
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Simulate LLM streaming response
    with chat_container:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # --- REPLACE THIS BLOCK WITH YOUR ACTUAL LLM CALL ---
            simulated_response = f"Echoing your request: '{prompt}'. This is an automated response."
            for chunk in simulated_response.split(" "):
                full_response += chunk + " "
                time.sleep(0.08)
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            # ----------------------------------------------------

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
