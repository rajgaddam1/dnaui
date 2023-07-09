import streamlit as st
import os
import spacy
import warnings
warnings.filterwarnings("ignore")
st.header("Name Identification in text", anchor=None)

text = st.text_input('Enter Text',label_visibility="visible")
