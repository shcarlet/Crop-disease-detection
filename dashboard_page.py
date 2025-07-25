import streamlit as st
import pandas as pd
import os
from translations import translations

def show():
    language = st.session_state.get("language", "English")
    t = translations[language]

    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #007bff;
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

    # Inside the page
    col = st.columns(1)[0]
    with col:
        if st.button("↤", key="back_button_alerts"):
            st.session_state.page = "Home"

    st.title(f"📊 {t['dashboard_title']}")

  # Check if the CSV exists
    if os.path.exists("predictions.csv"):
      df = pd.read_csv("predictions.csv")

      st.markdown(f"<h6 style='color:#2b1d0e;'>{t['dashboard_subtitle']}</h6>", unsafe_allow_html=True)

      st.dataframe(df.iloc[::-1].reset_index(drop=True), use_container_width=True)


    

      # Most common predictions
    

      # Confidence over time
    
      # Option to clear history
      if st.button("🗑️"):
          os.remove("predictions.csv")
          st.success(t['clear_history_success'])
    else:
      st.warning(t['no_predictions_warning'])
