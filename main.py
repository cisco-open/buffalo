import json 
import requests 
import streamlit as st

from frontend.col1 import col1 
from frontend.col2A import col2A
from frontend.col2B import col2B

from const import INITIAL_STATE 
 

st.set_page_config(page_title='J-WATR-BUFFALO', layout="wide")

if 'demo_state' not in st.session_state: 
    st.session_state.demo_state = INITIAL_STATE 

lhs, _, rhs = st.columns([0.3, 0.1, 0.6]) 

with lhs: 
    col1()

with _: pass # Empty space (col)

with rhs: 
    col2A()
    if st.session_state.demo_state['selected_generation']: col2B() 
