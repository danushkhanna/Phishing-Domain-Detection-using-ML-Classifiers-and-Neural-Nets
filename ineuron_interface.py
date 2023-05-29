import streamlit as st
import pickle
import pandas as pd
from extract_features import ExtractFeatures

# Load the image
image = image.open('ineuron-logo1.png')
st.image(image, width=150)

st.write("<div align='left'><span style='color:#FF5A5F; font-size: 15px;'>Amsterdam</span></div>", unsafe_allow_html=True)

st.markdown(
    "<div style='display: flex; align-items: left;'>"
    "<h1 style='color:#484848; margin-right: -40px'>Visualization with</h1>"
    "<h1 style='color:#FF5A5F;'>NumPy 🗺️</h1>"
    "</div>", 
    unsafe_allow_html=True
)

image=image.open('cybersec_orange.png')
width=750
height=500
image_new=image.resize((width,height))
st.image(image_new)

@st.cache_resource
def get_model():
    """
    Loads the phishing URL detection model from a pickle file.

    This function reads and loads a pickled file containing the classifier.

    Returns:
        object: The loaded phishing URL detection model.

    Note:
        The model should be saved in a file named 'phishing_url_detector.pkl'.
        XGBoost module must be installed before using the file.
    """
    with open('phishing_url_detector.pkl', 'rb') as pickle_model:
        phishing_url_detector = pickle.load(pickle_model)
    return phishing_url_detector

st.title("Phishing Website Detector")
st.header("Are you sure your 'bank' sent that link?")

# Takes in user input
input_url = st.text_area("Put in your sus site link here: ")

if input_url != "":
    
    # Extracts features from the URL and converts it into a dataframe
    features_url = ExtractFeatures().url_to_features(url=input_url)
    features_dataframe = pd.DataFrame.from_dict([features_url])
    features_dataframe = features_dataframe.fillna(-1)
    features_dataframe = features_dataframe.astype(int)

    st.write("Okay!")
    st.cache_data.clear()
    prediction_str = ""

    # Predict outcome using extracted features
    try: 
        phishing_url_detector = get_model()
        prediction = phishing_url_detector.predict(features_dataframe)
        if prediction == int(True):
            prediction_str = 'Phishing Website. Do not click!'
        elif prediction == int(False):
            prediction_str = 'Not Phishing Website, stay safe!'
        else:
            prediction_str = ''
        st.write(prediction_str)
        st.write(features_dataframe)

    except Exception as e:
        print(e)
        st.error("Not sure, what went wrong. We'll get back to you shortly!")

else:
    st.write("")
