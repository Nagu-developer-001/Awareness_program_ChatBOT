import streamlit as st
from openai import OpenAI

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Awareness Bot", page_icon="🧠", layout="centered")

# --- CUSTOM CSS: Fixing the "Invisible Text" & White Background ---
st.markdown("""
    <style>
    /* 1. Force the app background to a light, clean grey */
    .stApp {
        background-color: #f8f9fa !important;
    }

    /* 2. FORCE ALL TEXT TO BE DARK (Fixes the white-on-white issue) */
    h1, h2, h3, p, span, div, label {
        color: #1f2937 !important;
    }

    /* 3. Style the Title and Subheader for the Awareness Program */
    .main-title {
        color: #1e3a8a !important; /* Deep Blue */
        font-weight: 800;
        text-align: center;
    }

    /* 4. Make Chat Bubbles distinct from the background */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 15px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* 5. Style the Code block (Model name) */
    code {
        color: #d946ef !important; /* Playful Pink */
        background-color: #f1f5f9 !important;
        padding: 2px 6px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (The Awareness Center) ---
with st.sidebar:
    st.title("🤖 AI Lab @ College")
    st.info("This bot demonstrates how Large Language Models (LLMs) use probability to predict the next word.")
    
    api_key = st.text_input("Enter Groq API Key", type="password", help="Get yours at console.groq.com")
    
    model_choice = st.selectbox(
        "Select AI Brain (Model):",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0
    )

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.write("**Did you know?**")
    st.caption("AI calculates the mathematical likelihood of words based on patterns in training data.")

# --- 3. CHAT LOGIC ---
st.markdown("<h1 class='main-title'>🌟 AI Awareness Program</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Running on: <code>{model_choice}</code></p>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a friendly AI expert. Explain things using simple metaphors like 'auto-complete on steroids'."}
    ]

# Welcome Message if chat is empty
if len(st.session_state.messages) <= 1:
    st.chat_message("assistant").write("👋 **Hello!** I'm your AI guide today. To start, enter your API key in the sidebar and ask me: *'How do you generate text?'*")

# Display history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt.lower() in ["hi", "hello", "hey"]:
        st.balloons()

    if api_key:
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=model_choice,
                    messages=st.session_state.messages,
                    stream=True,
                )
                full_response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("👈 Please enter your Groq API Key in the sidebar!")