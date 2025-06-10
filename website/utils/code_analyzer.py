import streamlit as st
from .schemas import CodeAnalysis
from .ollama_handler import structured_ollama_call

# Supported file extensions mapped to languages
EXT_LANG_MAP = {
    "py": "Python",
    "js": "JavaScript",
    "java": "Java",
    "cpp": "C++",
    "c": "C"
}

def analyze_code(code: str, lang: str) -> CodeAnalysis:
    """Call the LLM to analyze code for bugs, security issues, optimizations, and complexity."""
    prompt = f"""
Analyze this {lang} code for bugs, security issues, optimizations, and complexity.
Return JSON with:
- overall_score: int
- bugs: list of {{description, severity, line_number, fix_suggestion}}
- optimizations: list of str
- security_issues: list of str
- complexity_analysis: dict
Code:
{code}
"""
    return structured_ollama_call(
        prompt=prompt,
        response_model=CodeAnalysis,
        model="gemma3"
    )

def show_ui():
    st.header("Code Inspector 🐞")
    st.write("Upload code files or paste code below, then click Analyze to invoke the LLM.")

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload Code Files", type=list(EXT_LANG_MAP.keys()), accept_multiple_files=True
    )

    # Prepare session state for contents and results
    if "file_contents" not in st.session_state:
        st.session_state.file_contents = {}  # name -> (lang, code)
    if "code_results" not in st.session_state:
        st.session_state.code_results = {}  # key -> CodeAnalysis

    # Read and store uploaded files
    if uploaded_files:
        for file in uploaded_files:
            name = file.name
            if name not in st.session_state.file_contents:
                ext = name.split('.')[-1]
                lang = EXT_LANG_MAP.get(ext, "Unknown")
                code = file.read().decode('utf-8', 'ignore')
                st.session_state.file_contents[name] = (lang, code)

    # Display uploaded files with analyze buttons
    for name, (lang, code) in st.session_state.file_contents.items():
        with st.expander(f"{name} ({lang})", expanded=False):
            st.code(code, language=lang.lower())
            analyze_btn = st.button(f"Analyze {name}", key=f"analyze_{name}")
            if analyze_btn:
                with st.spinner(f"Analyzing {name}…"):
                    st.session_state.code_results[name] = analyze_code(code, lang)

    # Text area fallback
    st.markdown("---")
    code_fallback = st.text_area("Or paste code here", height=200)
    fallback_lang = st.selectbox("Language for pasted code", list(EXT_LANG_MAP.values()), key="fallback_lang")
    analyze_paste = st.button("Analyze Pasted Code")
    if analyze_paste and code_fallback.strip():
        key = f"Pasted::{fallback_lang}" + code_fallback[:30]
        with st.spinner("Analyzing pasted code…"):
            st.session_state.code_results[key] = analyze_code(code_fallback, fallback_lang)

    # Display results
    for key, result in st.session_state.code_results.items():
        title = key if not key.startswith("Pasted::") else "Pasted Code"
        with st.expander(f"Results: {title}", expanded=True):
            tabs = st.tabs(["Overview", "Bugs", "Optimizations", "Security", "Complexity"])
            with tabs[0]:
                st.metric("Overall Score", f"{result.overall_score}/100")
            with tabs[1]:
                if result.bugs:
                    for bug in result.bugs:
                        st.markdown(
                            f"### 🐞 {bug.description}\n**Severity:** {bug.severity}  \n**Line:** {bug.line_number or 'N/A'}  \n**Fix:** {bug.fix_suggestion}"
                        )
                else:
                    st.write("No bugs detected.")
            with tabs[2]:
                st.write("No optimizations suggested." if not result.optimizations else "")
                for opt in result.optimizations or []:
                    st.markdown(f"- 🚀 {opt}")
            with tabs[3]:
                st.write("No security issues found." if not result.security_issues else "")
                for sec in result.security_issues or []:
                    st.markdown(f"- 🔒 {sec}")
            with tabs[4]:
                st.json(result.complexity_analysis)
            st.markdown("---")


