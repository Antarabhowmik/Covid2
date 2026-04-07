import streamlit as st
import joblib
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="COVID Probability AI", layout="wide")

# -----------------------------
# LOAD MODEL
# -----------------------------
model = joblib.load("Model.pkl")

# -----------------------------
# CUSTOM CSS (BIOPUNK MEDICAL LAB)
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --neon-cyan: #00ffe7;
    --neon-red: #ff2d55;
    --neon-amber: #ffb800;
    --bg-deep: #020b12;
    --bg-panel: rgba(0, 255, 231, 0.04);
    --border-glow: rgba(0, 255, 231, 0.2);
    --text-primary: #e0f7fa;
    --text-muted: #4a7a82;
    --font-display: 'Orbitron', monospace;
    --font-mono: 'Share Tech Mono', monospace;
    --font-body: 'Inter', sans-serif;
}

/* ── BASE RESET ── */
html, body, .stApp {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}

/* ── ANIMATED GRID BACKGROUND ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,255,231,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,231,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
    animation: gridPulse 8s ease-in-out infinite;
}

@keyframes gridPulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

/* ── SCANLINE OVERLAY ── */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.08) 2px,
        rgba(0,0,0,0.08) 4px
    );
    pointer-events: none;
    z-index: 0;
}

/* ── MAIN CONTAINER ── */
.block-container {
    max-width: 1300px !important;
    padding: 2rem 3rem !important;
    position: relative;
    z-index: 1;
}

/* ── TITLE ── */
h1 {
    font-family: var(--font-display) !important;
    font-size: 2.6rem !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, var(--neon-cyan), #007cf0, var(--neon-cyan));
    background-size: 200%;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shimmer 4s linear infinite;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.2rem !important;
    filter: drop-shadow(0 0 20px rgba(0,255,231,0.4));
}

@keyframes shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

/* ── SUBTITLE ── */
h3 {
    font-family: var(--font-mono) !important;
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-left: 3px solid var(--neon-cyan);
    padding-left: 0.75rem;
    margin-bottom: 2rem !important;
}

/* ── SECTION HEADERS (subheader) ── */
h2 {
    font-family: var(--font-display) !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--neon-cyan) !important;
    border-bottom: 1px solid var(--border-glow);
    padding-bottom: 0.6rem;
    margin-bottom: 1.4rem !important;
    position: relative;
}

h2::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 40px;
    height: 2px;
    background: var(--neon-cyan);
    box-shadow: 0 0 10px var(--neon-cyan);
}

/* ── RADIO BUTTONS ── */
div[role="radiogroup"] {
    gap: 0.5rem !important;
}

div[role="radiogroup"] label {
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
    color: var(--text-muted) !important;
    background: rgba(0,255,231,0.04) !important;
    border: 1px solid rgba(0,255,231,0.12) !important;
    border-radius: 6px !important;
    padding: 0.3rem 0.9rem !important;
    cursor: pointer;
    transition: all 0.25s ease !important;
}

div[role="radiogroup"] label:hover {
    border-color: rgba(0,255,231,0.45) !important;
    color: var(--neon-cyan) !important;
    background: rgba(0,255,231,0.08) !important;
    box-shadow: 0 0 12px rgba(0,255,231,0.15);
}

/* Selected radio */
div[role="radiogroup"] label:has(input:checked) {
    border-color: var(--neon-cyan) !important;
    color: var(--bg-deep) !important;
    background: var(--neon-cyan) !important;
    box-shadow: 0 0 20px rgba(0,255,231,0.4), inset 0 0 10px rgba(0,0,0,0.2) !important;
    font-weight: 600 !important;
}

/* Hide default radio dot */
div[role="radiogroup"] input[type="radio"] {
    display: none !important;
}

