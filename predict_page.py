import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import requests
import base64
from translations import translations
from disease_info import About_disease_hi, About_disease_kn


def show():
    mode = st.session_state.get("mode", "Light")
    st.markdown("""
    <style>
    div.stButton > button {
      background-color: #3f2a14;
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
    
    # Fetch the translation dictionary for the selected language
    language = st.session_state.get("language", "English")
    t = translations[language]


  # Inside the page
    col = st.columns(1)[0]
    with col:
      if st.button("↤", key="back_button_alerts"):
          st.session_state.page = "Home"

  # Set page config
    #st.set_page_config(page_title="Plant Disease Predictor", layout="centered")

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
                <h1>{t["AI-title"]}</h1>
                <h4>{t["leaf_it"]}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
    set_background("C:/Users/sruja/OneDrive/Desktop/crop_disease/crop_disease/SoilBg2.jpg")

    #Light and Dark theme Feature
    '''mode = st.sidebar.radio("Choose Theme Mode", ["Light", "Dark"])
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
        """, unsafe_allow_html=True)'''


    st.markdown(f"""
    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
    <h2 style="color: #2e7d32;">{t['how_it_works_title']}</h2>
    <ul style="color: black; list-style-position: inside; text-align: left; display: inline-block;">
        <li>📷 <b>{t['how_it_works_1']}</b></li>
        <li>⬆️ <b>{t['how_it_works_2']}</b></li>
        <li>🤖 {t['how_it_works_3']}</li>
        <li>🩺 {t['how_it_works_4']}</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    # Constants
    IMAGE_SIZE = (128, 128)
    MODEL_PATH = "C:/Users/sruja/OneDrive/Desktop/crop_disease/crop_disease/model_ver12.keras"
    THINGSPEAK_CHANNEL_ID = "2996157"  # Replace with your ThingSpeak channel ID

    # Load model
    @st.cache_resource
    def load_keras_model():
        return load_model(MODEL_PATH)

    model = load_keras_model()

    # Class names (index to label mapping)
    class_names = {
        0: 'Apple___Apple_scab',
        1: 'Apple___Black_rot',
        2: 'Apple___Cedar_apple_rust',
        3: 'Apple___healthy',
        4: 'Blueberry___healthy',
        5: 'Cherry_(including_sour)___Powdery_mildew',
        6: 'Cherry_(including_sour)___healthy',
        7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        8: 'Corn_(maize)___Common_rust_',
        9: 'Corn_(maize)___Northern_Leaf_Blight',
        10: 'Corn_(maize)___healthy',
        11: 'Grape___Black_rot',
        12: 'Grape___Esca_(Black_Measles)',
        13: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        14: 'Grape___healthy',
        15: 'Orange___Haunglongbing_(Citrus_greening)',
        16: 'Peach___Bacterial_spot',
        17: 'Peach___healthy',
        18: 'Pepper,_bell___Bacterial_spot',
        19: 'Pepper,_bell___healthy',
        20: 'Potato___Early_blight',
        21: 'Potato___Late_blight',
        22: 'Potato___healthy',
        23: 'Raspberry___healthy',
        24: 'Soybean___healthy',
        25: 'Squash___Powdery_mildew',
        26: 'Strawberry___Leaf_scorch',
        27: 'Strawberry___healthy',
        28: 'Tomato___Bacterial_spot',
        29: 'Tomato___Early_blight',
        30: 'Tomato___Late_blight',
        31: 'Tomato___Leaf_Mold',
        32: 'Tomato___Septoria_leaf_spot',
        33: 'Tomato___Spider_mites Two-spotted_spider_mite',
        34: 'Tomato___Target_Spot',
        35: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        36: 'Tomato___Tomato_mosaic_virus',
        37: 'Tomato___healthy'
    }

    # Crop conditions dictionary
    CROP_CONDITIONS = {
        "Corn Northern Leaf Blight": {"Temperature (°C)": "20–28", "Humidity (%)": "90–100", "Soil Moisture (%)": "60–80"},
        "Corn Common rust": {"Temperature (°C)": "18–25", "Humidity (%)": "95–100", "Soil Moisture (%)": "50–70"},
        "Corn Cercospora leaf spot Gray leaf spot": {"Temperature (°C)": "25–30", "Humidity (%)": "85–95", "Soil Moisture (%)": "60–80"},
        "Corn healthy": {"Temperature (°C)": "21–30", "Humidity (%)": "50–70", "Soil Moisture (%)": "40–60"},
        "Apple Apple scab": {"Temperature (°C)": "18–24", "Humidity (%)": "75–90", "Soil Moisture (%)": "60–80"},
        "Apple Black rot": {"Temperature (°C)": "24–30", "Humidity (%)": "70–85", "Soil Moisture (%)": "50–70"},
        "Apple Cedar apple rust": {"Temperature (°C)": "10–24", "Humidity (%)": "85–100", "Soil Moisture (%)": "60–80"},
        "Apple healthy": {"Temperature (°C)": "15–24", "Humidity (%)": "60–75", "Soil Moisture (%)": "40–60"},
        "Tomato Early blight": {"Temperature (°C)": "22–28", "Humidity (%)": "80–90", "Soil Moisture (%)": "50–70"},
        "Tomato Late blight": {"Temperature (°C)": "15–22", "Humidity (%)": "90–100", "Soil Moisture (%)": "60–80"},
        "Tomato healthy": {"Temperature (°C)": "18–27", "Humidity (%)": "50–70", "Soil Moisture (%)": "40–60"},
        "Orange Haunglongbing (Citrus greening)": {"Temperature (°C)": " 25–30", "Humidity (%)": "60–80%", "Soil Moisture (%)": "60–80"},
        "Grape Black rot": {"Temperature (°C)": "15–35", "Humidity (%)": "60–85%", "Soil Moisture (%)": "60–80"}


        # Add more entries as needed...
    }
    #dictionary for the disease info
    About_disease = {
        
        "Apple Apple scab" : {
        "About the disease" : "Apple scab is a common disease of plants in the rose family that is caused by the ascomycete fungus Venturia inaequalis.It can lead to significant damage, including defoliation, fruit drop, and reduced fruit quality. The disease is characterized by dark, scab-like lesions on leaves, fruit, and sometimes twigs.",
        "Symptoms" : "Olive-green to black velvety spots on leaves and fruits. Leaves may become distorted and drop early.",
        "Cure" : "Prune to improve airflow, remove fallen leaves, and apply fungicides during early growth stages."

        },
        "Apple Black rot": {
            "About the disease": "Black rot is a fungal disease affecting apple trees, causing fruit rot, leaf spots, and cankers.",
            "Symptoms": "Circular brown or black spots on fruit, purple-bordered leaf lesions, sunken cankers on branches.",
            "Cure": "Prune infected limbs, remove mummified fruits, apply fungicides during bloom and early fruit development."
        },
        "Apple Cedar apple rust": {
            "About the disease": "A fungal disease requiring both apple and cedar hosts to complete its lifecycle.",
            "Symptoms": "Yellow-orange leaf spots on apple, galls on cedar trees.",
            "Cure": "Remove nearby cedar trees if possible, apply fungicides in early spring, use resistant apple varieties."
        },
        "Cherry (including sour) Powdery mildew": {
            "About the disease": "Powdery mildew is a fungal infection affecting cherry leaves, shoots, and fruits.",
            "Symptoms": "White powdery fungal growth on leaves and shoots, leaf curling and distortion.",
            "Cure": "Improve air circulation by pruning, avoid excessive nitrogen, apply sulfur or other fungicides."
        },
        "Corn (maize) Cercospora Gray leaf spot": {
            "About the disease": "A serious foliar disease of maize caused by the fungus Cercospora zeae-maydis.",
            "Symptoms": "Long rectangular gray lesions parallel to leaf veins, reduced photosynthesis.",
            "Cure": "Rotate crops, plant resistant hybrids, apply foliar fungicides at disease onset."
        },
        "Corn (maize) Common rust": {
            "About the disease": "Common rust is a fungal disease caused by Puccinia sorghi affecting maize leaves.",
            "Symptoms": "Small reddish-brown pustules on both leaf surfaces.",
            "Cure": "Use resistant hybrids, apply fungicides if rust is severe."
        },
        "Corn (maize) Northern Leaf Blight": {
            "About the disease": "A destructive maize disease caused by Exserohilum turcicum fungus.",
            "Symptoms": "Long tan 'cigar-shaped' lesions on leaves, rapid leaf death under humid conditions.",
            "Cure": "Plant resistant hybrids, rotate crops, apply fungicides if disease pressure is high."
        },
        "Grape Black rot": {
            "About the disease": "Black rot is a common grapevine disease caused by the fungus Guignardia bidwellii.",
            "Symptoms": "Circular tan spots on leaves with dark margins, black shriveled mummified berries.",
            "Cure": "Remove infected plant debris, prune for airflow, apply protective fungicides early in the season."
        },
        "Grape Esca (Black Measles)": {
            "About the disease": "Esca is a complex fungal disease causing internal wood decay and leaf symptoms in grapevines.",
            "Symptoms": "Interveinal chlorosis with 'tiger stripe' leaf pattern, sudden vine collapse in hot weather.",
            "Cure": "Prune infected wood, avoid wounds during pruning, no effective chemical treatment currently available."
        },
        "Grape Leaf blight (Isariopsis Leaf Spot)": {
            "About the disease": "A fungal leaf spot disease affecting grape foliage.",
            "Symptoms": "Angular brown spots with yellow halos, premature leaf drop.",
            "Cure": "Improve ventilation, remove infected leaves, apply fungicides during early growth."
        },
        "Orange Haunglongbing (Citrus greening)": {
            "About the disease": "A devastating bacterial disease spread by Asian citrus psyllid insects.",
            "Symptoms": "Yellow shoots, blotchy mottled leaves, misshapen bitter fruits, tree decline.",
            "Cure": "Remove infected trees to reduce spread, control psyllid populations with insecticides, plant certified disease-free nursery stock."
        },
        "Peach Bacterial Spot": {
        "About the disease": "Bacterial spot of peach is caused by the bacterium Xanthomonas campestris pv. pruni. It affects leaves, twigs, and fruit, leading to economic losses due to blemished or cracked fruits and defoliation.",
        "Symptoms": "Small, dark, water-soaked lesions on leaves that become angular and eventually fall out. Fruit may have dark, sunken spots that crack.",
        "Cure": "Use resistant varieties, avoid overhead irrigation, apply copper-based bactericides during early development stages."
        },
        "Pepper Bell Bacterial Spot": {
        "About the disease": "Caused by Xanthomonas campestris pv. vesicatoria, this bacterial disease affects bell peppers and other pepper varieties, causing leaf loss and unmarketable fruits.",
        "Symptoms": "Small, water-soaked, dark spots on leaves and fruits; leaf drop and fruit lesions that are scabby and sunken.",
        "Cure": "Plant resistant varieties, rotate crops, and apply copper-based sprays during early growth."
        },
        "Potato Early Blight": {
        "About the disease": "A fungal disease caused by Alternaria, it mainly hits older leaves but can also affect stems and tubers.",
        "Symptoms": "Dark, concentric-ring spots on older leaves, often surrounded by yellow halos. Leaves may wither and die prematurely.",
        "Cure": "Use resistant varieties, rotate crops, remove infected debris, and apply appropriate fungicides."
        },
        "Potato Late blight": {
        "About the disease": "Caused by the oomycete Phytophthora infestans, late blight is one of the most devastating potato diseases and was responsible for the Irish Potato Famine.",
        "Symptoms": "Wet, brownish-black lesions on leaves and tubers. White mold might show up underneath in humid weather.",
        "Cure": "Use certified disease-free seed, apply protective fungicides, and destroy infected plant material."
        },
        "Squash Powdery Mildew": {
        "About the disease": "Powdery mildew is a fungal disease that affects squash and other cucurbits, typically in warm, dry conditions.",
        "Symptoms": "White, powdery fungal growth on upper leaf surfaces, stems, and sometimes fruits. Leaves may yellow and die.",
        "Cure": "Improve air circulation, avoid overhead watering, and apply sulfur or other fungicides early."
        },
        "Strawberry Leaf Scorch": {
        "About the disease": "Caused by the fungus Diplocarpon earlianum, this disease affects strawberry plants, primarily attacking the leaves.",
        "Symptoms": "Irregular brown spots on leaves, often with purple margins. Severe cases cause leaf death and reduced fruit production.",
        "Cure": "Remove infected leaves, improve air circulation, and use fungicides during wet, warm weather."
        },
        "Tomato Bacterial spot": {
        "About the disease": "A bacterial disease caused by Xanthomonas species that affects tomatoes and peppers, leading to yield losses and poor fruit quality.",
        "Symptoms": "Small, water-soaked spots on leaves, stems, and fruits that darken and may crack.",
        "Cure": "Use certified disease-free seeds, rotate crops, and apply copper-based sprays."
        },
        "Tomato Early Blight": {
        "About the disease": "Early blight of tomato is caused by Alternaria solani. It commonly affects older leaves and can reduce yield if not controlled.",
        "Symptoms": "Dark brown spots with concentric rings on lower leaves; leaf yellowing and drop.",
        "Cure": "Use resistant varieties, crop rotation, mulching, and timely fungicide applications."
        },
        "Tomato Late blight": {
        "About the disease": "Caused by Phytophthora infestans, late blight is a fast-spreading, devastating disease of tomatoes and potatoes.",
        "Symptoms": "Brown to black lesions on leaves, stems, and fruits; lesions may have white fungal growth in humid conditions.",
        "Cure": "Use resistant varieties, remove infected debris, and apply systemic fungicides."
        },
        "Tomato Leaf Mold": {
        "About the disease": "Leaf mold is caused by the fungus Passalora fulva, especially in humid, poorly ventilated environments.",
        "Symptoms": "Yellow spots on upper leaf surfaces with olive-green or gray mold on the underside.",
        "Cure": "Ensure proper ventilation, avoid overhead watering, and apply fungicides."
        },
        "Tomato Septoria Leaf spot": {
        "About the disease": "Septoria leaf spot is caused by Septoria lycopersici and primarily affects tomato foliage, leading to reduced yield and vigor.",
        "Symptoms": "Small, circular spots with dark borders and light centers on lower leaves; leaves may yellow and fall.",
        "Cure": "Remove affected leaves, avoid overhead irrigation, and use fungicides early."
        },
        "Tomato spider mites two spotted spider mite": {
        "About the disease": "Two-spotted spider mites (Tetranychus urticae) are pests rather than a disease, but they cause damage by feeding on plant sap, leading to stippling and bronzing of leaves.",
        "Symptoms": "Tiny yellow or white spots on leaves, webbing on undersides, and leaf bronzing or drying.",
        "Cure": "Use miticides, release natural predators (like ladybugs), and regularly spray with water to reduce mite populations."
        },
        "Tomato Target spot": {
        "About the disease": "Target spot is caused by the fungus Corynespora cassiicola and affects leaves, stems, and fruit of tomatoes.",
        "Symptoms": "Dark brown lesions with concentric rings (target-like appearance) on leaves; leaf drop and fruit lesions may occur.",
        "Cure": "Practice crop rotation, improve air circulation, and apply fungicides as needed."
        },
        "Tomato Mosaic virus": {
        "About the disease": "Tomato mosaic virus (ToMV) is a highly infectious virus that affects tomato and other Solanaceae family members, leading to stunted growth and reduced yield.",
        "Symptoms": "Mottled, light and dark green mosaic pattern on leaves, leaf distortion, and reduced fruit size.",
        "Cure": "Remove infected plants, disinfect tools, and use resistant varieties."
        },
        "Tomato Yellow leaf Curl Virus": {
        "About the disease": "Tomato yellow leaf curl virus (TYLCV) is transmitted by whiteflies and affects tomato plants, causing serious yield losses.",
        "Symptoms": "Upward curling of leaves, yellowing, stunted growth, and reduced fruit set.",
        "Cure": "Control whitefly populations, remove infected plants, and use resistant cultivars."
        }

    }
    # Image preprocessing
    def preprocess_image(uploaded_image):
        img = Image.open(uploaded_image)
        img = img.convert("RGB")
        img = img.resize(IMAGE_SIZE)
        img_array = image.img_to_array(img)
        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
        return np.expand_dims(img_array, axis=0)

    # Model prediction
    def predict(img_array):
        preds = model.predict(img_array)
        class_index = np.argmax(preds[0])
        confidence = preds[0][class_index]
        return class_names[class_index], confidence

    # Fetch live sensor data from ThingSpeak
    def get_latest_data(field):
        url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/fields/{field}.json?results=1"
        try:
            response = requests.get(url)
            data = response.json()
            return float(data['feeds'][0][f'field{field}'])
        except:
            return "N/A"

    # Get healthy ranges for the disease
    def get_healthy_ranges(label):
        label_cleaned = label.replace("___", " ").replace("_", " ").strip()
        # Remove known substrings
        for s in ["(maize)", "(including sour)", "(Two-spotted)", "(Black Measles)", "(Isariopsis Leaf Spot)"]:
            label_cleaned = label_cleaned.replace(s, "")
        label_cleaned = " ".join(label_cleaned.split())  # Remove extra spaces
        return CROP_CONDITIONS.get(label_cleaned)

    # Get disease information
    def get_disease_info(label):
        language = st.session_state.get("language", "English")
        if language == "Hindi":
            disease_info_dict = About_disease_hi
        elif language == "Kannada":
            disease_info_dict = About_disease_kn
        else:
            disease_info_dict = About_disease

        label_cleaned = label.replace("___", " ").replace("_", " ").strip()
        label_cleaned = " ".join(label_cleaned.split())
        st.write(f"DEBUG Cleaned Label: {label_cleaned}")
        return disease_info_dict.get(label_cleaned)

    # ---- Streamlit UI ----
    st.title(f"🌿 {t['page_title']}")
    st.markdown(f"<h6 style='color:#2b1d0e;'>{t['subtitle']}</h6>", unsafe_allow_html=True)

    
    uploaded_image = st.file_uploader(t['uploader'], type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
        img_array = preprocess_image(uploaded_image)

        with st.spinner(t['predicting']):
            label, confidence = predict(img_array)

        st.markdown(
         f'<p style="background-color:#4bb873;color:white;padding:10px;border-radius:5px;">🩺 {t["prediction"]}: <b>{label}</b></p>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<p style="background-color:#42acc9;color:white;padding:10px;border-radius:5px;">🔍 {t["confidence"]}: {confidence * 100:.2f}%</p>',
            unsafe_allow_html=True
        )


        import os
        import pandas as pd
        from datetime import datetime
        save_path = "C:/Users/sruja/OneDrive/Desktop/crop_disease/crop_disease/predictions.csv"
        new_data = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Prediction": label,
            "Confidence (%)": round(confidence * 100, 2)
        }])
        if os.path.exists(save_path):
            new_data.to_csv(save_path, mode="a", header=False, index=False)
        else:
            new_data.to_csv(save_path, index=False)

        # Determine theme mode
        
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
        # Fetch and display live sensor values
        st.subheader(f"📡 {t['live_sensor']}")
        temperature = get_latest_data(1)
        humidity = get_latest_data(2)
        soil_moisture = get_latest_data(3)

        col1, col2, col3 = st.columns(3)
        col1.metric(f"🌡️ {t['temp_metric']}", temperature)
        col2.metric(f"💧 {t['humidity_metric']}", humidity)
        col3.metric(f"🌱 {t['soil_metric']}", soil_moisture)

        
        

        # Fetch healthy ranges for the predicted disease
        healthy_ranges = get_healthy_ranges(label)

        if healthy_ranges:
            st.subheader(f"🌱 {t['healthy_conditions']}")
            col4, col5, col6 = st.columns(3)
            col4.metric(f"🌡️ {t['temp_range']}", healthy_ranges["Temperature (°C)"])
            col5.metric(f"💧 {t['humidity_range']}", healthy_ranges["Humidity (%)"])
            col6.metric(f"🌱 {t['soil_range']}", healthy_ranges["Soil Moisture (%)"])
        

        
        # Disease information
        info = get_disease_info(label)
        if info:
            st.subheader(f"🩺 {t['disease_info']}")

            # Set text color based on mode
            text_color = "#ffffff" 
            background_color = "#08573a" 
            # Style the container for better visibility
            st.markdown(
                f"""
                <div style="
                    color: {text_color};
                    background-color: {background_color};
                    padding: 16px;
                    border-radius: 8px;
                    font-size: 16px;
                    ">
                    <p><strong>{t['about_disease']}:</strong> {info['About the disease']}</p>
                    <p><strong>{t['symptoms']}:</strong> {info['Symptoms']}</p>
                    <p><strong>{t['cure']}:</strong> {info['Cure']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
                    


