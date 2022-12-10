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

with st.sidebar:
    add_radio = st.radio(
        "Warehouse",
        list_ware_up
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
