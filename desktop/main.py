# main.py
import webview

# Create the window
webview.create_window("My Streamlit App", "http://localhost:8501", width=1024, height=768)

# This keeps the window running
webview.start()
