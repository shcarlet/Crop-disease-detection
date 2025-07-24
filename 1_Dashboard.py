import streamlit as st
import pandas as pd
import os

st.title("📊 Prediction Dashboard")

# Check if the CSV exists
if os.path.exists("C:/Users/User/crop_disease/predictions.csv"):
    df = pd.read_csv("C:/Users/User/crop_disease/predictions.csv")

    st.write("Here are your past predictions:")

    st.dataframe(df.iloc[::-1].reset_index(drop=True), use_container_width=True)


   

    # Most common predictions
   

    # Confidence over time
   
    # Option to clear history
    if st.button("🗑️ Clear All Records"):
        os.remove("C:/Users/User/crop_disease/predictions.csv")
        st.success("All records have been deleted. Please refresh.")
else:
    st.warning("⚠️ No predictions recorded yet. Run a prediction in the Home page.")
