import streamlit as st

from Battle import battle_manager
from configuration_screen import configuration_widget
from fight_simulator_screen import fight_simulator_widget
from battle_dashboard_screen import dashboard_widget
from Tribes import tribe_manager
from initializations import init_process, init_database_connection


def streamlit_initialization():
    #random.seed('297145941b593410080ad664a30f7b4b371a6a0fa497b365b836c8f9252da782')
    st.set_page_config(layout='wide')


def main_loop():
    # Create tribes
    tribe_manager.create_tribes(st.session_state['GLOBAL_TRIBES_DICT'])

    # Sidebar Navigation
    st.sidebar.header('Navigation')
    options = st.sidebar.radio('', ('Configuration', 'Fight simulator', 'Battle Dashboard',))
    reset_btn = st.sidebar.button('Reset')

    st.title('Urban Tribes')

    if options == 'Configuration':
        configuration_widget(tribe_manager)
    if options == 'Fight simulator':
        fight_simulator_widget(tribe_manager)

    if options == 'Battle Dashboard':
        dashboard_widget(tribe_manager)

    if reset_btn:
        print('Reset')
        battle_manager.setup_battle(tribe_manager)


# Main loop
streamlit_initialization()
init_process()
init_database_connection()
main_loop()
