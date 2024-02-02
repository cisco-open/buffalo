
# Copyright 2024 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

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
