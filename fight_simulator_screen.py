import streamlit as st

from Battle import battle_manager


def fight_simulator_widget(tribe_manager):
    st.subheader('Fight simulator')

    # Show slots
    st.markdown('### Randomly generated initial slots')

    cols = st.columns([1, 1, 1, 1, 1, 1])
    _ = [cols[i].metric(f'{v.name}', f'Slot: {v.slot}', None) for i, v in
         enumerate(tribe_manager.tribes)]

    st.markdown('---')

    cols = st.columns(6)

    if cols[0].button('Full fight'):

        if len(battle_manager.alive_tribes) < 4:
            battle_manager.reset(tribe_manager)

        if len(battle_manager.alive_tribes) == 4:
            battle_manager.main_battle_loop(tribe_manager, one_round=False)

    elif cols[1].button('Next Round'):
        if len(battle_manager.alive_tribes) == 0 or len(battle_manager.alive_tribes) == 1:
            battle_manager.reset(tribe_manager)
        if len(battle_manager.alive_tribes) > 1:
            battle_manager.main_battle_loop(tribe_manager, one_round=True)
