import re
import streamlit as st
from data_preprocessing import load_and_preprocess_data, get_recipe_details
from ai_matcher import RecipeMatcher

st.set_page_config(page_title="Food Recipe Chat", layout="wide")
st.markdown("""
    <h1 style='text-align:center; color:#ff7043; font-size:2.5em;'>
        🍽️ Chat & Discover Delicious Recipes Instantly!
    </h1>
    <p style='text-align:center; color:#444; font-size:1.2em; margin-bottom:25px;'>
        Tell me what you're in the mood for. I’ll suggest the best recipes from my collection.<br>
        Try:<em>low carb pasta</em>, <em>North Indian curry</em>, or <em>snacks with paneer</em>!
    </p>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

@st.cache_data
def load_data():
    return load_and_preprocess_data('food_data.csv')

df = load_data()
matcher = RecipeMatcher(df)

def extract_cook_time(text):
    match = re.search(r'(\d+)\s*min', text.lower())
    if match:
        return int(match.group(1))
    return None

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)


user_input = st.chat_input("What are you craving? perhaps a pasta or chicken biryani? ")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    requested_mins = extract_cook_time(user_input)
    raw_results = matcher.find_matching_recipes(user_input, top_k=10)
    filtered = []

    for rec in raw_results:
        times = rec['Times'] if isinstance(rec['Times'], dict) else {}
        cook_time_str = times.get('Cook time') or times.get('Cook Time') or times.get('Total Time') or ""
        cook_time_match = re.search(r'(\d+)', str(cook_time_str))
        rec_cook_time = int(cook_time_match.group(1)) if cook_time_match else None

        if requested_mins is not None:
            if rec_cook_time is not None and rec_cook_time <= requested_mins + 3:
                filtered.append(rec)
        else:
            filtered.append(rec)

    final_results = filtered if filtered else raw_results[:2]

    if final_results:
        messages = []
        for idx, result in enumerate(final_results[:2]):
            details = get_recipe_details(result)
            cook_time_line = ""
            times_lines = details['times'].splitlines()
            for line in times_lines:
                if "cook" in line.lower():
                    cook_time_line = line
                    break
            intro = [
                f"Here's a quick recipe for you:",
                f"This one is fast and tasty!",
                f"Perfect for when you're in a hurry:"
            ][idx % 3]

            block = (
                f"**{intro} [{details['name']}]**\n"
                f"*{cook_time_line}*\n"
                f"**Course:** {details['course']}   **Cuisine:** {details['cuisine']}\n"
                f"**Summary:** {details['summary']}\n"
                f"**Ingredients:** {details['ingredients']}\n"
                f"**Nutrition:**\n{details['nutritions']}\n"
                f"**Times:**\n{details['times']}\n"
            )
            if details['imgurl']:
                block += f"\n<img src='{details['imgurl']}' width='180'>\n"
            messages.append(block)
        reply = "\n---\n".join(messages)
        reply += "\n\nNeed something even quicker, or with fewer ingredients? Just ask!"
    else:
        reply = "Sorry, I couldn't find any recipes with that quick cook time. Try another keyword or time!"

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()
