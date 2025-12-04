import streamlit as st
import pandas as pd
import plotly.express as px
from digipin_decoder import decode_digipin
from address_parser import parse_address
from ml_similarity import similarity_score
from geo_validator import distance_meters
from score_engine import compute_confidence, interpretation

# ───────────────────────────────────────────────
# PAGE CONFIG
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="AAVA Validator",
    page_icon="📍",
    layout="wide",
)

# ───────────────────────────────────────────────
# CUSTOM CSS FOR MODERN UI
# ───────────────────────────────────────────────
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0F172A, #1E293B);
}

/* Title Style */
.big-title {
    font-size: 45px !important;
    font-weight: 900 !important;
    background: linear-gradient(to right, #06b6d4, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    color: transparent;
    letter-spacing: -1px;
    padding-bottom: 10px;
}

/* Glass Card */
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

/* Better Inputs */
textarea, input {
    border-radius: 10px !important;
}

/* Score Banner */
.decision-banner {
    padding: 15px;
    font-size: 22px;
    border-radius: 12px;
    margin-top: 20px;
    color: white;
    font-weight: bold;
}

/* Expander Style */
.streamlit-expanderHeader {
    font-size: 20px !important;
    color: #06b6d4 !important;
}

</style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# HEADER
# ───────────────────────────────────────────────
st.markdown("<h1 class='big-title'>AAVA Digital Address Validation Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### 📡 DIGIPIN • 📍 Geo Validation • 🤖 ML Similarity • 🧠 NLP Parsing")

# ───────────────────────────────────────────────
# INPUT SECTION
# ───────────────────────────────────────────────
with st.container():
    colA, colB = st.columns(2)

    with colA:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🧩 Address Inputs")
        digipin = st.text_input("DIGIPIN")
        address = st.text_area("Full Address")
        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🌍 Location Inputs")
        lat = st.text_input("Latitude (optional)")
        lon = st.text_input("Longitude (optional)")
        reference = st.text_input("Reference Address (optional)")
        st.markdown("</div>", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# AAR DATA
# ───────────────────────────────────────────────
AAR = {
    'Karnataka': {'districts': ['Bengaluru', 'Mysuru'], 'pincodes': ['560001','560002','560003']},
    'Delhi': {'districts': ['New Delhi', 'South Delhi'], 'pincodes': ['110001','110002']},
    'Rajasthan': {'districts': ['Jaipur', 'Jodhpur'], 'pincodes': ['302001','302002']}
}

# VALIDATION FUNCTIONS (same as before)
# ----------------------------------------------------
def rule_checks(parsed, digipin):
    score = 0
    reasons = []
    try:
        centroid = decode_digipin(digipin)
        score += 10
    except:
        reasons.append("Invalid DIGIPIN")
        return 0, reasons, None

    # Pincode
    p = parsed.get("pincode")
    if p and any(p in info['pincodes'] for info in AAR.values()):
        score += 8
    else:
        reasons.append("Pincode mismatch or missing")

    # District
    district = parsed.get("district_guess")
    if district and any(district.lower() in [d.lower() for d in info['districts']] for info in AAR.values()):
        score += 6
    else:
        reasons.append("District mismatch or missing")

    if parsed.get("house_no"): score += 6
    if parsed.get("locality_guess"): score += 4

    return min(score, 40), reasons, centroid

def ml_checks(text, reference=None):
    sim = similarity_score(text, reference or text)
    return round(sim * 40, 2), round(sim, 3)

def geo_checks(centroid, coords):
    if centroid is None:
        return 0, None
    if coords is None:
        return 5, None
    dist = distance_meters(centroid, coords)
    if dist <= 10: return 20, dist
    if dist <= 50: return 14, dist
    if dist <= 200: return 8, dist
    if dist <= 1000: return 4, dist
    return 0, dist

def validate(digipin, address, lat, lon, reference):
    parsed = parse_address(address)
    rule_score, reasons, centroid = rule_checks(parsed, digipin)
    ml_score, sim = ml_checks(address, reference)
    geo_score, dist = geo_checks(centroid, (lat, lon) if lat and lon else None)
    conf = compute_confidence(rule_score, ml_score, geo_score)
    dec = interpretation(conf)
    return {
        "parsed": parsed,
        "rule": rule_score,
        "ml": ml_score,
        "geo": geo_score,
        "similarity": sim,
        "distance": dist,
        "confidence": conf,
        "decision": dec,
        "centroid": centroid,
        "reasons": reasons
    }

# ───────────────────────────────────────────────
# VALIDATION RESULT
# ───────────────────────────────────────────────
if st.button("🚀 Validate Address"):
    lat_val = float(lat) if lat else None
    lon_val = float(lon) if lon else None

    res = validate(digipin, address, lat_val, lon_val, reference)

    # COLOR BANNER
    color_map = {
        "Auto Approved": "#16a34a",
        "High Confidence": "#2563eb",
        "Verified": "#fbbf24",
        "Needs Attention": "#f59e0b",
        "Physical Verification Required": "#ef4444"
    }

    st.markdown(
        f"<div class='decision-banner' style='background-color:{color_map.get(res['decision'],'gray')}'>"
        f"Decision: {res['decision']}</div>",
        unsafe_allow_html=True
    )

    # SCORE RADAR
    df = pd.DataFrame({
        "Score Type": ["Rule", "ML", "Geo"],
        "Score": [res["rule"], res["ml"], res["geo"]]
    })
    radar = px.line_polar(df, r="Score", theta="Score Type", line_close=True, range_r=[0,40])
    radar.update_traces(fill='toself')
    st.plotly_chart(radar, use_container_width=True)

    # CONFIDENCE METER
    st.metric("Final Confidence", f"{res['confidence']}%")
    st.progress(res['confidence']/100)

    # MAP
    if res["centroid"]:
        map_df = pd.DataFrame({
            "type": ["DIGIPIN Centroid"],
            "lat": [res["centroid"][0]],
            "lon": [res["centroid"][1]]
        })
        st.map(map_df)

    with st.expander("🧩 Parsed Address"):
        st.json(res["parsed"])

    with st.expander("⚙ Rule Engine Details"):
        st.write(res["reasons"])

    with st.expander("🤖 ML Similarity"):
        st.write(f"Similarity: {res['similarity']}")

    with st.expander("📍 Geo Validation"):
        st.write(f"Distance: {res['distance']} meters")