/* ── SLIDER ── */
.stSlider > div > div > div {
    background: linear-gradient(90deg, var(--neon-cyan), #007cf0) !important;
}

.stSlider [data-testid="stThumbValue"] {
    font-family: var(--font-display) !important;
    font-size: 0.8rem !important;
    color: var(--neon-cyan) !important;
}

.stSlider [data-baseweb="slider"] > div:first-child {
    background: rgba(0,255,231,0.1) !important;
}

/* ── ANALYZE BUTTON ── */
.stButton > button {
    width: 100% !important;
    margin-top: 2rem !important;
    padding: 1.1rem 2rem !important;
    font-family: var(--font-display) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--bg-deep) !important;
    background: linear-gradient(90deg, var(--neon-cyan) 0%, #007cf0 50%, var(--neon-cyan) 100%) !important;
    background-size: 200% !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow:
        0 0 20px rgba(0,255,231,0.4),
        0 0 60px rgba(0,255,231,0.15),
        inset 0 1px 0 rgba(255,255,255,0.2) !important;
    animation: btnShimmer 3s linear infinite !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 0 35px rgba(0,255,231,0.6),
        0 0 80px rgba(0,255,231,0.25),
        inset 0 1px 0 rgba(255,255,255,0.3) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

@keyframes btnShimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

/* ── METRIC (RESULT) ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0,255,231,0.06), rgba(0,124,240,0.06)) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 12px !important;
    padding: 1.5rem 2rem !important;
    position: relative;
    overflow: hidden;
    animation: resultPulse 2s ease-in-out 3;
}

[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    animation: scanLine 2s linear infinite;
}

@keyframes scanLine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

@keyframes resultPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(0,255,231,0.1); }
    50% { box-shadow: 0 0 40px rgba(0,255,231,0.35), 0 0 80px rgba(0,255,231,0.1); }
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, var(--neon-cyan), #007cf0);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    filter: drop-shadow(0 0 15px rgba(0,255,231,0.5));
}

/* ── PROGRESS BAR ── */
.stProgress > div > div {
    background: rgba(0,255,231,0.1) !important;
    border-radius: 4px !important;
    overflow: hidden;
    border: 1px solid rgba(0,255,231,0.15) !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--neon-cyan), #007cf0) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 15px rgba(0,255,231,0.5) !important;
    transition: width 1s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
}

/* ── CAPTIONS ── */
[data-testid="stCaptionContainer"] {
    font-family: var(--font-mono) !important;
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em;
}

/* ── COLUMN DIVIDERS ── */
[data-testid="column"] {
    background: var(--bg-panel) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(6px) !important;
}

/* ── ERROR ── */
.stAlert {
    font-family: var(--font-mono) !important;
    background: rgba(255,45,85,0.08) !important;
    border: 1px solid rgba(255,45,85,0.3) !important;
    border-radius: 8px !important;
    color: #ff6b8a !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb {
    background: rgba(0,255,231,0.2);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(0,255,231,0.4);
}

/* ── LABEL TEXT ── */
.stRadio > label,
.stSlider > label {
    font-family: var(--font-body) !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #8ecfd8 !important;
    letter-spacing: 0.03em;
}
</style>

<!-- HEADER DECORATION -->
<div style="
    font-family:'Share Tech Mono',monospace;
    font-size:0.7rem;
    color:rgba(0,255,231,0.35);
    letter-spacing:0.15em;
    margin-bottom:0.5rem;
">
    ◈ SYSTEM ONLINE &nbsp;│&nbsp; DIAGNOSTIC MODULE v4.1 &nbsp;│&nbsp; NEURAL ANALYSIS ENGINE
</div>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🧬 COVID Probability Predictor")
st.write("### Enter Patient Details")

# -----------------------------
# YES/NO FUNCTION
# -----------------------------
def yes_no(label):
    return 1 if st.radio(label, ["No", "Yes"], horizontal=True) == "Yes" else 0

# -----------------------------
# INPUTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🦠 Symptoms")
    fever = yes_no("Fever")
    cough = yes_no("Cough")
    fatigue = yes_no("Fatigue")
    headache = yes_no("Headache")
    loss_of_smell = yes_no("Loss of Smell")
    shortness_of_breath = yes_no("Shortness of Breath")
    difficulty_breathing = yes_no("Difficulty Breathing")

with col2:
    st.subheader("🏥 Health Conditions")
    diabetes = yes_no("Diabetes")
    heart_disease = yes_no("Heart Disease")
    hypertension = yes_no("Hypertension")
    asthma = yes_no("Asthma")
    cancer = yes_no("Cancer")
    icu_admission = yes_no("ICU Admission")
    hospitalized = yes_no("Hospitalized")

# -----------------------------
# EXTRA INFO
# -----------------------------
st.subheader("📊 Patient Info")

col3, col4 = st.columns(2)

with col3:
    age = st.slider("Age", 1, 100, 25)

with col4:
    gender_ui = st.radio("Gender", ["Male", "Female"], horizontal=True)

vacc_ui = st.radio(
    "Vaccination Status",
    ["Not Vaccinated", "Partially Vaccinated", "Fully Vaccinated"],
    horizontal=True
)

# -----------------------------
# ENCODING
# -----------------------------
gender = 1 if gender_ui == "Male" else 0

vacc_map = {
    "Not Vaccinated": 0,
    "Partially Vaccinated": 1,
    "Fully Vaccinated": 2
}
vaccination_status = vacc_map[vacc_ui]

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("🚀 Analyze Probability"):

    input_data = pd.DataFrame([{
        "fever": fever,
        "cough": cough,
        "fatigue": fatigue,
        "difficulty_breathing": difficulty_breathing,
        "loss_of_smell": loss_of_smell,
        "shortness_of_breath": shortness_of_breath,
        "icu_admission": icu_admission,
        "hospitalized": hospitalized,
        "diabetes": diabetes,
        "heart_disease": heart_disease,
        "hypertension": hypertension,
        "asthma": asthma,
        "cancer": cancer,
        "headache": headache,
        "age": age,
        "gender": gender,
        "vaccination_status": vaccination_status
    }])

    try:
        probs = model.predict_proba(input_data)[0]
        covid_prob = round(probs[1] * 100, 2)

        # -----------------------------
        # CLEAN OUTPUT
        # -----------------------------
        st.subheader("🧬 COVID Probability")

        # Big number
        st.metric(label="Estimated Risk", value=f"{covid_prob}%")

        # Progress bar
        st.progress(covid_prob / 100)

        # Extra text
        st.caption("Probability based on symptoms & health conditions")

    except Exception as e:
        st.error(f"❌ Error: {e}")