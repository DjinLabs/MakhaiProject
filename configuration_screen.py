import random
import warnings
import pymongo
import streamlit as st
import inflect
from Database import db_manager
from Tribes import TribeManager

p = inflect.engine()


def configuration_widget(tribe_manager: TribeManager, tribes_dict: dict):
    st.subheader('Configuration')

    general_config_expander()

    stats_config_expander(tribe_manager)

    abilities_config_expander(tribe_manager)


def general_config_expander():
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


def stats_config_expander(tribe_manager: TribeManager):
    with st.expander('Stats configuration'):
        selected_tier = st.selectbox('Select a tier',
                                     [tier.title() for tier in st.session_state['GLOBAL_TIERS'].values()],
                                     key='stats_selected_tier')
        tier = selected_tier.lower()

        cols = st.columns([1, 1, 1, 1])

        for i, tribe in enumerate(tribe_manager.tribes):  # For each Tribe

            cols[i].markdown(f'#### Tribe {i + 1}: {tribe.name[:-1].title()}')  # Tribe names title

            if tier == st.session_state['GLOBAL_TIERS'][0]:  # Gods

                gods = list(db_manager.get_gods())

                cols[i].selectbox(f'"{tribe.name[:-1].title()}" God selection',
                                  [god['name'] for god in gods if god['tribe'] == tribe.key],
                                  key='select_stats_god')

                with cols[i]:
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

            else:  # Other tiers
                with cols[i]:
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


def abilities_config_expander(tribe_manager: TribeManager):
    with st.expander('Abilities configuration'):

        abilities = list(db_manager.get_abilities().sort([
            ('sex', pymongo.DESCENDING),
            ('positive', pymongo.ASCENDING)]))

        cols = st.columns(2)

        selected_tribe = cols[0].selectbox('Select a tier',
                                           [tr.name for tr in tribe_manager.tribes],
                                           key=f'select_tribe')
        tribe = [tr for tr in tribe_manager.tribes if tr.name == selected_tribe][0]

        selected_tier = cols[1].selectbox('Select a tier',
                                          [tier.title() for tier in st.session_state['GLOBAL_TIERS'].values()],
                                          key='abilities_selected_tier')

        tier_title = selected_tier.lower()
        tier = list(st.session_state['GLOBAL_TIERS'].keys())[
            list(st.session_state['GLOBAL_TIERS'].values()).index(tier_title)]

        if tier == 0:  # Gods
            with st.form(f'abilities_config_form_{tribe.key}'):
                gods = list(db_manager.get_gods())

                st.selectbox(f'"{tribe.name[:-1].title()}" God selection',
                             [god['name'] for god in gods if god['tribe'] == tribe.key],
                             key=f'select_abilities_{tribe.key}_god')

                st.error('No abilities yet')

                if st.form_submit_button('Save'):
                    # TODO: Save GODS abilities changes
                    pass

        elif tier == 1:  # Heroes
            with st.form(f'abilities_config_form_{tribe.key}'):
                heroes = list(db_manager.get_heroes())

                st.selectbox(f'"{tribe.name[:-1].title()}" God selection',
                             [hero['name'] for hero in heroes if hero['tribe'] == tribe.key],
                             key=f'select_abilities_{tribe.key}_god')

                st.error('No abilities yet')

                if st.form_submit_button('Save'):
                    # TODO: Save HEROES abilities changes
                    pass

        elif tier == 2:  # Champs

            abilities_config_widget(tribe_manager, tribe, tier, abilities)


        elif tier == 3:  # Soldiers
            abilities_config_widget(tribe_manager, tribe, tier, abilities)

    return None, None


