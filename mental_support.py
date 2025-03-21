'''import streamlit as st
import ollama
import base64

st.set_page_config(page_title="Mental Health Chatbot")

def get_base64(background):
    with open(background,"rb") as f:
        data=f.read()
    return base64.b64encode(data).decode()

bin_str= get_base64("background.png")

st.markdown(f"""
        <style>
            .stApp{{
            background-image:url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat:no-repeat;

            }}
        </style>
        """,unsafe_allow_html=True)

st.session_state.setdefault('converstion_history',[])

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

def generate_response(user_input):
    st.session_state['conversation_history'].append({"role":"user","content":user_input})

    response= ollama.chat(model="tinyllama", messages=st.session_state['conversation_history'])
    ai_response=response['message']['content']

    st.session_state['conversation_history'].append({"role":"assistant","content":ai_response})
    return ai_response

def generate_affirmation():
    prompt= "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed"
    response= ollama.chat(model="tinyllama",messages=[{"role":"user","content":prompt}])
    return response['message']['content']

def generate_meditation_guide():
    prompt= "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response= ollama.chat(model="tinyllama",messages=[{"role":"user","content":prompt}])
    return response['message']['content']

st.title("Mental Health Support Agent")

for msg in st.session_state['conversation_history']:
    role= "You" if msg['role']== "user" else "AI"
    st.markdown(f"**{role}:**{msg['content']}")

user_message= st.text_input("How can I help today?")

if user_message:
    with st.spinner("Thinking......"):
        ai_response= generate_response(user_message)
        st.markdown(f"**AI:**{ai_response}")




col1, col2=st.columns(2)

with col1:
    if st.button("Give me a positive Affirmation"):
        affirmation= generate_affirmation()
        st.markdown(f"**Affirmation:**{affirmation}")

with col2:
    if st.button("Give me a guided meditation"):
        meditation_guide= generate_meditation_guide()
        st.markdown(f"**Guided Meditation:**{meditation_guide}")'''



import streamlit as st
import openai
import base64

# Set your OpenAI API key here (you can also set it as a Streamlit secret)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "YOUR_OPENAI_API_KEY"

# Page config
st.set_page_config(page_title="Mental Health Chatbot")

# Function to get background image in base64
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set background image
bin_str = get_base64("background.png")

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
""", unsafe_allow_html=True)

# Initialize conversation history in session state
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Function to generate a response from OpenAI ChatGPT
def generate_response(user_input):
    # Append user message to the conversation history
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})

    # Send the conversation to OpenAI and get a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['conversation_history']
    )

    ai_response = response['choices'][0]['message']['content']

    # Append AI response to conversation history
    st.session_state['conversation_history'].append({"role": "assistant", "content": ai_response})

    return ai_response

# Function to generate a positive affirmation
def generate_affirmation():
    prompt = "Provide a positive affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Function to generate a 5-minute guided meditation
def generate_meditation_guide():
    prompt = "Provide a 5-minute guided meditation script to help someone relax and reduce stress."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# UI - Title
st.title("🧘 Mental Health Support Agent")

# Display previous conversation
for msg in st.session_state['conversation_history']:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# User input for conversation
user_message = st.text_input("How can I help today?")

if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

# Two columns for buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Give me a Positive Affirmation"):
        with st.spinner("Generating affirmation..."):
            affirmation = generate_affirmation()
            st.markdown(f"**Affirmation:** {affirmation}")

with col2:
    if st.button("Give me a Guided Meditation"):
        with st.spinner("Generating meditation guide..."):
            meditation_guide = generate_meditation_guide()
            st.markdown(f"**Guided Meditation:** {meditation_guide}")
