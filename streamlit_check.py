import streamlit as st
import pyodbc

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={st.secrets['server']};"
    f"DATABASE={st.secrets['database']};"
    "Trusted_Connection=yes;"  # Use trusted connection if applicable
    ";LoginTimeout=30"  # Set login timeout to 30 seconds
)

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from Matches;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
