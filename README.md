# 🍲 Food Recommender Chatbot

A Streamlit-based chatbot that suggests dishes, recipes, and ingredients based strictly on your real menu data, powered by Google Gemini API.
---

## 🚀 Features
- Natural chat interface for food discovery, recipes, and more
- Uses your own dataset (`food_data.csv`)
- Google Gemini API integration
- Friendly, aesthetic, and customizable UI
---

## ⚙️ Setup Instructions
### 1. Clone the Repository
```sh
git clone https://github.com/Insia-Avd/yourproject.git
cd yourproject

###2. Install Dependencies
Create a virtual environment (recommended) and install requirements:
sh
Copy
Edit
pip install -r requirements.txt

###3. Environment Variables
For security:
Your sensitive keys should NOT be stored in the repo.
This project uses a .env file for secrets.
The repo contains a .env.example file with variable names.
Do not use your real API key in .env.example!

Steps:
Make a copy of .env.example and rename it to .env:
bash
Copy
Edit
cp .env.example .env
Open .env and add your actual Google API key:
ini
Copy
Edit
GOOGLE_API_KEY=your_real_api_key_here

###4. Add Your Dataset
Place your food_data.csv in the project folder.
Ensure the column headers match those expected in the code.

###5. Run the App
sh
Copy
Edit
streamlit run app.py
