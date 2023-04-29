import streamlit as st
import pickle
import pandas as pd
import re
import whois
import tldextract
import time
from urllib.parse import urlparse, parse_qs

def parse_url(url):
    # Parse the URL into its components
    if '//' not in url:
        url = '//' + url

    parsed_url = urlparse(url)

    # Extract the domain name
    domain = parsed_url.netloc

    # Extract the path and split it into directories and file name
    path = parsed_url.path
    try:
        directories, file = path.rsplit('/', 1)
    except:
        if '.' in path:
            file = path
            directories = ""
        else:
            directories = path
            file = ""

    # Extract the query parameters
    parameters = parse_qs(parsed_url.query)

    tld_info = tldextract.extract(url)
    tld = tld_info.suffix

    # Count the number of top-level domains
    num_tlds = tld.count('.') + 1

    tld_params = parsed_url.netloc.split('.')[-1]
    if tld_params in parameters:
        tld_present = True
    else:
        tld_present = False

    if re.search(r'[\w\-.]+@[\w\-.]+\.\w+', url):
        email = True
    else:
        email = False

    return domain, directories, file, parameters, email, tld_present, num_tlds

def get_domain_info(domain):
    try:
        # Get the domain information using python-whois
        domain_info = whois.whois(domain)

        # Extract the creation and expiration time
        creation_time = domain_info.creation_date
        expiration_time = domain_info.expiration_date

        # Convert the time to seconds
        if creation_time != None and expiration_time != None:
            creation_time_seconds = time.mktime(creation_time.timetuple())
            expiration_time_seconds = time.mktime(expiration_time.timetuple())
        else:
            raise ValueError
    except:
        creation_time_seconds = -1
        expiration_time_seconds = -1

    return creation_time_seconds, expiration_time_seconds

def count_sign(param, sign):
    num = 0
    if len(param) != 0:
        for value in param.values():
            num += value.count(sign)
    return num

@st.cache_resource
def get_features():
    features_list = []
    with open('features.csv') as feat_file:
        for line in feat_file:
            features_list.append(line.rstrip())
    return features_list

def url_to_features(url):
    features_list = get_features()
    new_dataset = {}

    signs_dict = {"dot":".", 
            "hyphen":"-", 
            "underline": "_", 
            "slash":"/", 
            "questionmark": "?", 
            "equal":"=", 
            "at": "@", 
            "and": "&", 
            "exclamation": "!", 
            "space": " ", 
            "tilde": "~",
            "comma": ",", 
            "plus": "+", 
            "asterisk": "∗", 
            "hashtag": "#", 
            "dollar": "$", 
            "percent": "%"}

    return_val = parse_url(url)
    if  return_val != None:
        domain, directory, file, parameters, email_in_url, tld_present_params, qty_tld_url = parse_url(url)
    else:
        st.write("Invalid URL")
        return

    new_dataset['length_url'] = len(url)
    new_dataset['directory_length'] = len(directory)
    new_dataset['file_length'] = len(file)
    new_dataset['params_length'] = len(str(parameters.values()))
    new_dataset['qty_params'] = len(parameters)
    new_dataset['email_in_url'] = int(email_in_url)
    new_dataset['tld_present_params'] = int(tld_present_params)
    new_dataset['qty_tld_url'] = qty_tld_url
    new_dataset['time_domain_activation'], new_dataset['time_domain_expiration'] = get_domain_info(str(domain))
    new_dataset['qty_vowels_domain'] = len(list(filter(lambda char: char in "aeiouAEIOU", domain)))

    for sign_name, sign in signs_dict.items():
        
        if f'qty_{sign_name}_url' in features_list:
            new_dataset[f'qty_{sign_name}_url'] = url.count(sign)

        if f'qty_{sign_name}_domain' in features_list:
            new_dataset[f'qty_{sign_name}_domain'] = domain.count(sign)

        if f'qty_{sign_name}_directory' in features_list:
            new_dataset[f'qty_{sign_name}_directory'] = directory.count(sign)

        if f'qty_{sign_name}_file' in features_list:
            new_dataset[f'qty_{sign_name}_file'] = file.count(sign)

        if f'qty_{sign_name}_params' in features_list:
            new_dataset[f'qty_{sign_name}_params'] = count_sign(parameters, sign)

    reordered_dict = {k: new_dataset[k] for k in features_list}
    return reordered_dict

@st.cache_resource
def get_model():
    with open('phishing_url_detector.pkl', 'rb') as pickle_model:
        phishing_url_detector = pickle.load(pickle_model)
    return phishing_url_detector

st.title("Phishing Website Detector")
st.header("Are you sure your 'bank' sent that link?")

input_url = st.text_area("Put in your sus site link here: ")

if input_url != "":
    features_url = url_to_features(input_url)
    features_dataframe = pd.DataFrame.from_dict([features_url])
    features_dataframe = features_dataframe.fillna(-1)
    features_dataframe = features_dataframe.astype(int)

    st.write("Okay!")
    st.cache_data.clear()
    prediction_str = ""

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

    except Exception as e:
        print(e)
        st.error("Not sure, what went wrong. We'll get back to you shortly!")

else:
    st.write("")
