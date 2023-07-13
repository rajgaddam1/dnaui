import streamlit as st
import os
import spacy
import warnings
warnings.filterwarnings("ignore")
st.header("Name Identification in text", anchor=None)

def contains_name(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            names.append(ent.text)
    return names

text = st.text_input('Enter Text',label_visibility="visible")
if st.button("Submit"):
    names_idn = contains_name(text)
    if len(names_idn) == 0:
        st.error('No names identified in the text')
    else:
        st.success('Below names identified in the text')
        st.write(names_idn)

        
  
    
