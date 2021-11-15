import random
import streamlit as st

from Battle import battle_manager
from Tribes import tribe_manager

st.set_page_config(layout='wide')

# GLOBAL VARIABLES
TRIBE_NAMES_PLACEHOLDER = ['Raperos', 'Punks', 'Otakus', 'Jipis']

random.seed('297145941b593410080ad664a30f7b4b371a6a0fa497b365b836c8f9252da782')

st.title('TeamFight Tokens')

st.subheader('Fight simulator')

# Input container
with st.container():

    # Create Tribes from Text Input with  Placeholder pre-fill
    cols = st.columns([.75, 0.25, 1, 1, 1, 1])

    with cols[0]:
        tribes_names_input = [st.text_input(f'Tribe {i + 1}', TRIBE_NAMES_PLACEHOLDER[i])
                              for i, tribe in enumerate(TRIBE_NAMES_PLACEHOLDER)]

        tribe_manager.create_tribes(tribes_names_input)

    if st.button('Get slots'):
        battle_manager.get_slots()

        # Show slots
        _ = [cols[i+2].metric(f'{v.name}', f'Slot: {v.slot}', None) for i, v in
             enumerate(tribe_manager.tribes)]

        # Show config cards
        _ = [st.info(f'Army member {i+1}: {type(v).__name__} from {tribe_manager.tribes[0].name} Tribe') for i,v in enumerate(tribe_manager.tribes[0].army.brawlers)]

