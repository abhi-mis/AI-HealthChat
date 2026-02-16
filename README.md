# HealthChat POC - 2-Person Chat with NLP Insights

A Streamlit-based Proof-of-Concept demonstrating a side-by-side chat application for Patients and Doctors, featuring real-time mood analysis using spaCy NLP.

## Features
- **Dual Perspective:** Side-by-side windows for Patient and Doctor on a single screen.
- **NLP Mood Detection:** Analyzes patient replies to detect tones such as Worried, Happy, Angry, Calm, or Neutral.
- **Session Intelligence:** Captures doctor's last message as reference context.
- **Premium UI:** Custom CSS for a modern, healthcare-themed interface.
- **Deployable:** Fully compatible with Streamlit Community Cloud.

## Tech Stack
- **Frontend:** Streamlit
- **NLP Logic:** spaCy (`en_core_web_sm`)
- **Language:** Python 3.9+

## Local Setup
1. Clone the repository or download the files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Workflow
1. Use the **Left Panel** (Patient) to send messages.
2. The **Right Panel** (Doctor) will immediately show:
   - The message in the chat history.
   - An **AI Insight** card showing the detected mood of the patient.
   - A short descriptive analysis of the tone.
3. Use the **Right Panel** (Doctor) to respond to the patient.
