# utils/document_qa.py
import streamlit as st
import PyPDF2
from docx import Document
from io import BytesIO
from .schemas import QAResponse
from .ollama_handler import structured_ollama_call
from typing import Union

def parse_document(file: Union[bytes, str]) -> str:
    """Parse different document formats with error handling and text normalization"""
    try:
        if file.type == "application/pdf":
            return parse_pdf(file)
        elif file.type == "text/plain":
            return parse_txt(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return parse_docx(file)
        else:
            st.error(f"Unsupported file format: {file.type}")
            return ""
    except Exception as e:
        st.error(f"Error parsing document: {str(e)}")
        return ""

def parse_pdf(file) -> str:
    """Extract text from PDF with page normalization"""
    pdf = PyPDF2.PdfReader(BytesIO(file.getvalue()))
    text = []
    for page in pdf.pages:
        page_text = page.extract_text() or ""
        # Normalize whitespace and clean text
        text.append(" ".join(page_text.replace("\n", " ").split()))
    return " ".join(text)[:5000]  # Truncate to 5000 chars

def parse_docx(file) -> str:
    """Extract text from DOCX with paragraph joining"""
    doc = Document(BytesIO(file.getvalue()))
    return "\n".join([
        " ".join(para.text.replace("\n", " ").split())
        for para in doc.paragraphs
        if para.text.strip()
    ])[:5000]

def parse_txt(file) -> str:
    """Read and clean text from TXT file"""
    try:
        text = file.getvalue().decode("utf-8")
    except UnicodeDecodeError:
        text = file.getvalue().decode("latin-1")
    return " ".join(text.replace("\n", " ").split())[:5000]

def analyze_document(text: str, question: str) -> QAResponse:
    """Analyze document content with context-aware prompting"""
    prompt = f"""
    Answer this question based EXCLUSIVELY on the provided document content.
    If the answer isn't found, state that clearly.
    
    Question: {question}
    Document Content: {text}
    
    Format your response with:
    - Direct answer in first line
    - Confidence percentage (0-100)
    - Up to 3 relevant excerpts from the document
    - 2-3 suggested follow-up questions
    """
    return structured_ollama_call(
        prompt=prompt,
        response_model=QAResponse,
        model="gemma3"
    )

def show_ui():
    st.header("Document Q&A Agent 📑")
    
    doc = st.file_uploader(
        "Upload Document",
        type=["pdf", "txt", "docx"],
        help="Supported formats: PDF, TXT, DOCX (max 5MB)"
    )
    
    if doc:
        with st.expander("Preview First 500 Characters"):
            text_preview = parse_document(doc)[:500]
            st.write(text_preview + "..." if len(text_preview) == 500 else text_preview)
    
    question = st.text_input("Ask about the document", placeholder="What is the main purpose of this document?")
    
    if doc and question:
        with st.spinner("Analyzing document..."):
            text = parse_document(doc)
            if not text:
                st.error("Failed to extract text from document")
                return
            
            result = analyze_document(text, question)
            
            st.subheader("Answer")
            st.markdown(f"**{result.answer}**")
            st.progress(result.confidence/100)
            
            if result.sources:
                st.markdown("**Relevant Sections:**")
                for source in result.sources[:3]:
                    st.markdown(f"- `...{source}...`")
            
            if result.related_questions:
                st.markdown("**Suggested Follow-up Questions:**")
                for q in result.related_questions[:3]:
                    st.markdown(f"- *{q}*")