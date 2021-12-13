import streamlit as st
from Database import db_manager


def init_database_connection():
    print("Initializing database connection...")
    # Database
    db_manager.initialize_connection()

def init_process():
    print("Initializing global variables...")
    # GLOBAL VARIABLES
    st.session_state['GLOBAL_TIERS'] = ['gods', 'heroes', 'champions', 'soldiers']
    if 'GLOBAL_TRIBES_DICT' not in st.session_state:
        st.session_state['GLOBAL_TRIBES_DICT'] = {'tribe1': 'Punks', 'tribe2': 'Otakus',
                                                  'tribe3': 'Raperos', 'tribe4': 'Hippies', }
