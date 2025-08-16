import streamlit as st
import requests
import json
from datetime import datetime

# Configure FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/chatresponse"

def get_chat_response(prompt):
    """Send prompt to FastAPI backend and return response"""
    try:
        response = requests.post(
            FASTAPI_URL,
            json={"prompt": prompt},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid response from server"}

# Streamlit UI setup
st.set_page_config(page_title="AI Chat", layout="wide")
st.title("AI Chat Interface")

# Initialize chat history with timestamp
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(message["timestamp"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history with timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)
    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            api_response = get_chat_response(prompt)
            
            if "error" in api_response:
                st.error(api_response["error"])
            else:
                ai_response = api_response.get("response", "No response received")
                response_timestamp = datetime.now().strftime("%H:%M:%S")
                
                st.markdown(ai_response)
                st.caption(response_timestamp)
                
                # Add AI response to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": response_timestamp
                })

# Add a clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()