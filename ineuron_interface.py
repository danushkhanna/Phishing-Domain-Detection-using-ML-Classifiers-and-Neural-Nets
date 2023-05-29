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

st.markdown("### *Abstract*")
st.markdown("Phishing stands for a fraudulent process, where an attacker tries to obtain sensitive information from the victim. Usually, these kinds of attacks are done via emails, text messages, or websites. Phishing websites, which are nowadays in a considerable rise, have the same look as legitimate sites. However, their backend is designed to collect sensitive information that is inputted by the victim. Discovering and detecting phishing websites has recently also gained the machine learning community’s attention, which has built the models and performed classifications of phishing websites. This paper presents two dataset variations that consist of 58,645 and 88,647 websites labeled as legitimate or phishing and allow the researchers to train their classification models, build phishing detection systems, and mining association rules.")
st.markdown("### *Value of the Data*")
st.markdown("- These data consist of a collection of legitimate, as well as phishing website instances. Each website is represented by the set of features that denote whether the website is legitimate or not. Data can serve as input for the machine learning process.")
st.markdown("- Machine learning and data mining researchers can benefit from these datasets, while also computer security researchers and practitioners. Computer security enthusiasts can find these datasets interesting for building firewalls, intelligent ad blockers, and malware detection systems.")            
st.markdown("- This dataset can help researchers and practitioners easily build classification models in systems preventing phishing attacks since the presented datasets feature the attributes which can be easily extracted.")
st.markdown("- Finally, the provided datasets could also be used as a performance benchmark for developing state-of-the-art machine learning methods for the task of phishing websites classification.")

# Define the table data
data = {
    'Nr.': list(range(1, 21)),
    'Attribute': [
        'qty_dot_url', 'qty_hyphen_url', 'qty_underline_url', 'qty_slash_url', 'qty_questionmark_url',
        'qty_equal_url', 'qty_at_url', 'qty_and_url', 'qty_exclamation_url', 'qty_space_url',
        'qty_tilde_url', 'qty_comma_url', 'qty_plus_url', 'qty_asterisk_url', 'qty_hashtag_url',
        'qty_dollar_url', 'qty_percent_url', 'qty_tld_url', 'length_url', 'email_in_url'
    ],
    'Format': [
        'Number of "." signs', 'Number of "-" signs', 'Number of "_" signs', 'Number of "/" signs',
        'Number of "?" signs', 'Number of "=" signs', 'Number of "@" signs', 'Number of "&" signs',
        'Number of "!" signs', 'Number of " " signs', 'Number of "~" signs', 'Number of "," signs',
        'Number of "+" signs', 'Number of "*" signs', 'Number of "#" signs', 'Number of "$" signs',
        'Number of "%" signs', 'Top level domain character length', 'Number of characters', 'Is email present'
    ],
    'Description': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    'Values': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '[0, 1]']
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Display the table using st.table
st.table(df)

   
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
