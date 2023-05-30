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

st.markdown("### *Yep, Literally!*")
st.markdown("#### *Try It Out!*")
st.markdown("Type in that link that your 'bank' sent you XD!")

st.markdown("### *Our Approach*")
st.markdown("To tackle this challenge, we leveraged classical machine learning techniques, including Data Exploration, Data Cleaning, Feature Engineering, Model Building, and Model Testing. Our comprehensive approach involved experimenting with different machine learning algorithms to identify the most suitable ones for this particular case.")
st.markdown("### *Key Features*")
st.markdown("- URL-Based Features: We extracted insightful features from the URL itself to capture potential indicators of phishing behavior.")
st.markdown("- Domain-Based Features: By analyzing the domain properties, we uncovered valuable attributes that help distinguish between genuine and malicious domains.")
st.markdown("- Page-Based Features: We delved into the contents of web pages associated with each domain, uncovering unique features that shed light on their legitimacy.")
st.markdown("- Content-Based Features: Leveraging the textual content present on web pages, we derived additional features that contribute to the overall detection accuracy.")

st.markdown("### *Results*")
st.markdown("Our solution provides a robust and reliable method for predicting whether a domain is authentic or fake. By utilizing the power of machine learning, we have created a model that can effectively discern the telltale signs of phishing attempts, enabling users to make informed decisions and avoid potential security breaches.")


