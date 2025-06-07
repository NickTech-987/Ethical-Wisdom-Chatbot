# %%
import streamlit as st
import pandas as pd
import openai
import os

# Set your OpenAI API Key 
openai.api_key = os.getenv("OPENAI_API_KEY") 


#  Load the CSV file
df = pd.read_csv("Quote_Master.csv", encoding="ISO-8859-1")
df.dropna(subset=['Quote', 'Category', 'Source', 'Religion'], inplace=True)

# --- Page Title & Intro ---
st.set_page_config(page_title="Ethical Wisdom Chatbot", layout="centered")
st.title("🧠 Ethical Wisdom Chatbot")
st.write("""
Ask about a moral or ethical theme like **Love**, **Faith**, **Peace**, or **Duty**.

This chatbot presents quotes from ancient scriptures such as the Gita, Bible, Quran, and more.
""")

# --- Function to fetch quotes by category ---
def find_quotes_by_category(category):
    mask = df['Category'].str.lower() == category.lower()
    filtered = df[mask]
    if not filtered.empty:
        return category, filtered
    else:
        return None

# --- Function to get GPT response ---
def get_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a wise assistant that shares ethical and spiritual wisdom from world scriptures like the Gita, Bible, Quran, and Guru Granth Sahib."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Error contacting GPT: {e}"

# --- User Input ---
user_input = st.text_input("Enter a theme (e.g., Love, Faith, Peace):")

# --- Response Logic ---
if user_input:
    result = find_quotes_by_category(user_input)
    if result:
        category, quotes = result
        st.subheader(f"📜 Quotes on {category.capitalize()}")
        for _, row in quotes.iterrows():
            st.markdown(f"""
> "{row['Quote']}"

**Source:** {row['Source']}  
**Religion:** {row['Religion']}
""")
    else:
        st.subheader("💬 No quotes found in the CSV. Here's a GPT-generated insight:")
        gpt_response = get_gpt_response(f"Give a spiritual or ethical quote about {user_input}.")
        st.markdown(gpt_response)






