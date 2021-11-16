import streamlit as st

from Tribes import TribeManager

st.set_page_config(layout='wide')


def configuration_widget(tribe_manager: TribeManager, tribes_dict: dict):
    st.subheader('Configuration')

    cols = st.columns([1, 0.25, 1, 0.25, 1, 0.25, 1])

    _ = [cols[i * 2].markdown(f'#### {k.title()}: {v}') for i, (k,v) in enumerate(tribes_dict.items())]

    config_dict = {'tribe1': {'gods': dict(), 'heroes': dict(), 'champs': dict(), 'solds': dict(), },
                   'tribe2': {'gods': dict(), 'heroes': dict(), 'champs': dict(), 'solds': dict(), },
                   'tribe3': {'gods': dict(), 'heroes': dict(), 'champs': dict(), 'solds': dict(), },
                   'tribe4': {'gods': dict(), 'heroes': dict(), 'champs': dict(), 'solds': dict(), }, }

    # Tribe 1
    cols[0].markdown('##### Gods')
    config_dict['tribe1']['gods']['base_attack'] = cols[0].slider('Base attack', 0, 25, 10,
                                                                  key='tribe1_gods_base_attack')
    config_dict['tribe1']['gods']['hit_prob'] = cols[0].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                               key='tribe1_gods_hit_prob_attack')
    config_dict['tribe1']['gods']['evade_prob'] = cols[0].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                 key='tribe1_gods_evade_prob_attack')

    cols[0].markdown('##### Heroes')
    config_dict['tribe1']['heroes']['base_attack'] = cols[0].slider('Base attack', 0, 25, 10,
                                                                 key='tribe1_heroes_base_attack')
    config_dict['tribe1']['heroes']['hit_prob'] = cols[0].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe1_heroes_hit_prob_attack')
    config_dict['tribe1']['heroes']['evade_prob'] = cols[0].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe1_heroes_evade_prob_attack')

    cols[0].markdown('##### Champions')
    config_dict['tribe1']['champs']['base_attack'] = cols[0].slider('Base attack', 0, 25, 10,
                                                                    key='tribe1_champs_base_attack')
    config_dict['tribe1']['champs']['hit_prob'] = cols[0].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe1_champs_hit_prob_attack')
    config_dict['tribe1']['champs']['evade_prob'] = cols[0].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe1_champs_evade_prob_attack')

    cols[0].markdown('##### Soldiers')
    config_dict['tribe1']['solds']['base_attack'] = cols[0].slider('Base attack', 0, 25, 10,
                                                                   key='tribe1_solds_base_attack')
    config_dict['tribe1']['solds']['hit_prob'] = cols[0].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                key='tribe1_solds_hit_prob_attack')
    config_dict['tribe1']['solds']['evade_prob'] = cols[0].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                  key='tribe1_solds_evade_prob_attack')

    # Tribe 2
    cols[2].markdown('##### Gods')
    config_dict['tribe2']['gods']['base_attack'] = cols[2].slider('Base attack', 0, 25, 10,
                                                                  key='tribe2_gods_base_attack')
    config_dict['tribe2']['gods']['hit_prob'] = cols[2].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                               key='tribe2_gods_hit_prob_attack')
    config_dict['tribe2']['gods']['evade_prob'] = cols[2].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                 key='tribe2_gods_evade_prob_attack')

    cols[2].markdown('##### Heroes')
    config_dict['tribe2']['heroes']['base_attack'] = cols[2].slider('Base attack', 0, 25, 10,
                                                                    key='tribe2_heroes_base_attack')
    config_dict['tribe2']['heroes']['hit_prob'] = cols[2].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe2_heroes_hit_prob_attack')
    config_dict['tribe2']['heroes']['evade_prob'] = cols[2].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe2_heroes_evade_prob_attack')

    cols[2].markdown('##### Champions')
    config_dict['tribe2']['champs']['base_attack'] = cols[2].slider('Base attack', 0, 25, 10,
                                                                    key='tribe2_champs_base_attack')
    config_dict['tribe2']['champs']['hit_prob'] = cols[2].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe2_champs_hit_prob_attack')
    config_dict['tribe2']['champs']['evade_prob'] = cols[2].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe2_champs_evade_prob_attack')

    cols[2].markdown('##### Soldiers')
    config_dict['tribe2']['solds']['base_attack'] = cols[2].slider('Base attack', 0, 25, 10,
                                                                   key='tribe2_solds_base_attack')
    config_dict['tribe2']['solds']['hit_prob'] = cols[2].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                key='tribe2_solds_hit_prob_attack')
    config_dict['tribe2']['solds']['evade_prob'] = cols[2].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                  key='tribe2_solds_evade_prob_attack')

    # Tribe 3
    cols[4].markdown('##### Gods')
    config_dict['tribe3']['gods']['base_attack'] = cols[4].slider('Base attack', 0, 25, 10,
                                                                  key='tribe3_gods_base_attack')
    config_dict['tribe3']['gods']['hit_prob'] = cols[4].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                               key='tribe3_gods_hit_prob_attack')
    config_dict['tribe3']['gods']['evade_prob'] = cols[4].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                 key='tribe3_gods_evade_prob_attack')

    cols[4].markdown('##### Heroes')
    config_dict['tribe3']['heroes']['base_attack'] = cols[4].slider('Base attack', 0, 25, 10,
                                                                    key='tribe3_heroes_base_attack')
    config_dict['tribe3']['heroes']['hit_prob'] = cols[4].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe3_heroes_hit_prob_attack')
    config_dict['tribe3']['heroes']['evade_prob'] = cols[4].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe3_heroes_evade_prob_attack')

    cols[4].markdown('##### Champions')
    config_dict['tribe3']['champs']['base_attack'] = cols[4].slider('Base attack', 0, 25, 10,
                                                                    key='tribe3_champs_base_attack')
    config_dict['tribe3']['champs']['hit_prob'] = cols[4].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe3_champs_hit_prob_attack')
    config_dict['tribe3']['champs']['evade_prob'] = cols[4].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe3_champs_evade_prob_attack')

    cols[4].markdown('##### Soldiers')
    config_dict['tribe3']['solds']['base_attack'] = cols[4].slider('Base attack', 0, 25, 10,
                                                                   key='tribe3_solds_base_attack')
    config_dict['tribe3']['solds']['hit_prob'] = cols[4].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                key='tribe3_solds_hit_prob_attack')
    config_dict['tribe3']['solds']['evade_prob'] = cols[4].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                  key='tribe3_solds_evade_prob_attack')

    # Tribe 4
    cols[6].markdown('##### Gods')
    config_dict['tribe4']['gods']['base_attack'] = cols[6].slider('Base attack', 0, 25, 10,
                                                                  key='tribe4_gods_base_attack')
    config_dict['tribe4']['gods']['hit_prob'] = cols[6].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                               key='tribe4_gods_hit_prob_attack')
    config_dict['tribe4']['gods']['evade_prob'] = cols[6].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                 key='tribe4_gods_evade_prob_attack')

    cols[6].markdown('##### Heroes')
    config_dict['tribe4']['heroes']['base_attack'] = cols[6].slider('Base attack', 0, 25, 10,
                                                                    key='tribe4_heroes_base_attack')
    config_dict['tribe4']['heroes']['hit_prob'] = cols[6].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe4_heroes_hit_prob_attack')
    config_dict['tribe4']['heroes']['evade_prob'] = cols[6].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe4_heroes_evade_prob_attack')

    cols[6].markdown('##### Champions')
    config_dict['tribe4']['champs']['base_attack'] = cols[6].slider('Base attack', 0, 25, 10,
                                                                    key='tribe4_champs_base_attack')
    config_dict['tribe4']['champs']['hit_prob'] = cols[6].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                 key='tribe4_champs_hit_prob_attack')
    config_dict['tribe4']['champs']['evade_prob'] = cols[6].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                   key='tribe4_champs_evade_prob_attack')

    cols[6].markdown('##### Soldiers')
    config_dict['tribe4']['solds']['base_attack'] = cols[6].slider('Base attack', 0, 25, 10,
                                                                   key='tribe4_solds_base_attack')
    config_dict['tribe4']['solds']['hit_prob'] = cols[6].slider('Hit probability', 0.0, 1.0, value=0.8,
                                                                key='tribe4_solds_hit_prob_attack')
    config_dict['tribe4']['solds']['evade_prob'] = cols[6].slider('Evade probability', 0.0, 1.0, value=0.4,
                                                                  key='tribe4_solds_evade_prob_attack')

    tribe_manager.create_armies(config_dict)


