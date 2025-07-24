# alert_page.py
import streamlit as st
import requests
from translations import translations

def show():
    mode = st.session_state.get("mode", "Light")
    language = st.session_state.get("language", "English")
    t = translations[language]

    # Back Button
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #BF1C1C;
        color: black;
        width: 36px;
        height: 36px;
        font-size: 28px !important;
        border-radius: 6px;
        border: none;
        padding: 0;
    }
    div.stButton > button:hover {
        background-color: #555555;
    }
    </style>
    """, unsafe_allow_html=True)

    # Back button in a single column
    col = st.columns(1)[0]
    with col:
        if st.button("↤", key="back_button_alerts"):
            st.session_state.page = "Home"

    st.subheader(t['alert_subheader'])

    THINGSPEAK_CHANNEL_ID = "2996157"

    def get_latest_data(field):
        url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/fields/{field}.json?results=1"
        try:
            response = requests.get(url)
            data = response.json()
            return float(data['feeds'][0][f'field{field}'])
        except:
            return "N/A"

    # Thresholds
    TEMP_THRESHOLD = 35
    MOISTURE_THRESHOLD = 20

    # Fetch data
    temperature = get_latest_data(1)
    humidity = get_latest_data(2)
    soil_moisture = get_latest_data(3)

    metric_text_color = "#ffffff" if mode == "Dark" else "#2b1d0e"

    # Inject CSS to target all text in metrics
    st.markdown(
        f"""
        <style>
        div[data-testid="stMetric"] * {{
            color: {metric_text_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    col1.metric(f"🌡️ {t['temp_metric']}", temperature)
    col2.metric(f"💧 {t['humidity_metric']}", humidity)
    col3.metric(f"🌱 {t['soil_metric']}", soil_moisture)

    # Alerts
    st.subheader(t['alerts_subheader'])

    if temperature != "N/A" and temperature > TEMP_THRESHOLD:
        st.error(t['high_temp_alert'].format(value=temperature))

    if soil_moisture != "N/A" and soil_moisture < MOISTURE_THRESHOLD:
        st.error(t['low_soil_alert'].format(value=soil_moisture))

    if (temperature != "N/A" and temperature <= TEMP_THRESHOLD) and (soil_moisture != "N/A" and soil_moisture >= MOISTURE_THRESHOLD):
        st.success(t['all_safe'])