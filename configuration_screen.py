import pymongo
import streamlit as st
import inflect
from Database import db_manager
from Tribes import TribeManager

p = inflect.engine()


def configuration_widget(tribe_manager: TribeManager, tribes_dict: dict):
    st.subheader('Configuration')

    general_config_expander(tribe_manager)

    stats_config_expander(tribe_manager, tribes_dict)

    abilities_config_expander(tribe_manager, tribes_dict)


def general_config_expander(tribe_manager: TribeManager):
    with st.expander('General configuration'):
        with st.form('general_configuration_form'):

            general_configuration, query = db_manager.get_general_configuration()

            for config_name in general_configuration['configs']:
                config = general_configuration['configs'][config_name]
                general_configuration['configs'][config_name]['value'] = st.slider(config['name'], config['min'],
                                                                                   config['max'],
                                                                                   config['value'],
                                                                                   key=config_name)
            if st.form_submit_button('Save'):
                db_manager.config_collection.update_one(query, {"$set": general_configuration})
                # tribe_manager.create_armies() Probando que esto no hace falta porque se llama en el reset de batalla


def stats_config_expander(tribe_manager: TribeManager, tribes_dict: dict):
    with st.expander('Stats configuration'):
        selected_tier = st.selectbox('Select a tier',
                                     [tier.title() for tier in st.session_state['GLOBAL_TIERS'].values()],
                                     key='stats_selected_tier')
        tier = selected_tier.lower()

        cols = st.columns([1, 0.25, 1, 0.25, 1, 0.25, 1])

        for i, tribe in enumerate(tribe_manager.tribes):  # For each Tribe

            cols[i * 2].markdown(f'#### Tribe {i + 1}: {tribe.name[:-1].title()}')  # Tribe names title

            if tier == st.session_state['GLOBAL_TIERS'][0]:  # Gods

                gods = list(db_manager.get_gods())

                cols[i * 2].selectbox(f'"{tribe.name[:-1].title()}" God selection',
                                      [god['name'] for god in gods if god['tribe'] == tribe.key],
                                      key='select_stats_god')

                with cols[i * 2]:
                    with st.form(f'stats_{tribe}_gods_config_form'):
                        for stat_name in gods[i]['stats']:
                            stat = gods[i]['stats'][stat_name]
                            gods[i]['stats'][stat_name]['value'] = st.slider(stat['name'], stat['min'],
                                                                             stat['max'],
                                                                             stat['value'],
                                                                             key=stat_name)

                        if st.form_submit_button('Save'):
                            db_manager.brawlers_collection.update_one({'_id': gods[i]['_id']},
                                                                      {"$set": gods[i]})
                            # tribe_manager.create_armies() Probando que esto no hace falta porque se llama en el reset de batalla

            else:  # Other tiers
                with cols[i * 2]:
                    with st.form(f'stats_{tribe}_others_config_form'):

                        query = {"custom_id": "stats_configuration"}

                        stats_configuration = list(db_manager.config_collection.find(query))[0]

                        for stat_name in stats_configuration['configs'][tier][tribe.key]['stats']:
                            stat = stats_configuration['configs'][tier][tribe.key]['stats'][stat_name]
                            stats_configuration['configs'][tier][tribe.key]['stats'][stat_name][
                                'value'] = st.slider(
                                stat['name'], stat['min'],
                                stat['max'],
                                stat['value'],
                                key=stat_name)

                        if st.form_submit_button('Save'):
                            db_manager.config_collection.update_one(query, {"$set": stats_configuration})
                            # tribe_manager.create_armies() Probando que esto no hace falta porque se llama en el reset de batalla


def abilities_config_expander(tribe_manager: TribeManager, tribes_dict: dict):
    # TODO [preAlpha 0.3]: Entonces en la config no solo será tocable el stat en sí (en este caso por ejemplo el daño) si no también
    #  lo relativo a los targets (en este caso el número de targets), me lo apunto por ahí, y rondas etc etc
    # TODO [preAlpha 0.3]: Añadir número de turnos a las configs de las habilidades con número de turnos e.g., Yaoi

    with st.expander('Abilities configuration'):

        abilities = list(db_manager.get_abilities().sort([
            ('sex', pymongo.DESCENDING),
            ('positive', pymongo.ASCENDING)]))

        selected_tier = st.selectbox('Select a tier',
                                     [tier.title() for tier in st.session_state['GLOBAL_TIERS'].values()],
                                     key='abilities_selected_tier')
        tier_title = selected_tier.lower()
        tier = list(st.session_state['GLOBAL_TIERS'].keys())[list(st.session_state['GLOBAL_TIERS'].values()).index(tier_title)]


        print(tier)

        cols = st.columns([1, 0.25, 1, 0.25, 1, 0.25, 1])

        for i, tribe in enumerate(tribe_manager.tribes):  # For each Tribe

            cols[i * 2].markdown(f'#### Tribe {i + 1}: {tribe.name[:-1].title()}')  # Tribe names title

            if tier == 0:  # Gods
                gods = list(db_manager.get_gods())

                cols[i * 2].selectbox(f'"{tribe.name[:-1].title()}" God selection',
                                      [god['name'] for god in gods if god['tribe'] == tribe.key],
                                      key=f'select_abilities_{tribe.key}_god')

                cols[i * 2].error('Not abilities yet')

            elif tier == 1:  # Heroes
                heroes = list(db_manager.get_heroes())

                cols[i * 2].selectbox(f'"{tribe.name[:-1].title()}" God selection',
                                      [hero['name'] for hero in heroes if hero['tribe'] == tribe.key],
                                      key=f'select_abilities_{tribe.key}_god')

                cols[i * 2].error('Not abilities yet')
            elif tier == 2:  # Champs
                print(tier)
                abilities_config_widget(cols, i, tribe, tier, abilities)

            elif tier == 3:  # Soldiers
                print(tier)
                abilities_config_widget(cols, i, tribe, tier, abilities)

    return None, None


def abilities_config_widget(cols, i, tribe, tier, abilities):
    # TODO: HEMENDIK NOA!
    abs = list(filter(lambda x: x['tier'] == tier and x['tribe'] == tribe.key, abilities))

    for sex, sex_title in zip([-1, 0, 1], ['Unisex', 'Hombres', 'Mujeres']):
        abs_sex = list(filter(lambda x: x['sex'] == sex, abs))
        if len(abs_sex) > 0:
            cols[i * 2].markdown(f' ##### {sex_title}')
        for pos, pos_title in zip([True, False], ['Positivas', 'Negativas']):
            abs_pos = list(filter(lambda x: x['positive'] == pos, abs_sex))
            if len(abs_pos) > 0:
                cols[i * 2].markdown(f' ###### {pos_title.upper()}')

            for ab_tup in abs_pos:
                cols[i * 2].markdown(f'**{ab_tup["name"]}**')
                cols[i * 2].slider('Pick probability', 0.0, 1.0, step=0.01, value=0.1,
                                   key=f'pick_prob_{ab_tup["name"]}_{tribe.key}_{tier}_{sex}')

                for type, stats, effects, target_info, related_brwlrs in zip(ab_tup["type"],
                                                                             ab_tup["stats"],
                                                                             ab_tup["effects"],
                                                                             ab_tup["target_information"],
                                                                             ab_tup["related_brawlers"]):
                    cols[i * 2].text(f'{type}')

