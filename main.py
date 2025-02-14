import streamlit as st
import requests
from newspaper import Article
import groq

# Initialize Groq Client
GROQ_API_KEY = st.secrets["API_KEY"]  # Securely fetch API key
client = groq.Client(api_key=GROQ_API_KEY)

# Function to fetch and summarize an article
def fetch_and_summarize(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        content = article.text

        # Use Groq AI to summarize the content
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Use an available Groq model
            messages=[
                {"role": "system", "content": "Summarize the following news article in key bullet points."},
                {"role": "user", "content": content}
            ],
        )

        summary = response.choices[0].message.content
        return article.title, summary

    except Exception as e:
        return None, f"Error: {str(e)}"

# Streamlit UI
st.title("📰 AI-Powered News Summarizer (Groq)")

url = st.text_input("Enter News Article URL:")
if st.button("Summarize"):
    if url:
        title, summary = fetch_and_summarize(url)
        st.subheader(f"📌 {title}")
        st.write(summary)
    else:
        st.warning("Please enter a valid URL.")
