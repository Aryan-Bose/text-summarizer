import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import time
import tiktoken

# ---------------- LOAD ENV ----------------

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- CONFIG ----------------

DAILY_LIMIT = 20
COOLDOWN = 5

# ---------------- SESSION STATE ----------------

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

if "requests_today" not in st.session_state:
    st.session_state.requests_today = 0

if "tokens_used" not in st.session_state:
    st.session_state.tokens_used = 0

# ---------------- TOKEN COUNTER ----------------

def estimate_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Notes Generator | Free Study Notes Maker",
    page_icon="📘",
    layout="centered"
)

# ---------------- UI STYLE ----------------

st.markdown("""
<style>

.main {background-color:#0f172a;}

h1,h2,h3 {color:#38bdf8;}

.hero {
background: linear-gradient(135deg,#020617,#0f172a);
padding:30px;
border-radius:18px;
text-align:center;
}

.card {
background:#1e293b;
padding:20px;
border-radius:16px;
margin-top:15px;
}

.badge {
background:#38bdf8;
color:black;
padding:6px 12px;
border-radius:12px;
font-size:14px;
margin:5px;
display:inline-block;
}

.stButton>button {
background:#38bdf8;
color:black;
font-weight:bold;
border-radius:12px;
padding:10px 22px;
}

textarea {
border-radius:12px !important;
}

.swipe-container {
display:flex;
overflow-x:auto;
gap:15px;
scroll-snap-type:x mandatory;
}

.swipe-card {
min-width:260px;
background:#1e293b;
padding:15px;
border-radius:14px;
scroll-snap-align:start;
text-align:center;
}

.footer {
text-align:center;
color:gray;
margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------

st.markdown("""
<div class="hero">
<h1>📘 AI Notes Generator For Students</h1>
<p>Convert Text & PDFs into Smart Exam-Ready Notes Instantly</p>

<span class="badge">Free AI Tool</span>
<span class="badge">PDF Export</span>
<span class="badge">Exam Focused</span>
<span class="badge">Mobile Friendly</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- FEATURE SWIPE ----------------

st.markdown("""
<div class="swipe-container">

<div class="swipe-card">
<h3>✍ Text Input</h3>
<p>Paste articles or notes</p>
</div>

<div class="swipe-card">
<h3>📂 PDF Upload</h3>
<p>Summarize study material</p>
</div>

<div class="swipe-card">
<h3>🎯 Exam Notes</h3>
<p>Bullet & revision format</p>
</div>

<div class="swipe-card">
<h3>⬇ PDF Export</h3>
<p>Download clean notes</p>
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- INPUT TABS ----------------

tab1, tab2 = st.tabs(["✍ Text Input", "📂 Upload File"])

final_text = ""

with tab1:
    text_input = st.text_area("Paste your content:", height=220)
    st.caption(f"Word Count: {len(text_input.split())}")
    final_text = text_input

with tab2:
    file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

    if file:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            final_text = text
        else:
            final_text = file.read().decode("utf-8")

        st.success("File loaded successfully")
        st.caption(f"Word Count: {len(final_text.split())}")

# ---------------- SETTINGS ----------------

st.subheader("⚙ Notes Settings")

col1, col2 = st.columns(2)

with col1:
    summary_style = st.selectbox(
        "Summary Style",
        ["Quick Revision", "Detailed Notes", "Exam Bullet Points"]
    )

with col2:
    level = st.selectbox(
        "Student Level",
        ["School", "College", "Professional"]
    )

# ---------------- GENERATE ----------------

generate = st.button("🚀 Generate Smart Notes")

if generate:

    # Daily quota
    if st.session_state.requests_today >= DAILY_LIMIT:
        st.error("🚫 Daily usage limit reached (20 requests). Try tomorrow.")
        st.stop()

    # Cooldown
    now = time.time()
    if now - st.session_state.last_request_time < COOLDOWN:
        st.warning("⏳ Please wait a few seconds before next request.")
        st.stop()

    st.session_state.last_request_time = now

    # Empty input check
    if final_text.strip() == "":
        st.warning("Please add text or upload file")
        st.stop()

    style_map = {
        "Quick Revision": "Short revision notes in simple bullet points.",
        "Detailed Notes": "Detailed structured notes with headings.",
        "Exam Bullet Points": "Exam-focused bullet point notes with key facts."
    }

    level_map = {
        "School": "Use simple easy language.",
        "College": "Use academic explanation.",
        "Professional": "Use professional concise tone."
    }

    prompt = f"""
    {style_map[summary_style]}
    {level_map[level]}

    Format output with:
    - Headings
    - Bullet points
    - Important keywords highlighted

    Content:
    {final_text}
    """

    input_tokens = estimate_tokens(prompt)

    with st.spinner("Generating AI Notes..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an expert academic notes generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            summary = response.choices[0].message.content

        except Exception:
            st.error("🚨 AI server busy or rate limited. Try later.")
            st.stop()

    output_tokens = estimate_tokens(summary)

    st.session_state.tokens_used += input_tokens + output_tokens
    st.session_state.requests_today += 1

    # ---------------- SAVE HISTORY ----------------

    os.makedirs("data", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("data/history.txt", "a", encoding="utf-8") as f:
        f.write("\n\n" + timestamp + "\n" + summary)

    # ---------------- DISPLAY RESULT ----------------

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("✅ Generated Notes")

    st.code(summary, language="markdown")

    # ---------------- PDF EXPORT ----------------

    os.makedirs("downloads", exist_ok=True)

    pdf_path = "downloads/AI_Notes.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_path)

    story = [Paragraph(line, styles["BodyText"]) for line in summary.split("\n")]

    doc.build(story)

    with open(pdf_path, "rb") as f:
        st.download_button("⬇ Download Notes PDF", f, file_name="AI_Notes.pdf")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- USAGE DASHBOARD ----------------

st.markdown("---")
st.subheader("📊 Usage Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("Requests Today", st.session_state.requests_today, f"/ {DAILY_LIMIT}")
c2.metric("Tokens Used", st.session_state.tokens_used)
c3.metric("Cooldown", f"{COOLDOWN}s")

# ---------------- HISTORY ----------------

st.markdown("---")
st.subheader("📚 Notes History")

if os.path.exists("data/history.txt"):
    with open("data/history.txt", "r", encoding="utf-8") as f:
        history = f.read()

    st.text_area("Saved Notes", history, height=220)
else:
    st.info("No saved notes yet")

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
⚡ Powered by Groq AI | Built by You 🚀 <br>
AI Notes Generator Platform
</div>
""", unsafe_allow_html=True)
