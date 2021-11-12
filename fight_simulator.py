import streamlit as st
import random
from random import sample

import Tribes as Tribes
from Tribes import Tribe

random.seed('297145941b593410080ad664a30f7b4b371a6a0fa497b365b836c8f9252da782')

# GLOBAL VARIABLES



### Functions
def get_slots(tribes):
    slots = sample(['A', 'B', 'C', 'D'], 4)
    tribes_dict = {}
    for s, t in zip(slots, tribes):
        tribes_dict[t] = {'slot': s}

    return dict(sorted(tribes_dict.items(), key=lambda item: item[1]['slot']))  # Sort by slot


st.title('TeamFight Tokens')

st.subheader('Fight simulator')

# Create Tribes #@TODO: Mover to Tribes.py
TRIBES = []
for tribe_name in Tribes.TRIBE_NAMES:
    TRIBES.append(Tribe(tribe_name))

tribes_text_input = [st.text_input(f'Tribe {i + 1}', TRIBES[i].name) for i, tribe in enumerate(TRIBES)]

if st.button('Get slots'):
    tribes_dict = get_slots(Tribes.TRIBE_NAMES)

    for k, v in tribes_dict.items():
        st.write(
            f'Tribe "{k}" is on slot {v["slot"]}')
