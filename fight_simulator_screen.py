import streamlit as st

from Battle import battle_manager, Status


def fight_simulator_widget(tribe_manager):
    st.subheader('Fight simulator')

    # Titles and fight controls
    cols = st.columns([1, 1, 1, 1, 1])
    cols[0].markdown('#### Initial slots')
    cols[1].markdown('#### <span style="color:white">FOO</span>', unsafe_allow_html=True)
    cols[2].markdown('#### <span style="color:white">FOO</span>', unsafe_allow_html=True)
    cols[3].markdown('#### <span style="color:white">FOO</span>', unsafe_allow_html=True)
    cols[4].markdown('#### Fight Controls')

    # Show slots
    _ = [cols[i].metric(f'{v.name}', f'Slot: {v.slot}', None) for i, v in
         enumerate(tribe_manager.tribes)]

    st.markdown('---')

    print(f'STATUS: {battle_manager.status}')
    if cols[4].button('Full fight') and battle_manager.status != Status.RUNNING:
        battle_manager.run_battle(tribe_manager, one_round=False)

    if cols[4].button('Next Round') and battle_manager.status != Status.RUNNING:
        battle_manager.run_battle(tribe_manager, one_round=True)

    if cols[4].button('Pause') and battle_manager.status == Status.RUNNING:
        # TODO: Si tenemos un método que simplemente haga el output de la batalla, lo suyo sería llamarlo aquí.
        # de esta manera el pause funcionaría correctamente en el full fight y si se pulsa tras un next round
        # no se va la visualización
        battle_manager.run_battle(tribe_manager, one_round=True)
