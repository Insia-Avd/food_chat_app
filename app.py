from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai

from utils import load_data

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def build_data_block(df):
    food_lines = []
    for idx, row in df.iterrows():
        food_lines.append(
            f"""Dish: {row['name']}
Course: {row['course']}
Cuisine: {row['cusine']}
Keywords: {row['keyword']}
Summary: {row['summary']}
Ingredients: {row['ingredients']}
Nutrition: {row['nutritions']}
Time: {row['Times']}
Image: {row['imgurl']}
"""
        )
    return "\n".join(food_lines)

def get_gemini_response(user_message, df):
    foods_block = build_data_block(df)
    prompt = f"""
You are a super helpful, friendly food assistant. Below is my entire food dataset.
Whenever the user asks a question, use this data ONLY to answer as precisely as possible in a chatty, engaging, and informative way.
If the user asks for a recipe, ingredients, dish suggestions, pairings, nutrition info, or details about any dish, use only what's in the data.
Never make up information. If you can't answer based on this data, say so.

DATA:
{foods_block}

USER: {user_message}
AI:"""
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if "quota" in str(e).lower() or "ResourceExhausted" in str(e):
            return "⚠️ Sorry, the AI's free quota was exceeded or too many requests were made. Please try again later."
        else:
            return f"⚠️ Sorry, something went wrong with the AI: {e}"

# --- Streamlit Page Config & Custom CSS ---
st.set_page_config(page_title="Food Chatbot", page_icon="🍲", layout="centered")
st.markdown("""
    <style>
        .center-title { text-align: center; font-size: 2em; margin-bottom: 0.12em; }
        .chat-bubble-ai {
            background-color: #F3F6FD;
            border-radius: 16px;
            padding: 0.98em 1.25em;
            margin-bottom: 0.6em;
            color: #222;
            box-shadow: 0 2px 12px rgba(61,128,223,0.05);
            font-size: 0.98em;
            line-height: 1.6;
        }
        .chat-bubble-user {
            background: linear-gradient(90deg, #e3ffe8 0%, #f6f9fa 100%);
            border-radius: 16px;
            padding: 0.98em 1.25em;
            margin-bottom: 0.6em;
            color: #244a32;
            font-size: 0.98em;
            line-height: 1.6;
        }
        .footer {
            text-align: center;
            font-size: 0.95em;
            color: #7b8791;
            margin-top: 1.7em;
            padding-top: 0.6em;
            border-top: 1px solid #eee;
            letter-spacing: 0.01em;
        }
        .stChatInput > div > textarea {
            font-size: 1.05em;
            border-radius: 9px;
        }
    </style>
""", unsafe_allow_html=True)

# ----- Sidebar -----
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2965/2965567.png", width=86)
    st.markdown("## 🍴 Food Recommender Chatbot")
    st.write("""
    **How to use:**  
    - Ask for dishes by type (e.g. 'main course', 'dessert', 'appetizer', 'vegan', etc.)  
    - Or request recipes and ingredients (e.g. 'recipe for Egg Halwa').  
    - The chatbot uses only your real menu data for accuracy!
    """)
    st.markdown("---")
    st.write("Made with ❤️ using Google Gemini & Streamlit.")

# ----- App Title -----
st.markdown('<div class="center-title">🍽️ Food Recommender Chatbot</div>', unsafe_allow_html=True)
st.divider()

df = load_data()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# ---- Display all previous chat messages ----
for entry in st.session_state.chat_history:
    if entry["who"] == "user":
        st.markdown(
            f'<div class="chat-bubble-user">'
            f'<span style="font-size:1.75em;vertical-align:middle;">💬</span> '
            f'{entry["msg"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bubble-ai">'
            f'<span style="font-size:1.75em;vertical-align:middle;">🍴</span> '
            f'{entry["msg"]}</div>',
            unsafe_allow_html=True
        )
        if entry.get("img"):
            st.image(entry["img"], width=170, use_container_width="auto", output_format="auto")

# ---- User input/chat ----
user_input = st.chat_input("What are you looking for today? (e.g., Pakistani main course, appetizer, vegan etc.)")

if user_input:
    st.session_state.chat_history.append({"who": "user", "msg": user_input, "img": None})
    st.rerun()

if st.session_state.chat_history and st.session_state.chat_history[-1]["who"] == "user":
    with st.spinner("Thinking..."):
        user_msg = st.session_state.chat_history[-1]["msg"]
        ai_msg = get_gemini_response(user_msg, df)

        img_url = None
        ai_msg_lower = ai_msg.lower()
        for idx, row in df.iterrows():
            if str(row['name']).lower() in ai_msg_lower:
                img_url = row['imgurl']
                break

        st.session_state.chat_history.append({"who": "ai", "msg": ai_msg, "img": img_url})
        st.rerun()

# ---- Footer ----
st.markdown(
    """
    <style>
    .footer-fixed {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        background: #fafbfc;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        font-size: 0.94em;
        color: #7b8791;
        padding: 0.5em 0 0.7em 0;
        z-index: 100;
    }
    </style>
    <div class="footer-fixed">
        <span style="font-size:0.92em;">
            Food Recommender Chatbot &copy; 2025 Insia &mdash; Developed for Upwork Client
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
