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
    "<div style='display: flex; align-items: center; margin-bottom: -35px;'>"
    "<h1 style='color:#003E7F; margin-center: 10px;'> Let's Go</h1>"
    "</div>"
    "<h1 style='color:orange; margin-center: 10px;'>Phishing!</h1>"
    "</div>",
    unsafe_allow_html=True
)

image=Image.open('phising1.jpeg')
width=750
height=700
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

st.markdown("### *Our Approach*")
st.markdown("To tackle this challenge, we leveraged classical machine learning techniques, including Data Exploration, Data Cleaning, Feature Engineering, Model Building, and Model Testing. Our comprehensive approach involved experimenting with different machine learning algorithms to identify the most suitable ones for this particular case.")
st.markdown("### *Key Features*")
st.markdown("- URL-Based Features: We extracted insightful features from the URL itself to capture potential indicators of phishing behavior.")
st.markdown("- Domain-Based Features: By analyzing the domain properties, we uncovered valuable attributes that help distinguish between genuine and malicious domains.")
st.markdown("- Page-Based Features: We delved into the contents of web pages associated with each domain, uncovering unique features that shed light on their legitimacy.")
st.markdown("- Content-Based Features: Leveraging the textual content present on web pages, we derived additional features that contribute to the overall detection accuracy.")

st.markdown("### *Results*")
st.markdown("Our solution provides a robust and reliable method for predicting whether a domain is authentic or fake. By utilizing the power of machine learning, we have created a model that can effectively discern the telltale signs of phishing attempts, enabling users to make informed decisions and avoid potential security breaches.")


