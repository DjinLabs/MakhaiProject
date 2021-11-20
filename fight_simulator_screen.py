import streamlit as st

from Battle import battle_manager


def fight_simulator_widget(tribe_manager):
    st.subheader('Fight simulator')

    # Show slots
    st.markdown('### Randomly generated initial slots')

    cols = st.columns([1, 1, 1, 1, 1, 1])
    _ = [cols[i].metric(f'{v.name}', f'Slot: {v.slot}', None) for i, v in
         enumerate(tribe_manager.tribes)]

    if cols[0].button('Fight'):

        if len(battle_manager.alive_tribes) < 4:
            battle_manager.reset(tribe_manager)

        if len(battle_manager.alive_tribes) == 4:
            battle_manager.setup_battle(tribe_manager)
            battle_manager.main_battle_loop(tribe_manager)
