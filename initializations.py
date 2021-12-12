import streamlit as st

def init_global_variables():
    # GLOBAL VARIABLES
    st.session_state['GLOBAL_TIERS'] = ['gods', 'heroes', 'champions', 'soldiers']
    if 'GLOBAL_TRIBES_DICT' not in st.session_state:
        st.session_state['GLOBAL_TRIBES_DICT'] = {'tribe1': 'Punks', 'tribe2': 'Raperos',
                                                  'tribe3': 'Otakus', 'tribe4': 'Hippies', }
