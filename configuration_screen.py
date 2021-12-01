import streamlit as st
import inflect

from Tribes import TribeManager

p = inflect.engine()


def configuration_widget(tribe_manager: TribeManager, tribes_dict: dict):
    st.subheader('Configuration')

    # cols = st.columns([.75, .75, 1, 1, 1, 1, 1])
    # cols[0].button('Load Config. File')
    # cols[1].button('Save Config. File')

    general_config_expander(tribe_manager)

    tribes_config_expander(tribe_manager, tribes_dict)

    tribe_manager.create_armies()


def general_config_expander(tribe_manager: TribeManager):
    with st.expander('General configuration'):
        tribe_manager.config_dict['general'] = dict()
        tribe_manager.config_dict['general']['damage_reduction'] = st.slider('Damage Reduction', 0.0, 1.0,
                                                                                           value=(0.05, 0.2),
                                                                                           key='damage_reduction')


def tribes_config_expander(tribe_manager: TribeManager, tribes_dict: dict):
    with st.expander('Tribes configuration'):

        cols = st.columns([1, 0.25, 1, 0.25, 1, 0.25, 1])

        _ = [cols[i * 2].markdown(f'#### {k.title()[:-1]} {i + 1}: {v}') for i, (k, v) in
             enumerate(tribes_dict.items())]

        for i, tribe in enumerate(tribe_manager.tribes):  # For each Tribe
            tribe_manager.config_dict[tribe.key] = {st.session_state['GLOBAL_TIERS'][0]: dict(),
                                                    st.session_state['GLOBAL_TIERS'][1]: dict(),
                                                    st.session_state['GLOBAL_TIERS'][2]: dict(),
                                                    st.session_state['GLOBAL_TIERS'][3]: dict(), }

            for j, tier in enumerate(st.session_state['GLOBAL_TIERS']):  # For each Tier (in Tribe)
                cols[i * 2].markdown(f'#### {tier.title()}')
                tribe_manager.config_dict[tribe.key][tier]['life'] = cols[i * 2].slider('Life', 1, 100, (50, 75),
                                                                                        key=f'{tribe.key}_{tier}_life')
                tribe_manager.config_dict[tribe.key][tier]['base_attack'] = cols[i * 2].slider('Base attack', 0, 25,
                                                                                               (20, 25),
                                                                                               key=f'{tribe.key}_{tier}_base_attack')
                tribe_manager.config_dict[tribe.key][tier]['num_attacks'] = cols[i * 2].slider('Number of attacks', 0,
                                                                                               10, (1, 3),
                                                                                               key=f'{tribe.key}_{tier}_num_attacks')
                tribe_manager.config_dict[tribe.key][tier]['evade_prob'] = cols[i * 2].slider('Evade probability', 0.0,
                                                                                              1.0,
                                                                                              value=(0.05, 0.2),
                                                                                              key=f'{tribe.key}_{tier}_evade_prob')
                tribe_manager.config_dict[tribe.key][tier]['hit_prob'] = cols[i * 2].slider('Hit probability', 0.0, 1.0,
                                                                                            value=(0.85, 0.95),
                                                                                            key=f'{tribe.key}_{tier}_hit_prob')
                tribe_manager.config_dict[tribe.key][tier]['heal'] = cols[i * 2].slider('Healing', 0, 10, (1, 3),
                                                                                        key=f'{tribe.key}_{tier}_heal')
