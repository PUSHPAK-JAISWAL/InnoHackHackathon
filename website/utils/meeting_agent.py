# utils/meeting_agent.py
import streamlit as st
from .schemas import MeetingProposal
from .ollama_handler import structured_ollama_call

def show_ui():
    st.header("Meeting Scheduler 🗓️")
    
    attendees = st.text_input("Attendees (comma separated)")
    duration = st.slider("Duration (minutes)", 15, 120, 30)
    purpose = st.text_area("Meeting Purpose")
    timezone = st.selectbox("Timezone", ["UTC", "IST", "PST", "CET"])
    
    if st.button("Generate Proposal"):
        result = schedule_meeting(attendees, duration, purpose, timezone)
        
        st.subheader("Meeting Proposal")
        st.markdown(f"**Best Time:** {result.suggested_time}")
        st.markdown("**Agenda:**")
        for item in result.agenda_items:
            st.write(f"- {item}")
        st.markdown(f"**Follow-up Actions:** {result.follow_up_actions}")

def schedule_meeting(attendees: str, duration: int, purpose: str, tz: str) -> MeetingProposal:
    prompt = f"""
    Create meeting proposal with:
    - Attendees: {attendees}
    - Duration: {duration} minutes
    - Purpose: {purpose}
    - Timezone: {tz}
    """
    return structured_ollama_call(
        prompt=prompt,
        response_model=MeetingProposal,
        model="gemma3"
    )