import streamlit as st
import os
import snowflake.connector
import warnings
import pandas as pd
from snowflake.connector.connection import SnowflakeConnection

warnings.filterwarnings("ignore")

user = os.environ.get('user')
password = os.environ.get('password')
account = os.environ.get('account')

###Snow connection

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
#################

        
    
################
with st.sidebar:
    sel_ware = st.radio(
        "Warehouse",
        list_ware_up
    )

if sel_ware != 'Select below available wareshouse':
    if st.button('Create a new warehouse', on_click = create_ware(con)):
      def create_ware(con):
        ware_name = st.text_input('Enter Warehouse Name')
        ware_size = st.select_slider('Select size', ['XSMALL', 'SMALL', 'MEDIUM', 'LARGE', 'XLARGE', 'XXLARGE', 'XXXLARGE', 'X4LARGE', 'X5LARGE', 'X6LARGE'])
        sql_cmd = 'CREATE OR REPLACE WAREHOUSE  ' + str(ware_name) + ' ' +'WAREHOUSE_SIZE = '+ str(ware_size) +';'
        if st.button('Create Warehouse', key = 2, type="primary"):

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
      st.write('Thanks')
      #create_ware(con)
      pass
    st.subheader('Warehouse Information')

    st.dataframe(wareshouse[['name', 'size']].loc[wareshouse['name'] == sel_ware])


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
