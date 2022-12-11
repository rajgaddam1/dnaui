import streamlit as st
import os
import snowflake.connector
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from snowflake.connector.connection import SnowflakeConnection


##To manage bug in sreamlit(Intialize button click)
if 'key' not in st.session_state:
    st.session_state.key = False

def callback():
    st.session_state.key = True
    
###Function to convert data to csv

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

##############Snowflake Credentials
user = os.environ.get('user')
password = os.environ.get('password')
account = os.environ.get('account')
#################

def style_button_row(clicked_button_ix, n_buttons):
    def get_button_indices(button_ix):
        return {
            'nth_child': button_ix,
            'nth_last_child': n_buttons - button_ix + 1
        }

    clicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        border-color: rgb(255, 75, 75);
        color: rgb(255, 75, 75);
        box-shadow: rgba(255, 75, 75, 0.5) 0px 0px 0px 0.2rem;
        outline: currentcolor none medium;
    }
    """
    unclicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        pointer-events: none;
        cursor: not-allowed;
        opacity: 0.65;
        filter: alpha(opacity=65);
        -webkit-box-shadow: none;
        box-shadow: none;
    }
    """
    style = ""
    for ix in range(n_buttons):
        ix += 1
        if ix == clicked_button_ix:
            style += clicked_style % get_button_indices(ix)
        else:
            style += unclicked_style % get_button_indices(ix)
    st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

###Snow connection#######

con = snowflake.connector.connect(
                    user = user,
                    password = password,
                    account='MD93775.ap-southeast-1')

####Snowflake connection
def get_connector() -> SnowflakeConnection:
    """Create a connector to SnowFlake using credentials filled in Streamlit secrets"""
    con = snowflake.connector.connect(
    user = user,
    password = password,
    account = account,
    warehouse='DNAHACK')
    return con

snowflake_connector = get_connector()
#####Show warehouses
def get_wareshouse(_connector) -> pd.DataFrame:
    return pd.read_sql("SHOW WAREHOUSES;", _connector)

wareshouse = get_wareshouse(snowflake_connector)

list_ware = wareshouse['name'].to_list()
list_up = ['Select below available wareshouse']
list_ware_up = list_up + list_ware

##Snowflake Waarehouse dataframe to csv

ware_csv = convert_df(wareshouse)
#################

def create_ware(con):
    ware_name = st.text_input('Enter Warehouse Name')
    ware_size = st.select_slider('Select size', ['XSMALL', 'SMALL', 'MEDIUM', 'LARGE', 'XLARGE', 'XXLARGE', 'XXXLARGE', 'X4LARGE', 'X5LARGE', 'X6LARGE'])
    sql_cmd = 'CREATE OR REPLACE WAREHOUSE  ' + str(ware_name) + ' ' +'WAREHOUSE_SIZE = '+ str(ware_size) +';'
    if st.button('Create Warehouse', on_click=style_button_row, kwargs={
        'clicked_button_ix': 1, 'n_buttons': 4}):
        
        try:
            cur = con.cursor()
            cur.execute(sql_cmd)
            st.write('Warehouse has been created')
        except Exception as e:
            print(e)
            st.write('An error has occured please check logs')
        finally:
            cur.close()
        con.close()
        
    
################
with st.sidebar:
    sel_ware = st.radio(
        "Warehouse",
        list_ware_up
    )

if sel_ware != 'Select below available wareshouse':
    if st.button('Create a new warehouse', on_click = callback) or st.session_state.key:
        
        create_ware(con)
        #pass
    st.subheader('Warehouse Information')

    st.dataframe(wareshouse[['name', 'size']].loc[wareshouse['name'] == sel_ware])
    
    st.markdown("Click on below button to Download full Information about Warehouse")
    st.download_button(
    label = "Download data as CSV",
    data = ware_csv,
    file_name = 'Warehouse_info.csv',
    mime = 'text/csv',
)


####ShowDatabases
def get_databases(_connector) -> pd.DataFrame:
    return pd.read_sql("SHOW DATABASES;", _connector)

databases = get_databases(snowflake_connector)

list_data = databases['name'].to_list()
list_up = ['Select below available Databases']
list_data_up = list_up + list_data

with st.sidebar:
    add_radio = st.radio(
        "Databases",
        list_data_up
    )
