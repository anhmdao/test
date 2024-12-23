import streamlit as st

# Redash configuration
REDASH_URL = st.secrets["redash"]["url"]
API_KEY = st.secrets["redash"]["api_key"]

# Queries dictionary
QUERIES = {
    1004: st.secrets["queries"]["query_1004"],
    1204: st.secrets["queries"]["query_1204"],
    1968: st.secrets["queries"]["query_1968"],
    1921: st.secrets["queries"]["query_1921"]
}