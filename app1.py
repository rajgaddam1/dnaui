# -*- coding: utf-8 -*-
import streamlit as st
import os
import snowflake.connector
import warnings 
warnings.filterwarnings("ignore")

st.title("DNA Hackathon", anchor=None)

selected_database = st.selectbox("Select the Databse Name", ("None","student", "employee"))
st.write(selected_database)

selected_schema = st.selectbox("Select the Schema Name", ("None","info", "contact"))
st.write(selected_schema)

first_name = st.text_input('Enter your First Name')
st.write(first_name)

last_name = st.text_input('Enter your Last Name')
st.write(last_name)

email_id = st.text_input('Enter your Email')
st.write(email_id)

contact_no = st.text_input('Enter your Contact Number')
st.write(contact_no)

address = st.text_input('Enter your Address')
st.write(address)

user = os.environ.get('user')
password = os.environ.get('password')
insert_query = """

    INSERT INTO INFO.DETAILS (FIRST_NAME,LAST_NAME,EMAIL_ID,CONTACT_NO,ADDRESS) 
       VALUES(%s,%s,%s,%s,%s);
"""

if st.button("submit"):
    with snowflake.connector.connect(
    user = user,
    password = password,
    account = 'VK83964.ap-southeast-1',
    warehouse = 'DNAHACK',
    database = 'DNAHACK',
    schema = 'INFO'
    ) as con:
        
        try:
            cur = con.cursor()
            cur.execute(insert_query,(first_name,last_name,email_id,contact_no,address))
        except Exception as e:
            print(e)
        finally:
            cur.close()
    con.close()
    st.write('Added to the database')
