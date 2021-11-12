import streamlit as st
import random

import Tribes as Tribes
from Tribes import TribeManager
from Tribes import Tribe

st.set_page_config(layout='wide')

# GLOBAL VARIABLES
TRIBE_NAMES_PLACEHOLDER = ['Raperos', 'Punks', 'Otakus', 'Jipis']

random.seed('297145941b593410080ad664a30f7b4b371a6a0fa497b365b836c8f9252da782')

st.title('TeamFight Tokens')

st.subheader('Fight simulator')

# Create Tribes from Text Input with  Placeholder pre-fill
tribe_manager = TribeManager()
cols = st.columns(len(tribe_manager.slots))
with cols[0]:
    tribes_names_input = [st.text_input(f'Tribe {i + 1}', TRIBE_NAMES_PLACEHOLDER[i])
                          for i, tribe in enumerate(TRIBE_NAMES_PLACEHOLDER)]
    tribe_manager.create_tribes(tribes_names_input)

if st.button('Get slots'):
    tribe_manager.get_slots()
    cols = st.columns(len(tribe_manager.slots))
    _ = [cols[i].write(f'Tribe "{v.name}" is on slot {v.slot}') for i, v in enumerate(tribe_manager.tribes)]