def abilities_config_widget(tribe_manager, tribe, tier, abilities):
    stats_dict = {'life': 'Life', 'base_attack': 'Base attack', 'num_attacks': 'Number of attacks',
                  'evade_probability': 'Evade probability', 'hit_probability': 'Hit probability',
                  'heal': 'Heal'}
    sex_dict = {-1: 'Agénero', 0: 'Hombre', 1: 'Mujer'}
    sex_dict_inv = {v: k for k, v in sex_dict.items()}
    pos_dict = {0: 'Negativa', 1: 'Positiva'}

    abs = list(sorted(sorted(list(filter(lambda x: x['tier'] == tier and x['tribe'] == tribe.key, abilities)),
                             key=lambda x: x['positive'], reverse=True), key=lambda x: x['sex']))

    selected_ab = st.selectbox('Select an ability',
                               [f'{a["name"]} ({sex_dict[a["sex"]]} - {pos_dict[a["positive"]]})' for a in
                                abs], key=f'select_ability_{tribe.key}')

    ab_tup = [a for a in abs if f'{a["name"]} ({sex_dict[a["sex"]]} - {pos_dict[a["positive"]]})' == selected_ab][0]

    ab_id = f'{ab_tup["name"]}_{tribe.key}_{tier}_{ab_tup["sex"]}'

    st.markdown(f'##### General')
    with st.form(f'abilities_config_form_{tribe.key}'):
        ab_tup['pick_probability'] = st.slider('Pick probability', 0.0, 1.0, step=0.01, value=0.1, key=f'pick_prob_{ab_id}')
        if st.form_submit_button('Save'):
            db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})

    submitted = False
    for k, (type, stats, effects, target_info, related_brwlrs) in enumerate(zip(ab_tup["type"],
                                                                                ab_tup["stats"],
                                                                                ab_tup["effects"],
                                                                                ab_tup["target_information"],
                                                                                ab_tup["related_brawlers"])):
        st.markdown(f'##### Base ability {k + 1}: {type}')  # Ability name title

        # Stats

        st.markdown('###### Stats:')

        if type == 'AlterStat':

            cols = st.columns(3)

            with cols[0]:
                with st.form(f'stat_config_form_{k}_{ab_id}'):
                    if submitted:
                        st.experimental_rerun()
                        submitted = False

                    effects['stat'] = st.selectbox('Stat', options=stats_dict.values(),
                                                   index=list(stats_dict.keys()).index(effects['stat']),
                                                   key=f'stat_{k}_{ab_id}')

                    effects['stat'] = [key for key, val in stats_dict.items() if val == effects['stat']][0]

                    if st.form_submit_button('Save'):

                        ab_tup['effects'][k]['stat'] = effects['stat']
                        if effects['stat'] == 'life' or effects['stat'] == 'base_attack' or effects['stat'] == 'heal':
                            ab_tup['stats'][k]['shift'] = 10
                        elif effects['stat'] == 'num_attacks':
                            ab_tup['stats'][k]['shift'] = 1
                        elif effects['stat'] == 'hit_probability' or effects['stat'] == 'evade_probability':
                            ab_tup['stats'][k]['shift'] = 0.1

                        print("Storing to BD:" + effects['stat'], ab_tup['stats'][k]['shift'])
                        db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})
                        submitted = True

            with cols[1]:
                if submitted:
                    st.experimental_rerun()
                    submitted = False

                with st.form(f'shift_config_form_{k}_{ab_id}'):

                    if effects['stat'] == 'life' or effects['stat'] == 'base_attack' or effects['stat'] == 'heal':
                        stats['shift'] = st.select_slider('Shift', options=list(range(-100, 0)) + list(range(1, 101)),
                                                          value=float(stats['shift']) if effects['stat'] == effects[
                                                              'stat'] else 10,
                                                          key=f'shift_{k}_{ab_id}')
                    elif effects['stat'] == 'num_attacks':
                        stats['shift'] = st.select_slider('Shift', options=list(range(-3, 0)) + list(range(1, 4)),
                                                          value=float(stats['shift']) if effects['stat'] == effects[
                                                              'stat'] else 1,
                                                          key=f'shift_{k}_{ab_id}')
                    elif effects['stat'] == 'hit_probability' or effects['stat'] == 'evade_probability':
                        stats['shift'] = st.slider('Shift', -1.0, 1.0, step=0.01,
                                                   value=float(stats['shift']) if effects['stat'] == effects[
                                                       'stat'] else 0.1,
                                                   key=f'shift_{k}_{ab_id}')

                    if st.form_submit_button('Save'):
                        db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})
                        submitted = True

            with cols[2]:
                if submitted:
                    st.experimental_rerun()
                    submitted = False

                with st.form(f'rounds_config_form_{k}_{ab_id}'):
                    stats['rounds'] = st.select_slider('Rounds', options=list(range(1, 20)) + ['All'],
                                                       value=stats['rounds'] if stats['rounds'] != -1 else 'All',
                                                       key=f'rounds_{k}_{ab_id}')
                    if stats['rounds'] == 'All':
                        stats['rounds'] = -1
                    if st.form_submit_button('Save'):
                        db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})
                        submitted = True

        elif type == 'DirectDamage':
            if submitted:
                st.experimental_rerun()
                submitted = False

            with st.form(f'damage_config_form_{k}_{ab_id}'):

                stats['damage'] = st.select_slider('Damage', options=list(range(-100, 0)) + list(range(1, 101)),
                                                   value=float(stats['damage']),
                                                   key=f'damage_{k}_{ab_id}')

                if st.form_submit_button('Save'):
                    db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})
                    submitted = True
        elif type == 'Kill':
            pass

        elif type == 'Exclusion' or type == 'Skip' or type == 'Invulnerability':
            if submitted:
                st.experimental_rerun()
                submitted = False

            with st.form(f'rounds_config_form_{k}_{ab_id}'):
                stats['rounds'] = st.select_slider('Rounds', options=list(range(1, 20)) + ['All'],
                                                   value=stats['rounds'] if stats['rounds'] != -1 else 'All',
                                                   key=f'rounds_{k}_{ab_id}')
                if stats['rounds'] == 'All':
                    stats['rounds'] = -1
                if st.form_submit_button('Save'):
                    db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})
                    submitted = True

        else:
            warnings.warn(f"Ability type not implemented: {type}")

        # Targets

        st.markdown('###### Target information:')

        enemies_aux = target_info['enemies']
        allies_aux = target_info['allies']

        select_target = st.selectbox('Target type', [k.title() for k in target_info.keys()], key=f'target_{k}_{ab_id}')

        if select_target == 'Enemies' or select_target == 'Allies':
            abs = st.checkbox('Select number of targets with absolute value',
                              value=len(target_info['enemies']['number']['range']) == 0, key=f'abs_{k}_{ab_id}')

        if select_target != 'Self':

            target_info['self'] = False

            with st.form(f'target_info_form_{k}_{ab_id}'):
                if submitted:
                    st.experimental_rerun()
                    submitted = False

                if select_target == 'Enemies':

                    target_info['allies'] = allies_aux

                    st.markdown('**Enemies**')
                    selected_tribes = st.multiselect('Tribes', [t.name.title() for t in tribe_manager.tribes],
                                                     default=[st.session_state['GLOBAL_TRIBES_DICT'][t] for t in
                                                              target_info['enemies']['tribes']],
                                                     key=f'enemies_tribes_{k}_{ab_id}')
                    idxs = [list(st.session_state['GLOBAL_TRIBES_DICT'].values()).index(s) for s in selected_tribes]
                    selected_tribes = [list(st.session_state['GLOBAL_TRIBES_DICT'].keys())[i] for i in idxs]
                    target_info['enemies']['tribes'] = selected_tribes

                    selected_tiers = st.multiselect('Tiers', [t.title() for t in
                                                              st.session_state['GLOBAL_TIERS'].values()],
                                                    default=[st.session_state['GLOBAL_TIERS'][t].title() for t in
                                                             target_info['enemies']['tiers']],
                                                    key=f'enemies_tiers_{k}_{ab_id}')

                    idxs = [list(st.session_state['GLOBAL_TIERS'].values()).index(t.lower()) for t in selected_tiers]
                    target_info['enemies']['tiers'] = idxs

                    print(target_info['enemies']['sex'])
                    selected_sex = st.multiselect('Sex', sex_dict.values(),
                                                  default=[sex_dict[s] for s in target_info['enemies']['sex']],
                                                  key=f'enemies_sex_{k}_{ab_id}')

                    idxs = [sex_dict_inv[s] for s in selected_sex]
                    target_info['enemies']['sex'] = idxs

                    st.text('Number')

                    if abs:
                        options = list(range(1, 101)) + ['All']
                        target_info['enemies']['number']['value'] = st.select_slider('Number of enemies',
                                                                                     options=options,
                                                                                     value=
                                                                                     target_info['enemies']['number']
                                                                                     ['value'] if
                                                                                     target_info['enemies']['number']
                                                                                     ['value'] != 0 else 1,
                                                                                     key=f'enemies_number_{k}_{ab_id}')
                    else:
                        if len(target_info['enemies']['number']['range']) == 0:
                            min_value = 0.01
                            max_value = 1.0
                            value = (0.03, 0.06)
                        else:
                            min_value = int(target_info['enemies']['number']['range'][0])
                            max_value = int(target_info['enemies']['number']['range'][1])
                            value = int(target_info['enemies']['number']['value'])

                        target_info['enemies']['number']['range'] = st.slider('Number of enemies', min_value=min_value,
                                                                              max_value=max_value,
                                                                              value=value,
                                                                              key=f'enemies_number_{k}_{ab_id}')
                        target_info['enemies']['number']['value'] = round(random.uniform(
                            target_info['enemies']['number']['range'][0], target_info['enemies']['number']['range'][1]),
                            2)

                elif select_target == 'Allies':

                    target_info['enemies'] = enemies_aux

                    st.markdown('**Allies**')

                    selected_tiers = st.multiselect('Tiers', [t.title() for t in
                                                              st.session_state['GLOBAL_TIERS'].values()],
                                                    default=[st.session_state['GLOBAL_TIERS'][t].title() for t in
                                                             target_info['allies']['tiers']],
                                                    key=f'allies_tiers_{k}_{ab_id}')

                    idxs = [list(st.session_state['GLOBAL_TIERS'].values()).index(t.lower()) for t in selected_tiers]
                    target_info['allies']['tiers'] = idxs

                    print(target_info['allies']['sex'])
                    selected_sex = st.multiselect('Sex', sex_dict.values(),
                                                  default=[sex_dict[s] for s in target_info['allies']['sex']],
                                                  key=f'allies_sex_{k}_{ab_id}')

                    idxs = [sex_dict_inv[s] for s in selected_sex]
                    target_info['allies']['sex'] = idxs

                    st.text('Number')

                    if abs:
                        options = list(range(1, 101)) + ['All']
                        target_info['allies']['number']['value'] = st.select_slider('Number of allies',
                                                                                    options=options,
                                                                                    value=
                                                                                    target_info['allies']['number']
                                                                                    ['value'] if
                                                                                    target_info['allies']['number']
                                                                                    ['value'] != 0 else 1,
                                                                                    key=f'allies_number_{k}_{ab_id}')
                    else:
                        if len(target_info['allies']['number']['range']) == 0:
                            min_value = 0.01
                            max_value = 1.0
                            value = (0.03, 0.06)
                        else:
                            min_value = int(target_info['allies']['number']['range'][0])
                            max_value = int(target_info['allies']['number']['range'][1])
                            value = int(target_info['allies']['number']['value'])

                        target_info['allies']['number']['range'] = st.slider('Number of allies', min_value=min_value,
                                                                             max_value=max_value,
                                                                             value=value,
                                                                             key=f'allies_number_{k}_{ab_id}')
                        target_info['allies']['number']['value'] = round(random.uniform(
                            target_info['allies']['number']['range'][0], target_info['allies']['number']['range'][1]),
                            2)

                if st.form_submit_button('Save'):
                    db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})
                    submitted = True

        else:
            target_info['self'] = True
            save = st.button('Save', key=f'target_info_save_button_{k}_{ab_id}')
            if save:
                db_manager.abilities_collection.update_one({"_id": ab_tup["_id"]}, {"$set": ab_tup})

            st.markdown('----')
