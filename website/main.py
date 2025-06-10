import streamlit as st
import hashlib
from PIL import Image
from utils import (
    document_qa,
    email_agent,
    meeting_agent,
    resume_parser,
    news_validator,
    code_analyzer,
)

# Page configuration & custom CSS
st.set_page_config(
    page_title="AI Agent Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

custom_css = '''
<style>
/* Global */
body {
    background-color: #f4f6f8;
}
.stApp {
    font-family: 'Source Sans Pro', sans-serif;
}
/* Sidebar */
.css-1d391kg, .css-1d391kg .css-1v3fvcr {
    background: #2c3e50;
    color: #ecf0f1;
}
.css-1d391kg .st-bf {
    color: #ecf0f1;
}
.stSidebar .stButton>button {
    margin-top: 0.5em;
    width: 100%;
    border-radius: 8px;
    background: #e67e22;
    color: white;
}
/* Buttons */
.stButton>button {
    border-radius: 8px;
    padding: 0.6em 2em;
    background: linear-gradient(90deg, #36D1DC 0%, #5B86E5 100%);
    color: white;
    font-size: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
/* Cards and Containers */
.card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    padding: 1.5em;
    margin-bottom: 1em;
}
</style>
'''
st.markdown(custom_css, unsafe_allow_html=True)

# Authentication Handlers
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'auth' not in st.session_state:
    st.session_state.auth = {'logged_in': False, 'user': None}

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def login_form():
    st.header("🔑 Login")
    with st.form('login'):
        u = st.text_input('Username')
        pw = st.text_input('Password', type='password')
        if st.form_submit_button('Login'):
            if u in st.session_state.users and st.session_state.users[u]['password'] == hash_password(pw):
                st.session_state.auth = {'logged_in': True, 'user': u}
                st.success('Logged in successfully!')
            else:
                st.error('Invalid username or password')

def signup_form():
    st.header("🆕 Sign Up")
    with st.form('signup'):
        u = st.text_input('Choose Username')
        pw = st.text_input('Choose Password', type='password')
        if st.form_submit_button('Create Account'):
            if u in st.session_state.users:
                st.error('Username already exists')
            elif len(pw) < 8:
                st.error('Password must be at least 8 characters')
            else:
                st.session_state.users[u] = {'password': hash_password(pw), 'history': []}
                st.success('Account created! Please login.')

# Pages

def show_about():
    st.title('About AI Agent Suite')
    st.write('Revolutionizing workflows with AI-powered tools.')
    with st.expander('🌟 Features'):
        st.write('- Resume Analyzer: Smart CV/job matching')
        st.write('- News Validator: Fake news detection')
        st.write('- Code Inspector: Security-aware code analysis')
        st.write('- Document Q&A: Instant QA on documents')
        st.write('- Email Generator & Meeting Scheduler')

    cols = st.columns(2)
    with cols[0]:
        st.subheader('AI Stack')
        st.write('- NLP & Semantic Analysis')
        st.write('- Pattern Recognition')
        st.write('- Real-time Validation')
    with cols[1]:
        st.subheader('Core Team')
        st.write('- Pushpak Jaiswal: AI Engineer')
        st.write('- Pushpak Jaiswal: Full-stack Dev')
        st.write('- Pushpak Jaiswal: Security')
        st.write('- Pushpak Jaiswal: UX Designer')

    st.caption('© 2025 AI Agent Suite')

def main_app():
    st.sidebar.markdown(f"### Welcome, {st.session_state.auth['user']}")
    if st.sidebar.button('Logout'):
        st.session_state.auth = {'logged_in': False, 'user': None}
        st.success('Logged out successfully!')

    page = st.sidebar.radio('Navigate', [
        'Resume Analyzer', 'News Validator', 'Code Inspector',
        'Document Q&A', 'Email Generator', 'Meeting Scheduler', 'About'
    ])

    if page == 'Resume Analyzer':
        resume_parser.show_ui()
    elif page == 'News Validator':
        news_validator.show_ui()
    elif page == 'Code Inspector':
        code_analyzer.show_ui()
    elif page == 'Document Q&A':
        document_qa.show_ui()
    elif page == 'Email Generator':
        email_agent.show_ui()
    elif page == 'Meeting Scheduler':
        meeting_agent.show_ui()
    else:
        show_about()


def landing_page():
    st.title('AI Agent Suite')
    tab1, tab2 = st.tabs(['Login', 'Sign Up'])
    with tab1:
        login_form()
    with tab2:
        signup_form()


def main():
    if not st.session_state.auth['logged_in']:
        landing_page()
    else:
        main_app()

if __name__ == '__main__':
    main()
