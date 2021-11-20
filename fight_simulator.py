import streamlit as st
import random

from configuration_screen import configuration_widget
from fight_simulator_screen import fight_simulator_widget
from Tribes import tribe_manager

# Configs

random.seed('297145941b593410080ad664a30f7b4b371a6a0fa497b365b836c8f9252da782')
st.set_page_config(layout='wide')

# GLOBAL VARIABLES
st.session_state['GLOBAL_TIERS'] = ['gods', 'heroes', 'champions', 'soldiers']
if 'GLOBAL_TRIBES_DICT' not in st.session_state:
    st.session_state['GLOBAL_TRIBES_DICT'] = {'tribe1': 'Raperos', 'tribe2': 'Punks',
                                              'tribe3': 'Otakus', 'tribe4': 'Jipis', }

# Create tribes
tribe_manager.create_tribes(st.session_state['GLOBAL_TRIBES_DICT'])

# Sidebar Navigation
st.sidebar.header('Navigation')
options = st.sidebar.radio('', ('Configuration', 'Fight simulator'))
reset_btn = st.sidebar.button('Reset')

st.title('Urban Tribes')

if options == 'Configuration':
    configuration_widget(tribe_manager, st.session_state['GLOBAL_TRIBES_DICT'])

if options == 'Fight simulator':
    fight_simulator_widget(tribe_manager)

if reset_btn:
    # TODO: Proper reset function taking into account: TribeManager, BattleManager...
    st.sidebar.error('Reset not implemented yet. Refresh the page for resetting the battle.')
    tribe_manager.create_tribes(st.session_state['GLOBAL_TRIBES_DICT'])
