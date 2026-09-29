import os
import json
import re
import streamlit as st
from google import genai
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="MeetingMind", page_icon="🧠", layout="wide")

st.title("🧠 MeetingMind")
st.caption("AI-powered meeting transcript assistant")

def read_file(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file type.")

def extract_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("The AI response was not valid JSON.")
    return json.loads(match.group(0))

def analyze_meeting(transcript, api_key, model_name):
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are MeetingMind, a meeting intelligence assistant.
Analyze the meeting transcript below and return ONLY valid JSON with this exact structure:

{{
  "summary": "3-6 sentence concise summary",
  "key_points": ["point 1", "point 2"],
  "decisions": ["decision 1"],
  "action_items": [
    {{"task": "task description", "owner": "person or Unknown", "deadline": "deadline or Not specified"}}
  ],
  "unresolved_issues": ["issue 1"]
}}

Do not invent facts. If an owner or deadline is not present, use "Unknown" or "Not specified".

TRANSCRIPT:
{transcript}
"""
    response = client.models.generate_content(model=model_name, contents=prompt)
    return extract_json(response.text)

st.sidebar.header("Settings")

api_key = st.secrets["GEMINI_API_KEY"]
model_name = "gemini-3.8-flash"

uploaded = st.file_uploader("Upload a meeting transcript", type=["txt", "pdf", "docx"])

st.markdown("**Or paste your transcript below:**")
transcript = st.text_area("Meeting transcript", height=250, placeholder="Paste transcript here...")

if st.button("✨ Analyze Meeting", type="primary"):
    if not api_key:
        st.error("Gemini API key is not configured.")
    else:
        try:
            if uploaded:
                transcript_text = read_file(uploaded)
            else:
                transcript_text = transcript.strip()

            if not transcript_text:
                st.warning("Please upload a transcript or paste one.")
            elif len(transcript_text) < 30:
                st.warning("Please provide a longer transcript for meaningful analysis.")
            else:
                with st.spinner("Analyzing meeting..."):
                    result = analyze_meeting(transcript_text, api_key, model_name)

                st.success("Meeting analysis complete!")

                st.subheader("📝 Summary")
                st.write(result.get("summary", "Not available"))

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🔑 Key Points")
                    for item in result.get("key_points", []):
                        st.write(f"• {item}")

                    st.subheader("✅ Decisions")
                    for item in result.get("decisions", []):
                        st.write(f"• {item}")

                with col2:
                    st.subheader("📌 Action Items")
                    actions = result.get("action_items", [])
                    if actions:
                        st.dataframe(actions, use_container_width=True, hide_index=True)
                    else:
                        st.write("No action items identified.")

                    st.subheader("❓ Unresolved Issues")
                    for item in result.get("unresolved_issues", []):
                        st.write(f"• {item}")

                st.download_button(
                    "⬇️ Download JSON Report",
                    data=json.dumps(result, indent=2, ensure_ascii=False),
                    file_name="meetingmind_report.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()
st.caption("MeetingMind | Python • Gemini API • Streamlit • LangChain • NLP")
