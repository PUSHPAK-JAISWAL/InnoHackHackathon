import streamlit as st
from googlesearch import search
from .schemas import NewsAnalysis
from .ollama_handler import structured_ollama_call
import PyPDF2
import hashlib
from datetime import datetime
import time
import re

# Enhanced prompt template
PROMPT_TEMPLATE = """
**Current Date:** {current_date}
**News Content:** 
{content}

**Sources Found:**
{formatted_sources}

**Analysis Instructions:**
1. Determine if the news is authentic based SOLELY on the sources above
2. Set 'is_fake' to TRUE ONLY if the news is fabricated or disproven by evidence
3. Set 'is_fake' to FALSE if the news is confirmed by sources
4. Provide confidence percentage (0-100) based on source consistency
5. List specific reasons with source references
6. Extract related entities (people/orgs/locations)
7. Rate source credibility (0-100) based on domain authority
8. List supporting evidence URLs
9. Focus on current events - assume today is {current_date}
10. For sports/news events:
    - Prioritize sports/news domains
    - Verify dates and locations
    - Check for consistent reporting across sources

**Key Definition:**
- is_fake = True → News is fabricated/inaccurate
- is_fake = False → News is authentic/accurate
"""

def safe_google_search(query, num_results=3):
    """Wrapper for googlesearch with error handling"""
    try:
        results = []
        for result in search(query, num_results=num_results, advanced=True, sleep_interval=2):
            try:
                domain = result.url.split('/')[2] if len(result.url.split('/')) > 2 else result.url
                results.append({
                    "title": result.title,
                    "url": result.url,
                    "domain": domain
                })
            except Exception as e:
                print(f"Error processing result: {e}")
        return results
    except Exception as e:
        st.error(f"Search encountered an issue: {str(e)}")
        return []

def extract_keywords(content):
    """Extract important keywords for better search"""
    words = re.findall(r'\b[A-Z][a-z]+\b', content)
    unique_words = list(set(words))
    return " ".join(unique_words[:5])  # Return top 5 unique capitalized words

def validate_news(content: str) -> NewsAnalysis:
    try:
        # Get current date context
        current_date = datetime.now().strftime("%B %d, %Y")
        current_year = datetime.now().year
        
        # Extract keywords for better search
        keywords = extract_keywords(content)
        if not keywords:
            keywords = content[:50]  # Fallback to first 50 characters
        
        # Enhanced search with keywords and context
        query = f"{keywords} {current_year}"
        
        # Add domain prioritization for sports/news
        if "cricket" in content.lower() or "ipl" in content.lower():
            query += " site:espncricinfo.com OR site:cricbuzz.com"
        
        sources = safe_google_search(query, 5)
        
        # Format sources with metadata
        formatted_sources = "\n".join(
            [f"- [{s['title']}]({s['url']}) (Domain: {s['domain']})" 
             for s in sources]
        ) if sources else "No sources available"
    except Exception as e:
        st.error(f"Search setup failed: {e}")
        formatted_sources = "No sources available"

    # Build detailed prompt with special instructions
    prompt = PROMPT_TEMPLATE.format(
        content=content,
        formatted_sources=formatted_sources,
        current_date=current_date
    )
    
    # Add special handling for sports/news
    if "cricket" in content.lower() or "ipl" in content.lower():
        prompt += "\n\n**Sports News Context:**\n" \
                  "Verify using sports-specific domains. Recent matches might have limited coverage. " \
                  "Focus on official team/league sites when available."

    return structured_ollama_call(
        prompt=prompt,
        response_model=NewsAnalysis,
        model="gemma3"
    )

def show_ui():
    st.header("📰 News Validator")
    input_type = st.radio("Input Type", ["Text", "URL", "File"], horizontal=True)
    content = ""

    if input_type == "Text":
        content = st.text_area("Paste News Content", height=250,
                              placeholder="Paste news content here...")
    elif input_type == "URL":
        content = st.text_input("Enter News URL", 
                               placeholder="https://example.com/news-article")
    else:
        file = st.file_uploader("Upload News File (PDF or Text)", type=["txt", "pdf"])
        if file:
            if file.type == "application/pdf":
                try:
                    reader = PyPDF2.PdfReader(file)
                    content = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                except Exception as e:
                    st.error(f"PDF error: {e}")
                    content = ""
            else:
                try:
                    content = file.read().decode("utf-8")
                except Exception as e:
                    st.error(f"File error: {e}")
                    content = ""

    # Use hash for consistent caching
    if "news_results" not in st.session_state:
        st.session_state.news_results = {}

    if st.button("🔍 Validate News", type="primary") and content:
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        if content_hash not in st.session_state.news_results:
            with st.spinner("Analyzing news content..."):
                try:
                    result = validate_news(content)
                    st.session_state.news_results[content_hash] = result
                except Exception as e:
                    st.error(f"Validation failed: {e}")
                    # Create default response
                    st.session_state.news_results[content_hash] = NewsAnalysis(
                        is_fake=False,
                        confidence=0,
                        reasons=["Validation process encountered an error"],
                        related_entities=[],
                        source_credibility=0,
                        supporting_evidence=[]
                    )

    # Display results
    for key, result in st.session_state.news_results.items():
        with st.expander("📝 News Analysis Report", expanded=True):
            # Status indicator with confidence
            if result.is_fake:
                status = "❌ Fake News"
                color = "red"
                icon = "⚠️"
            else:
                status = "✅ Authentic News"
                color = "green"
                icon = "✔️"
                
            st.subheader(f"{icon} :{color}[{status}] ({result.confidence}% confidence)")
            
            # Confidence meter with color coding
            confidence_color = "red" if result.confidence < 40 else "orange" if result.confidence < 70 else "green"
            st.progress(result.confidence / 100, text=f"Confidence Level: {result.confidence}%")
            
            # Two-column layout
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("🔍 Analysis Details")
                with st.container(border=True):
                    st.markdown("**📋 Reasons**")
                    if result.reasons:
                        for reason in result.reasons:
                            st.info(f"- {reason}")
                    else:
                        st.warning("No analysis reasons provided")
                
                with st.container(border=True):
                    st.markdown("**🏷️ Related Entities**")
                    if result.related_entities:
                        for ent in result.related_entities:
                            st.write(f"- {ent}")
                    else:
                        st.info("No entities identified")

            with col2:
                st.subheader("📚 Source Evaluation")
                with st.container(border=True):
                    st.markdown("**⭐ Source Credibility**")
                    # Visual credibility indicator
                    credibility_color = "red" if result.source_credibility < 40 else "orange" if result.source_credibility < 70 else "green"
                    st.markdown(f"<div style='color:{credibility_color}; font-size: 24px;'>{result.source_credibility}/100</div>", 
                                unsafe_allow_html=True)
                    st.caption("Higher is better (based on domain authority and consistency)")
                
                with st.container(border=True):
                    st.markdown("**🔗 Supporting Evidence**")
                    if result.supporting_evidence:
                        for ev in result.supporting_evidence:
                            st.success(f"- {ev}")
                    else:
                        st.warning("No supporting evidence found")

            # Add disclaimer
            st.caption("ℹ️ Note: Analysis is based on available web sources. Confidence scores reflect consistency across sources. "
                       "Recent events might have limited coverage.")