import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import streamlit as st
from PIL import Image
from detector import detect_deepfake
import base64

# --- Load background image ---
with open("assets/background.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

st.set_page_config(page_title="DeepShield", page_icon="🛡️", layout="wide")

st.title("🛡️ DeepShield: Real-Time Deepfake Detection Agent")
st.markdown("DeepShield helps you detect and explain deepfakes in videos. Upload a video file, and our AI agent will analyze it for signs of manipulation.")

# --- Upload section ---
video_file = st.file_uploader("📤 Upload a video file", type=["mp4", "mov", "avi"])

if video_file is not None:
    with open("sample.mp4", "wb") as f:
        f.write(video_file.read())

    with st.spinner("🔍 Analyzing video... Please wait."):
        result = detect_deepfake("sample.mp4")

    score = result['score']
    label = result['label']
    stroke_dasharray = int(score * 0.72)

    with open("design.html", "r", encoding="utf-8") as f:
        html = f.read()
        html = html.replace("__PERCENTAGE__", f"{score:.2f}")
        html = html.replace("__STROKE_DASHARRAY__", str(stroke_dasharray))
        html = html.replace("__LABEL__", label)
        st.markdown(html, unsafe_allow_html=True)

    st.success(f"Result: {label} ({score:.2f}%)")
    st.markdown(f"🔍 Analyzed {result['total_frames']} frames, flagged {result['suspicious_frames']} as suspicious.")

else:
    stroke_dasharray = int(72 * 0.72)
    with open("design.html", "r", encoding="utf-8") as f:
        html = f.read()
        html = html.replace("__PERCENTAGE__", "72")
        html = html.replace("__STROKE_DASHARRAY__", str(stroke_dasharray))
        html = html.replace("__LABEL__", "Awaiting upload...")
        st.markdown(html, unsafe_allow_html=True)

# --- Background image styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Built by DHINESH and team • Agentic AI for truth and transparency")
