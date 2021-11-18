import streamlit as st

from Battle import battle_manager


def fight_simulator_widget(tribe_manager):
    st.subheader('Fight simulator')

    # Show slots
    st.markdown('### Randomly generated initial slots')

    cols = st.columns([1, 1, 1, 1, 1, 1])
    _ = [cols[i].metric(f'{v.name}', f'Slot: {v.slot}', None) for i, v in
         enumerate(tribe_manager.tribes)]

    if st.button('Fight'):
        battle_manager.main_battle_loop(tribe_manager)
