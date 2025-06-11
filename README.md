# T45_Solo_DEV

T45_Solo_DEV is a multi-agentic AI suite developed in Python, offering a powerful set of AI-driven tools accessible through web, desktop, and mobile platforms.

## Features

- **Resume Analyzer**: Instantly review and assess resumes for strengths and areas of improvement.
- **Fake News Detector**: Identify and flag potentially misleading or false information.
- **Code Debugger**: Analyze code for errors and get smart debugging suggestions.
- **Document Q&A**: Ask questions about documents and receive accurate, context-aware answers.
- **Meeting Scheduler**: Simplify scheduling with smart, AI-assisted meeting planning.
- **Email Generator**: Automatically generate professional emails based on your requirements.

## Technology Stack

- **Backend**: Python, [UV](https://www.uvicorn.org/), [Streamlit](https://streamlit.io/), [Ollama](https://ollama.com/)
- **Frontend/Web**: Streamlit web app
- **Desktop App**: [PyWebView](https://pywebview.flowrl.com/)
- **Mobile Apps**: Android and iOS wrappers using Expo (TypeScript) with WebView components

## Multi-Platform Support

- **Web**: Fully functional web application built with Streamlit.
- **Desktop**: Native-like desktop app using PyWebView.
- **Mobile**: Android and iOS applications built with Expo and WebView for a seamless mobile experience.

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/PUSHPAK-JAISWAL/T45_Solo_DEV.git
   cd T45_Solo_DEV
   ```
2. **Install Dependencies**
   - Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - For mobile and desktop apps, follow the respective subdirectory instructions.

3. **Run the Web App**
   ```bash
   streamlit run app.py
   ```

4. **Mobile & Desktop**
   - See `/mobile` and `/desktop` directories for platform-specific instructions.

## License

[MIT License](LICENSE)
