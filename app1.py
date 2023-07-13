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
            return names, True
    return False

text = st.text_input('Enter Text',label_visibility="visible")
if st.button("Submit"):
    a,b = contains_name(text)
    if b == False:
        st.write('The text has no Names')
    if b == True:
        st.write('The text has Names')
        st.write(a)
        
  
    
