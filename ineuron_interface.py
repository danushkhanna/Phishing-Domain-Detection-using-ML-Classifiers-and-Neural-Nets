import streamlit as st
import pickle
import pandas as pd
from extract_features import ExtractFeatures
from PIL import Image

# Load the image
image = Image.open('ineuron-logo1.png')
st.image(image, width=150)

import streamlit as st

st.markdown(
    "<div style='display: flex; align-items: center; margin-bottom: -10px;'>"
    "<h1 style='color:#003E7F; margin-right: 10px;'>Unmasking Phishing Websites:</h1>"
    "</div>"
    "<h1 style='color:orange; margin-left: 10px;'>A Machine Learning Approach</h1>"
    "</div>",
    unsafe_allow_html=True
)

image=Image.open('cybersecpic.jpeg')
width=750
height=500
image_new=image.resize((width,height))
st.image(image_new)

st.markdown("Phishing stands for a fraudulent process, where an attacker tries to obtain sensitive information from the victim. Usually, these kinds of attacks are done via emails, text messages, or websites. Phishing websites, which are nowadays in a considerable rise, have the same look as legitimate sites. However, their backend is designed to collect sensitive information that is inputted by the victim. Discovering and detecting phishing websites has recently also gained the machine learning community’s attention, which has built the models and performed classifications of phishing websites.")

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
