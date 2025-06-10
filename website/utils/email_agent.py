# utils/email_agent.py
import streamlit as st
from .schemas import EmailContent
from .ollama_handler import structured_ollama_call

def show_ui():
    st.header("Email Generator 📧")
    
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("Tone Style", ["Formal", "Casual", "Persuasive", "Friendly"])
        key_points = st.text_area("Key Points", height=150)
    with col2:
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        purpose = st.text_input("Email Purpose")
    
    if st.button("Generate Email"):
        result = generate_email(tone, key_points, purpose, language)
        
        st.subheader("Generated Email")
        st.markdown(f"**Subject:** {result.subject}")
        st.markdown(result.body)
        st.download_button("Download Email", result.body, file_name="generated_email.txt")

def generate_email(tone: str, points: str, purpose: str, lang: str) -> EmailContent:
    prompt = f"""
    Generate professional email with these requirements:
    - Tone: {tone}
    - Language: {lang}
    - Purpose: {purpose}
    - Key points: {points}
    """
    return structured_ollama_call(
        prompt=prompt,
        response_model=EmailContent,
        model="gemma3"
    )