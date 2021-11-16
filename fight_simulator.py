import random
import streamlit as st

from configuration_screen import *
from Battle import battle_manager
from Tribes import tribe_manager

# GLOBAL VARIABLES
GLOBAL_TRIBES_DICT = {'tribe1': 'Raperos', 'tribe2': 'Punks', 'tribe3': 'Otakus', 'tribe4': 'Jipis', }

random.seed('297145941b593410080ad664a30f7b4b371a6a0fa497b365b836c8f9252da782')

# Create tribes
tribe_manager.create_tribes(GLOBAL_TRIBES_DICT)

st.title('Urban Tribes')

# Sidebar Navigation
st.sidebar.header('Navigation')
options = st.sidebar.radio('', ('Configuration', 'Fight simulator'))

if options == 'Configuration':
    configuration_widget(tribe_manager, GLOBAL_TRIBES_DICT)

elif options == 'Fight simulator':
    st.subheader('Fight simulator')

    battle_manager.get_slots()

    # Show slots
    st.markdown('### Randomly generated initial slots')

    cols = st.columns([1, 1, 1, 1, 1, 1])
    _ = [cols[i].metric(f'{v.name}', f'Slot: {v.slot}', None) for i, v in
         enumerate(tribe_manager.tribes)]

    if st.button('Fight'):
        st.write('ToDo')
