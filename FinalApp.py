import streamlit as st
import numpy as np
from PIL import Image
from keras.models import load_model
import pandas as p
import base64

st.set_page_config(page_title="Crop Disease Detection", layout="wide") #Page Configuration



#background leaf image with the website name
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .hero {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            padding: 6rem 2rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
        }}
        .hero h1 {{
            font-size: 3em;
            margin-bottom: 0.5rem;
        }}
        .hero p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        </style>
        <div class="hero">
            <h1>🌿 AI-Powered Crop Disease Detection</h1>
            <p>Protect your crops with AI powered disease detection. Upload a crop leaf image, view real-time sensor data, and get actionable farming tips!.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
set_background("C:/Users/User/crop_disease/bg2.jpeg")

#Light and Dark theme Feature
mode = st.sidebar.radio("Choose Theme Mode", ["Light", "Dark"])
def set_theme(mode):
    if mode == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: white;
            }
            h1,h4, h5, h6, p, {
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background-color: #F5FFFA;
                color: #F5FFFA;
            }
            h1,h4, h5, h6, p, {
                color: #F5FFFA !important;
            }
            </style>
        """, unsafe_allow_html=True)

set_theme(mode)



#side bar about section
st.sidebar.markdown("## ☰ Menu")

with st.sidebar.expander("About website"):
    st.markdown("""
    🌾 AI-Powered Crop Disease Detection

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
    For queries, Contact:  
    <b>Sriya K</b> — <a href="mailto:sriyakswara@gmail.com">sriyakswara@gmail.com</a><br>
    <b>Srujana C Bhandary</b> — <a href="mailto:srujana.bhandary@gmail.com">srujana.bhandary@gmail.com</a><br>
    <b>Shruti Priya</b> — <a href="mailto:shrutip0911@gmail.com">shrutip0911@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)


# HOW IT WORKS SECTION
st.markdown("""
<div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
<h2 style="color: #2e7d32;">How It Works?</h2>
<ul style="color: black; list-style-position: inside; text-align: left; display: inline-block;">
  <li>📷 <b>Click a clear photo</b> of your crop leaf (use your phone camera)</li>
  <li>⬆️ <b>Upload the photo</b> using the uploader below</li>
  <li>🤖 The AI model will <b>analyze the leaf</b> and predict the disease</li>
  <li>🩺 View <b>smart suggestions or IoT data</b></li>
</ul>
</div>
""", unsafe_allow_html=True)




#Dummy Crop disease detection Model
st.markdown('<div class="section-title">1️⃣ Uploading the Crop Leaf Image</div>', unsafe_allow_html=True)
# Image uploader
uploaded_file = st.file_uploader("Please upload the Leaf image here ⬇️", type=["jpg", "jpeg", "png"])

# If an image is uploaded
if uploaded_file is not None:
    from PIL import Image
    import time

    # Show preview
    image = Image.open(uploaded_file)
    st.image(image.resize((300,300)), caption="Preview of uploaded leaf", use_container_width=False)

    # Predict button
    if st.button("🔍 Predict"):
        with st.spinner("Analyzing image..."):
            time.sleep(2)  # Simulate model delay

            with st.container():
                st.markdown('<h3 style="color:#black;">📊 Prediction Result</h3>',unsafe_allow_html=True)
                st.success("Prediction: **Leaf Spot 🌿**")
                st.info("Confidence: 94.7%")
            with st.container():
                st.markdown('<h3 style="color:#black;">✅ Disease Management Tips:</h3>',unsafe_allow_html=True)
                st.markdown('<ul style="color:#black;">'
            '<li>Remove infected leaves</li>'
            '<li>Use a copper-based fungicide</li>'
            '<li>Avoid overhead watering</li>'
            '</ul>', unsafe_allow_html=True)
            st.markdown("""
                <style>
                summary {
                    color: red !important; 
                    font-weight: bold;
                    font-size: 16px;
                }
                </style>
            """, unsafe_allow_html=True)
        with st.expander("📘 Click here for more information on Leaf Spot"):
            st.markdown("""
                <div style="color: #black; font-size: 15px; line-height: 1.6;">
                <b>Leaf Spot Details</b><br>
                - Caused by bacteria or fungi.<br>
                - Symptoms: small, dark lesions that may enlarge and kill surrounding tissue.<br>
                <b>Management:</b><br>
                • Remove and destroy infected leaves.<br>
                • Apply appropriate fungicides (e.g., copper-based).<br>
                • Ensure proper air circulation and avoid water splash.
                </div>
            """, unsafe_allow_html=True)


#Footer
st.markdown("<div style='text-align: center; padding: 10px; font-size: 13px; color: gray;'> Built by <b>Team TechTrio</b> |  Deloitte Capstone Project 2025</div>", unsafe_allow_html=True)




#dictionary for the disease info
About_disease = {
   
   "Apple Scab" : {
    "About the disease" : "Apple scab is a common disease of plants in the rose family that is caused by the ascomycete fungus Venturia inaequalis.It can lead to significant damage, including defoliation, fruit drop, and reduced fruit quality. The disease is characterized by dark, scab-like lesions on leaves, fruit, and sometimes twigs.",
    "Symptoms" : "Olive-green to black velvety spots on leaves and fruits. Leaves may become distorted and drop early.",
    "Cure" : "Prune to improve airflow, remove fallen leaves, and apply fungicides during early growth stages."

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },

    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
    "" : {
    "About the disease" : "",
    "Symptoms" : "",
    "Cure" : ""

    },
}