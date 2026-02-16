import streamlit as st
import spacy
from datetime import datetime

st.set_page_config(
    page_title="HealthChat POC - Patient & Doctor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        return None

nlp = load_nlp()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #ffffff;
    }

    [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }

    .main {
        background: #ffffff;
        padding: 2rem 1rem !important;
        max-width: 1400px;
        margin: 0 auto;
    }

    .main-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }

    .main-header p {
        color: #666666;
        font-size: 1rem;
        margin: 0;
    }

    .section-title {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #000000;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #000000;
    }

    .chat-box {
        background: #ffffff;
        border: 2px solid #000000;
        padding: 2rem;
        min-height: 400px;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 2rem;
    }

    .chat-box::-webkit-scrollbar {
        width: 6px;
    }

    .chat-box::-webkit-scrollbar-track {
        background: #f5f5f5;
    }

    .chat-box::-webkit-scrollbar-thumb {
        background: #cccccc;
    }

    .message {
        margin-bottom: 1.5rem;
        padding: 1rem;
        border: 1px solid #e0e0e0;
    }

    .message-header {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #666666;
        margin-bottom: 0.5rem;
    }

    .message-content {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #000000;
    }

    .patient-msg {
        background: #f5f5f5;
        border-left: 4px solid #000000;
    }

    .doctor-msg {
        background: #ffffff;
        border-left: 4px solid #666666;
    }

    .highlight-msg {
        border: 2px solid #000000;
        background: #fafafa;
    }

    .empty-state {
        text-align: center;
        color: #999999;
        padding: 3rem;
        font-size: 0.9rem;
    }

    .mood-detector {
        background: #000000;
        color: #ffffff;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 2px solid #000000;
    }

    .mood-header {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
        opacity: 0.7;
    }

    .mood-status {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .mood-description {
        font-size: 0.95rem;
        line-height: 1.6;
        opacity: 0.9;
    }

    .context-box {
        background: #f5f5f5;
        border-left: 3px solid #000000;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.875rem;
        color: #333333;
    }

    .context-label {
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        color: #000000;
        margin-bottom: 0.25rem;
    }

    .input-section {
        margin-bottom: 2rem;
    }

    [data-testid="stForm"] {
        background: #fafafa;
        border: 2px solid #e0e0e0;
        padding: 1.5rem;
    }

    [data-testid="stTextInput"] input {
        background: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 0 !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
        color: #000000 !important;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #000000 !important;
        outline: none !important;
        box-shadow: none !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #999999 !important;
    }

    [data-testid="stFormSubmitButton"] button {
        background: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #000000 !important;
        border-radius: 0 !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        cursor: pointer !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background: #ffffff !important;
        color: #000000 !important;
    }

    .footer {
        text-align: center;
        padding: 2rem;
        border-top: 2px solid #e0e0e0;
        margin-top: 3rem;
    }

    .footer p {
        color: #666666;
        font-size: 0.85rem;
        margin: 0.25rem 0;
    }

    [data-testid="column"] {
        padding: 0 1rem !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    label {
        display: none !important;
    }

    hr {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "patient_mood" not in st.session_state:
    st.session_state.patient_mood = {"mood": "Neutral", "desc": "No patient input yet.", "message_type": ""}
if "last_doctor_msg" not in st.session_state:
    st.session_state.last_doctor_msg = ""
if "last_analyzed_message" not in st.session_state:
    st.session_state.last_analyzed_message = None

def analyze_mood(text):
    if not nlp:
        return "Unknown", "NLP model not loaded.", "Unknown"
    
    doc = nlp(text.lower())
    text_stripped = text.strip()
    
    question_indicators = ["?", "what", "when", "where", "why", "how", "who", "which", "can", "could", "would", "should", "is", "are", "do", "does", "did"]
    is_question = text_stripped.endswith("?") or any(text_stripped.lower().startswith(q) for q in question_indicators)
    message_type = "Asking a Question" if is_question else "Making a Statement"
    
    worried_terms = [
        "pain", "hurt", "hurts", "hurting", "ache", "aching", "sore",
        "scared", "afraid", "fear", "fearful", "terrified", "nervous",
        "worry", "worried", "anxious", "anxiety", "stress", "stressed",
        "uneasy", "restless", "concerned", "panic", "panicking",
        "bad", "worse", "worst", "problem", "issue", "trouble",
        "help", "emergency", "serious", "critical",
        "difficult", "hard", "struggling", "weak", "tired", "fatigue",
        "dizzy", "breathless", "breathing", "vomit", "nausea",
        "infection", "bleeding", "swelling", "fever"
    ]
    
    angry_terms = [
        "angry", "mad", "furious", "frustrated", "irritated", "annoyed",
        "upset", "fed up", "tired of", "sick of",
        "hate", "dislike", "can't stand", "unacceptable",
        "stupid", "ridiculous", "nonsense",
        "ugh", "damn", "hell", "crap",
        "stop", "enough", "never", "worst",
        "why would", "makes no sense",
        "wasting time", "useless", "pathetic"
    ]

    happy_terms = [
        "good", "great", "better", "best", "fine",
        "happy", "glad", "relieved", "relief",
        "improving", "improved", "recovering", "recovery",
        "thanks", "thank you", "appreciate", "grateful",
        "awesome", "excellent", "perfect",
        "feeling well", "doing well", "much better",
        "no pain", "comfortable", "stable now",
        "hopeful", "positive"
    ]

    calm_terms = [
        "okay", "ok", "alright", "fine",
        "yes", "yeah", "yep",
        "understand", "understood", "got it", "clear",
        "sure", "will do", "alright doctor",
        "peaceful", "calm", "relaxed",
        "stable", "normal", "manageable",
        "no worries", "all good",
        "noted", "makes sense"
    ]

    mood = "Neutral"
    desc = "Patient seems neutral based on response tone."
    
    worried_count = sum(1 for token in doc if token.text in worried_terms)
    angry_count = sum(1 for token in doc if token.text in angry_terms)
    happy_count = sum(1 for token in doc if token.text in happy_terms)
    calm_count = sum(1 for token in doc if token.text in calm_terms)
    
    if worried_count > angry_count and worried_count > happy_count:
        mood = "Worried"
        desc = f"Patient is {message_type.lower()} and seems anxious or in pain."
    elif angry_count > worried_count and angry_count > happy_count:
        mood = "Angry"
        desc = f"Patient is {message_type.lower()} and seems frustrated or annoyed."
    elif happy_count > 0:
        mood = "Happy"
        desc = f"Patient is {message_type.lower()} and seems positive and satisfied."
    elif calm_count > 0:
        mood = "Calm"
        desc = f"Patient is {message_type.lower()} and seems composed and understanding."
    else:
        desc = f"Patient is {message_type.lower()} with a neutral tone."
        
    return mood, desc, message_type

def get_latest_patient_message():
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "Patient":
            return msg["content"]
    return None

st.markdown("""
<div class="main-header">
    <h1>HealthChat AI</h1>
    <p>Real-Time Patient-Doctor Communication</p>
</div>
""", unsafe_allow_html=True)

latest_patient_msg = get_latest_patient_message()
if latest_patient_msg and latest_patient_msg != st.session_state.last_analyzed_message:
    mood, desc, message_type = analyze_mood(latest_patient_msg)
    st.session_state.patient_mood = {
        "mood": mood,
        "desc": desc,
        "message_type": message_type,
        "highlighted_text": latest_patient_msg
    }
    st.session_state.last_analyzed_message = latest_patient_msg

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-title">Patient</div>', unsafe_allow_html=True)
    
    chat_html = '<div class="chat-box">'
    if st.session_state.messages:
        for msg in st.session_state.messages:
            msg_class = "patient-msg" if msg["role"] == "Patient" else "doctor-msg"
            import html
            safe_content = html.escape(msg["content"])
            chat_html += f'<div class="message {msg_class}"><div class="message-header">{msg["role"]}</div><div class="message-content">{safe_content}</div></div>'
    else:
        chat_html += '<div class="empty-state">No messages yet. Start the conversation below.</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    
    with st.form("patient_form", clear_on_submit=True):
        patient_input = st.text_input(
            "Message", 
            key="p_input", 
            placeholder="Type your message to the doctor...",
            label_visibility="collapsed"
        )
        submit_p = st.form_submit_button("Send to Doctor")
        
        if submit_p and patient_input:
            st.session_state.messages.append({
                "role": "Patient", 
                "content": patient_input, 
                "timestamp": datetime.now()
            })
            
            mood, desc, message_type = analyze_mood(patient_input)
            st.session_state.patient_mood = {
                "mood": mood, 
                "desc": desc,
                "message_type": message_type,
                "highlighted_text": patient_input
            }
            st.session_state.last_analyzed_message = patient_input
            st.rerun()

with col2:
    st.markdown('<div class="section-title">Doctor</div>', unsafe_allow_html=True)
    
    mood_data = st.session_state.patient_mood
    
    message_type_display = f" • {mood_data.get('message_type', '')}" if mood_data.get('message_type') else ""
    
    st.markdown(f"""
    <div class="mood-detector">
        <div class="mood-header">AI Mood Analysis{message_type_display}</div>
        <div class="mood-status">{mood_data['mood']}</div>
        <div class="mood-description">{mood_data['desc']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if "highlighted_text" in mood_data and mood_data["highlighted_text"]:
        import html
        safe_highlighted = html.escape(mood_data['highlighted_text'])
        st.markdown(f"""
        <div class="context-box">
            <div class="context-label">Latest Patient Message</div>
            <div>"{safe_highlighted}"</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.last_doctor_msg:
            safe_doctor_msg = html.escape(st.session_state.last_doctor_msg)
            st.markdown(f"""
            <div class="context-box" style="margin-top: 0.5rem;">
                <div class="context-label">Your Last Response</div>
                <div>"{safe_doctor_msg}"</div>
            </div>
            """, unsafe_allow_html=True)
    elif not st.session_state.messages:
        st.markdown("""
        <div class="context-box">
            <div class="context-label">Status</div>
            <div>Waiting for patient to initiate conversation...</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    
    chat_html = '<div class="chat-box">'
    if st.session_state.messages:
        import html
        for msg in st.session_state.messages:
            is_highlighted = ("highlighted_text" in mood_data and 
                            msg["role"] == "Patient" and 
                            msg["content"] == mood_data["highlighted_text"])
            
            msg_class = "patient-msg" if msg["role"] == "Patient" else "doctor-msg"
            if is_highlighted:
                msg_class += " highlight-msg"
            
            safe_content = html.escape(msg["content"])
            chat_html += f'<div class="message {msg_class}"><div class="message-header">{msg["role"]}</div><div class="message-content">{safe_content}</div></div>'
    else:
        chat_html += '<div class="empty-state">Waiting for patient messages...</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    
    with st.form("doctor_form", clear_on_submit=True):
        doctor_input = st.text_input(
            "Message", 
            key="d_input", 
            placeholder="Type your response to the patient...",
            label_visibility="collapsed"
        )
        submit_d = st.form_submit_button("Send to Patient")
        
        if submit_d and doctor_input:
            st.session_state.messages.append({
                "role": "Doctor", 
                "content": doctor_input, 
                "timestamp": datetime.now()
            })
            st.session_state.last_doctor_msg = doctor_input
            st.rerun()

st.markdown("""
<div class="footer">
    <p><strong>HealthChat Intelligence System</strong></p>
    <p>NLP Powered by spaCy</p>
</div>
""", unsafe_allow_html=True)