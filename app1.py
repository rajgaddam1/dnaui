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

def get_connector() -> SnowflakeConnection:
    """Create a connector to SnowFlake using credentials filled in Streamlit secrets"""
    con = snowflake.connector.connect(
    user = user,
    password = password,
    account = account,
    warehouse='DNAHACK')
    return con

snowflake_connector = get_connector()

def get_databases(_connector) -> pd.DataFrame:
    return pd.read_sql("SHOW DATABASES;", _connector)

databases = get_databases(snowflake_connector)

st.sidebar.["element_name"]
