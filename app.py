import streamlit as st
st.set_page_config(page_title="Plant Disease Predictor", layout="centered") 
import predict_page
import dashboard_page
import alert_page
from translations import translations
# Theme selection
mode = st.sidebar.radio("Choose Theme Mode", ["Light", "Dark"])
st.session_state["mode"] = mode

language = st.sidebar.radio("Select Language", ["English" , "Hindi" , "Kannada"])
st.session_state["language"] = language
t = translations[language]
def set_theme(mode):
    if mode == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #133631;
                color: white;
            }
            h1,h4, h5, h6, h7, p{
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background-color: #c2f0c7;
                color: #2b1d0e;
            }
            p, h4{
                color: #ffffff !important;
            }
            h5, h6, h7 {
                color: #2b1d0e !important;
            }
            </style>
        """, unsafe_allow_html=True)

set_theme(mode)


# Sidebar info
with st.sidebar.expander("About website"):
    st.markdown("""
    🌾 **AI-Powered Crop Disease Detection**

    Upload a clear photo of your crop leaf to get instant disease predictions using an AI model trained on real agricultural datasets.

    **Features**:
    - 📤 Image upload
    - 🤖 AI-based predictions
    - 📊 Sensor integration (coming soon)
    - ✅ Treatment suggestions

    **Built by:**  
    👩‍💻 Team TechTrio  
    🏢 Deloitte Capstone Project 2025
    """)

with st.sidebar.expander("Contact"):
    st.markdown("""
    <div style='line-height: 1.7; font-size: 15px;'>
    For queries, Contact:<br>
    <b>Sriya  Kirti Surampudi</b> — <a href="mailto:sriyakswara@gmail.com">sriyakswara@gmail.com</a><br>
    <b>Srujana C Bhandary</b> — <a href="mailto:srujana.bhandary@gmail.com">srujana.bhandary@gmail.com</a><br>
    <b>Shruti Priya</b> — <a href="mailto:shrutip0911@gmail.com">shrutip0911@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# CSS for card + button
st.markdown("""
<style>
.card {
    position: relative;
    width: 160px;
    height: 160px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    margin-bottom: 10px;
}
.card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.button-container {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
}
div.stButton > button {
    width: 60%;
    border-radius: 60;
}
</style>
""", unsafe_allow_html=True)

# HOME PAGE
if st.session_state.page == "Home":
    st.title(t["home_title"])
    st.markdown(f"<h6 style='color:#2b1d0e;'>{t['subtitle']}</h6>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <img src="https://cdn-icons-png.flaticon.com/512/17718/17718472.png" />
            <div class="button-container">
        """, unsafe_allow_html=True)
        if st.button(t["open_app_button"]):
            st.session_state.page = "App"
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <img src="https://cdn-icons-png.flaticon.com/512/12254/12254991.png" />
            <div class="button-container">
        """, unsafe_allow_html=True)
        if st.button(t["dashboard_button"]):
            st.session_state.page = "Dashboard"
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <img src="https://cdn-icons-png.flaticon.com/512/16750/16750201.png" />
            <div class="button-container">
        """, unsafe_allow_html=True)
        if st.button(t["alerts_button"]):
            st.session_state.page = "Alerts"
        st.markdown("</div></div>", unsafe_allow_html=True)

# APP PAGE
elif st.session_state.page == "App":
    mode = st.session_state.get("mode", "Light")
    predict_page.show()
    

# DASHBOARD PAGE
elif st.session_state.page == "Dashboard":
    dashboard_page.show()
    

elif st.session_state.page == "Alerts":
    alert_page.show()
   

