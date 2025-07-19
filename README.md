Food Recipe Chatbot
A conversational Streamlit web app that lets you search for food recipes by natural language chat, using semantic search and AI!
Just tell the bot what you’re craving ("quick healthy pasta", "snacks with mushrooms"), and get smart recommendations with detailed nutrition and cooking times.


🚀 Features
Chatbot interface: Friendly, conversational UI powered by Streamlit’s modern chat features.
Semantic recipe matching: Uses state-of-the-art Sentence Transformers to understand your intent and ingredients.
Rich responses: Shows recipe images, ingredients, nutrition facts, and summary for each result.
Handles diverse queries: Search by cuisine, course, cook/prep time, keywords, or ingredient names.
Easy to extend: Modular Python code for data processing, AI matching, and the app interface.

🛠️ Setup & Usage
Clone this repository:
bash
Copy
Edit
git clone https://github.com/Insia-Avd/food-recipe-chatbot.git
cd food-recipe-chatbot

Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt

Prepare data:
Place your food_data.csv file inside the data/ directory.
The CSV should include fields like: name, course, cusine, keyword, summary, ingredients, nutritions, Times, imgurl.

Run the app:
bash
Copy
Edit
streamlit run app.py
Chat with the bot:
Type your food query in plain English and get instant recommendations!

🧠 Project Structure
app.py - Main Streamlit app and chatbot UI logic.
data_preprocessing.py - CSV loading and text enrichment for better search.
ai_matcher.py - RecipeMatcher class using Sentence Transformers.
data/food_data.csv - Recipe data (see above).
requirements.txt - All Python dependencies.

📦 Requirements
Python 3.8+
Streamlit 1.30+
pandas, sentence-transformers, torch, ast (standard library)
Your recipe CSV data

⚡ Example Queries
quick italian pasta
north indian main course
high protein vegan salad
snacks with mushrooms

⚠️ Known Limitations
Cook/prep time filtering is approximate:
If you type “5 mins cook time”, the system tries to find recipes with a similar time, but due to inconsistent time formatting in data and limitations in natural language extraction, results may include recipes with longer cook times.
Tip: Use precise phrases and check the returned time in the response.
No complex reasoning:
The chatbot cannot explain recipe steps, substitute ingredients, or hold long-term multi-turn memory about your preferences.
Data dependency:
Recipe recommendations are only as good as your food_data.csv. If times or nutrition fields are missing or poorly formatted, results may not be relevant.
Limited dietary filtering:
Nutrition-based and allergen filtering (e.g. “no peanuts”, “low sodium”) is not strict and may not always work as expected.
No user personalization:
The bot does not remember user dietary preferences, liked/disliked recipes, or previous sessions.
Limited error handling:
Very unusual queries or malformed CSVs may cause errors or irrelevant answers.
No cloud/deployment out of the box:
This is a local app. For deployment (Heroku, AWS, etc.), extra configuration is required.
Model is local only:
All AI runs locally. HuggingFace APIs or online LLMs are not integrated by default.

📝 Acknowledgments
Built using Streamlit and sentence-transformers.
Recipe dataset: (provide your source or state if proprietary).
Inspired by modern food apps and AI chat assistants.

💡 How to Improve
Use more advanced NLP for stricter time/dietary filtering.
Integrate a local LLM for chat rephrasing and more “human” conversations.
Add user accounts and favorites.
Improve UI with custom avatars, clickable filters, or rich cards.
Deploy to the cloud for public sharing.

📬 Feedback & Issues
If you run into bugs or have suggestions, please open an issue or PR on GitHub!

Enjoy chatting about food! 🍲
