# MeetingMind 🧠

MeetingMind is a GenAI-powered meeting intelligence assistant that converts meeting transcripts into structured information.

## Features

- Upload `.txt`, `.pdf`, or `.docx` meeting transcripts
- Paste a transcript directly into the app
- Generate:
  - Meeting summary
  - Key discussion points
  - Decisions
  - Action items
  - Task owners
  - Deadlines
  - Unresolved issues
- Download the generated analysis as JSON

## Tech Stack

- Python
- Google Gemini API
- Streamlit
- LangChain
- PyPDF2
- python-docx
- NLP / text processing

## How it works

1. User uploads or pastes a meeting transcript.
2. MeetingMind extracts text from the input.
3. The transcript is sent to Gemini with a structured analysis prompt.
4. Gemini returns JSON containing the meeting insights.
5. Streamlit displays the results in an easy-to-read dashboard.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Enter your Gemini API key in the sidebar.

### API key

Create a Gemini API key through Google AI Studio and keep it private. Do not commit API keys to GitHub.

## Project Structure

```text
MeetingMind/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── sample_transcript.txt
```

## Example use case

A project team has a 30-minute meeting transcript. MeetingMind can identify what was discussed, what was decided, who owns each task, and which issues still need resolution.

## Limitations

- AI-generated information may contain mistakes.
- Owners and deadlines are reported as `Unknown` / `Not specified` when they are not present in the transcript.
- Very long transcripts may need to be split into smaller sections depending on model limits.
