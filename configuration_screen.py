import streamlit as st
import inflect

from Tribes import TribeManager

p = inflect.engine()


# TODO: Añadir panel  de configuraciones generales y añadir:
#  DAÑO DE CONTRAATAQUE (del BattleManager) (entre 40 y 60% del daño total del NFT atacado)


def configuration_widget(tribe_manager: TribeManager, tribes_dict: dict):
    st.subheader('Configuration')

    cols = st.columns([1, 0.25, 1, 0.25, 1, 0.25, 1])

    _ = [cols[i * 2].markdown(f'#### {k.title()[:-1]} {i + 1}: {v}') for i, (k, v) in enumerate(tribes_dict.items())]

    config_dict = dict()
    for i, tribe in enumerate(tribe_manager.tribes):  # For each Tribe
        config_dict[tribe.key] = {st.session_state['GLOBAL_TIERS'][0]: dict(),
                                  st.session_state['GLOBAL_TIERS'][1]: dict(),
                                  st.session_state['GLOBAL_TIERS'][2]: dict(),
                                  st.session_state['GLOBAL_TIERS'][3]: dict(), }

        for j, tier in enumerate(st.session_state['GLOBAL_TIERS']):  # For each Tier (in Tribe)
            cols[i * 2].markdown(f'#### {tier.title()}')
            config_dict[tribe.key][tier]['life'] = cols[i * 2].slider('Life', 1, 100, (50, 75),
                                                                      key=f'{tribe.key}_{tier}_life')
            config_dict[tribe.key][tier]['base_attack'] = cols[i * 2].slider('Base attack', 0, 25, (20, 25),
                                                                             key=f'{tribe.key}_{tier}_base_attack')
            config_dict[tribe.key][tier]['num_attacks'] = cols[i * 2].slider('Number of attacks', 0, 10, (1, 3),
                                                                             key=f'{tribe.key}_{tier}_num_attacks')
            config_dict[tribe.key][tier]['evade_prob'] = cols[i * 2].slider('Evade probability', 0.0, 1.0,
                                                                            value=(0.05, 0.2),
                                                                            key=f'{tribe.key}_{tier}_evade_prob')
            config_dict[tribe.key][tier]['hit_prob'] = cols[i * 2].slider('Hit probability', 0.0, 1.0, value=(0.85, 0.95),
                                                                          key=f'{tribe.key}_{tier}_hit_prob')
            config_dict[tribe.key][tier]['heal'] = cols[i * 2].slider('Healing', 0, 10, (1, 3),
                                                                      key=f'{tribe.key}_{tier}_heal')

    tribe_manager.create_armies(config_dict)
