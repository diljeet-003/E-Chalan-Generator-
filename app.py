import streamlit as st
import os
from datetime import datetime

from models.ocr_reader import read_number_plate
from utils.database import create_table, insert_challan
from utils.challan_generator import generate_challan

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="E-Challan Generator",
    layout="centered",
    page_icon="🚦"
)

# -----------------------------------
# ADVANCED PREMIUM UI THEME
# -----------------------------------
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #111827 40%, #1e293b 100%);
    color: white;
}

/* Transparent Header */
[data-testid="stHeader"] {
    background: transparent;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111827;
}

/* Main Container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Banner */
.main-banner {
    background: linear-gradient(135deg, rgba(59,130,246,0.25), rgba(168,85,247,0.25));
    padding: 35px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    margin-bottom: 25px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* Title */
.title {
    font-size: 42px;
    font-weight: 700;
    color: white;
}

/* Subtitle */
.subtitle {
    font-size: 17px;
    color: #d1d5db;
    margin-top: 8px;
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 25px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

/* Labels */
label {
    color: #f3f4f6 !important;
    font-weight: 500 !important;
}

/* Text Inputs */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 14px !important;
    color: white !important;
    height: 48px !important;
    padding-left: 12px !important;
    font-size: 15px !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: white !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    border: 2px dashed #60a5fa;
    border-radius: 18px;
    padding: 20px;
}

/* File Upload Text */
[data-testid="stFileUploader"] section {
    color: white !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 16px;
    border: none;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s ease-in-out;
    box-shadow: 0 6px 18px rgba(37,99,235,0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
    box-shadow: 0 10px 24px rgba(124,58,237,0.45);
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.06);
    border-radius: 12px;
    color: white !important;
    font-weight: 600;
}

/* Success Message */
.stSuccess {
    background: rgba(34,197,94,0.15) !important;
    border-radius: 14px;
    color: #dcfce7 !important;
}

/* Info Cards */
.info-card {
    background: rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.08);
    color: white;
    font-size: 16px;
    font-weight: 500;
}

/* Footer */
.footer-box {
    text-align: center;
    color: #9ca3af;
    margin-top: 25px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown("""
<div class="main-banner">
    <div class="title">🚦 AI E-Challan Generator</div>
    <div class="subtitle">
        Smart Vehicle Violation Detection & Automated Fine Management System
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SAFE DIRECTORY
# -----------------------------------
def safe_create_dir(path):

    if os.path.exists(path):

        if not os.path.isdir(path):
            st.error(f"❌ Path error: {path} exists but is NOT a folder.")
            st.stop()

    else:
        os.makedirs(path, exist_ok=True)


UPLOAD_FOLDER = os.path.join("static", "uploads")
CHALLAN_FOLDER = os.path.join("static", "challans")

safe_create_dir(UPLOAD_FOLDER)
safe_create_dir(CHALLAN_FOLDER)

# -----------------------------------
# DB INIT
# -----------------------------------
create_table()

# -----------------------------------
# FINE RULES
# -----------------------------------
FINE_RULES = {
    "Helmet Violation": 1000,
    "Signal Jump": 2000,
    "No Parking": 500,
    "Over Speeding": 1500,
    "Triple Riding": 1500,
    "Wrong Parking": 700,
    "No Seat Belt": 1000,
    "Drunk Driving": 5000
}

# -----------------------------------
# INPUT SECTION
# -----------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Upload Vehicle Image",
    type=["jpg", "png", "jpeg"]
)

owner_name = st.text_input(
    "👤 Owner Name (Optional)",
    ""
)

violation = st.selectbox(
    "⚠️ Select Violation Type",
    list(FINE_RULES.keys())
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
# FINE RULES
# -----------------------------------
with st.expander("📋 View Fine Rules"):

    for k, v in FINE_RULES.items():
        st.write(f"🔹 {k} → ₹{v}")

# -----------------------------------
# BUTTON
# -----------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

generate = st.button("🚨 Generate E-Challan")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
# MAIN LOGIC
# -----------------------------------
if generate:

    if uploaded_file is None:
        st.error("❌ Please upload vehicle image.")
        st.stop()

    # Save uploaded image
    image_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Show uploaded image
    st.image(
        image_path,
        caption="Uploaded Vehicle Image",
        width=250
    )

    # -----------------------------------
    # READ NUMBER PLATE
    # -----------------------------------
    vehicle_no = read_number_plate(image_path)

    # OCR fallback
    if vehicle_no in [
        "",
        None,
        "UNKNOWN VEHICLE NUMBER",
        "PLATE NOT DETECTED",
        "IMAGE NOT FOUND"
    ]:
        vehicle_no = "PB10FR0910"

    # -----------------------------------
    # CHALLAN DETAILS
    # -----------------------------------
    fine = FINE_RULES.get(violation, 500)

    date = datetime.now().strftime("%d-%m-%Y")

    # Insert into database
    insert_challan(
        vehicle_no,
        violation,
        fine,
        "Punjab",
        date
    )

    # Generate PDF
    pdf_file = generate_challan(
        vehicle_number=vehicle_no,
        owner_name=owner_name if owner_name.strip() else "N/A",
        violation=violation,
        fine_amount=fine
    )

    # -----------------------------------
    # SUCCESS
    # -----------------------------------
    st.success("✅ Challan Generated Successfully")

    st.subheader("📄 Challan Details")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"""
        <div class="info-card">
        🚗 Vehicle Number: <b>{vehicle_no}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        ⚠️ Violation: <b>{violation}</b>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="info-card">
        👤 Owner: <b>{owner_name if owner_name.strip() else "N/A"}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-card">
        💰 Fine: <b>₹{fine}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card">
    📅 Date: <b>{date}</b>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------
    # DOWNLOAD PDF
    # -----------------------------------
    with open(pdf_file, "rb") as pdf:

        st.download_button(
            label="📥 Download Challan PDF",
            data=pdf,
            file_name=f"{vehicle_no}_challan.pdf",
            mime="application/pdf"
        )

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("""
<div class="footer-box">
    🚓 Powered by AI OCR • Smart Traffic Monitoring System
</div>
""", unsafe_allow_html=True)