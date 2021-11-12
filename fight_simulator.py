import streamlit as st
import random
from random import sample

random.seed('297145941b593410080ad664a30f7b4b371a6a0fa497b365b836c8f9252da782')

# GLOBAL VARIABLES
TRIBES = ['Raperos', 'Punks', 'Otakus', 'Jipis']


### Functions
def get_slots(tribes):
    slots = sample(['A', 'B', 'C', 'D'], 4)
    tribes_dict = {}
    for s, t in zip(slots, tribes):
        tribes_dict[t] = {'slot': s}

    return dict(sorted(tribes_dict.items(), key=lambda item: item[1]['slot']))  # Sort by slot


st.title('TeamFight Tokens')

st.subheader('Fight simulator')

tribes_text_input = [st.text_input(f'Tribe {i + 1}', TRIBES[i]) for i, _ in enumerate(TRIBES)]

if st.button('Get slots'):
    tribes_dict = get_slots(TRIBES)

    for k, v in tribes_dict.items():
        st.write(
            f'Tribe "{k}" is on slot {v["slot"]}')
