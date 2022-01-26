import streamlit as st

from Database import db_manager
from Singleton import Singleton
from random import sample, choice, uniform
import altair as alt
import pandas as pd
import itertools
import numpy as np
import json


class BattleLogger(metaclass=Singleton):
    def __init__(self):
        self.round_log = {}
        self.log = []

    def clear_round(self):
        self.round_log = {}

    def add_round_log(self):
        self.log.append(self.round_log)
        with open('battle.log', 'w') as fout:
            json.dump(battle_logger.log, fout, indent=4)
        self.clear_round()


class Status(metaclass=Singleton):
    def __init__(self):
        self.NOT_SET = -1
        self.READY = 0
        self.RUNNING = 1
        self.PAUSED = 2
        self.FINISHED = 3


# Instantiate
Status = Status()


class BattleManager(metaclass=Singleton):
    def __init__(self):
        self.attacker = None
        self.round_number: int = 0
        self.slots = ['A', 'B', 'C', 'D']
        self.damage_reduction = None
        self.alive_tribes: [] = []
        self.eliminated_tribes: [] = None
        self.status = Status.NOT_SET

    def set_status(self, new_status):
        self.status = new_status

    def setup_battle(self, tribe_manager):
        tribe_manager.create_armies()
        gen_config = list(db_manager.get_general_configuration())[0]
        self.round_number = 0
        self.damage_reduction = gen_config['configs']['damage_reduction']['value']
        self.assign_slots(tribe_manager)
        self.alive_tribes = [tr for tr in tribe_manager.tribes]  # All tribes are alive at the beginning of the battle
        self.eliminated_tribes = []
        print(f'Setting up battle...\nAlive Tribes: {[tr.name for tr in self.alive_tribes]}')
        self.set_status(Status.READY)

    def assign_slots(self, tribe_manager):
        slots = sample(self.slots, len(self.slots))
        for s, t in zip(slots, tribe_manager.tribes):
            t.slot = s

        # Sort list of tribes according to their slot
        tribe_manager.tribes.sort(key=lambda x: x.slot)

    @staticmethod
    def next_slot(tribe_manager):
        for tr in tribe_manager.tribes:
            if tr.slot == 'A':
                tr.slot = 'B'
            elif tr.slot == 'B':
                tr.slot = 'C'
            elif tr.slot == 'C':
                tr.slot = 'D'
            elif tr.slot == 'D':
                tr.slot = 'A'

        # Sort list of tribes according to their slot
        tribe_manager.tribes.sort(key=lambda x: x.slot)

    def get_random_enemies(self, tiers=None, tribes=None, sexes=None, number=1):

        if tiers is None:
            tiers = [0, 1, 2, 3]
        if tribes is None:
            tribes = ['tribe1', 'tribe2', 'tribe3', 'tribe4']
        if sexes is None:
            sexes = [-1, 0, 1]

        victims_pool = list(itertools.chain.from_iterable(
            [tr.army.alive_brawlers for tr in self.alive_tribes if tr != self.attacker]))

        victims = []
        filtered_pool = []

        for victim in victims_pool:
            if victim.tier_key in tiers and victim.tribe.key in tribes and victim.sex in sexes:
                filtered_pool.append(victim)

        if isinstance(number, float):  # If it is percentage, compute absolute value
            number = round(len(filtered_pool) * number)
        elif number == 'all':
            number = len(filtered_pool)

        victims.extend(sample(filtered_pool, min(number, len(filtered_pool))))

        return victims

    def get_random_allies(self, tiers=None, sexes=None, number=1):

        if tiers is None:
            tiers = [0, 1, 2, 3]
        if sexes is None:
            sexes = [-1, 0, 1]

        allies_pool = list(itertools.chain.from_iterable(
            [tr.army.alive_brawlers for tr in self.alive_tribes if tr == self.attacker]))

        allies = []
        filtered_pool = []

        for ally in allies_pool:
            if ally.tier_key in tiers and ally.sex in sexes:
                filtered_pool.append(ally)

        if isinstance(number, float):  # If it is percentage, compute absolute value
            number = round(len(filtered_pool) * number)
        elif number == 'all':
            number = len(filtered_pool)

        allies.extend(sample(filtered_pool, min(number, len(filtered_pool))))

        return allies

    def wrestle(self, brwlr, victim):
        # a. Se produce el ataque básico, cuyo daño base está determinado en el Brawler
        # Este ataque puede fallar por: Tu probabilidad base de golpear y la prob. de evadir del adversario.
        brwlr.attack(victim)

        # b. El Brawler defensor responde al ataque
        # Se aplican % de acierto y evasión, el daño será de un valor entre 40 y 60% del daño total del atacado.
        if victim.stats['life']['value'] > 0:
            victim.counter_attack(brwlr)

        # TODO [preAlpha 0.2] c. Se ejecutan las habilidades [...]
        if brwlr.stats['life']['value'] > 0 and len(
                brwlr.abilities) > 0:  # TODO [preAlpha 0.3] Quitar condicion de no tener abilities xq todos tendran si ahora no tienen es xq no estan metidas en bd
            brwlr.execute_abilities(victim, self.alive_tribes)
            brwlr.update_alter_stat()

        # Checks de salud (matar brawlers)
        if brwlr.stats['life']['value'] <= 0:
            print('Atacante ha muerto')
            brwlr.tribe.army.depose_brawler(brwlr)

        if victim.stats['life']['value'] <= 0:
            print('Víctima ha muerto')
            victim.tribe.army.depose_brawler(victim)

        # Check de unidades (eliminar tribus)
        if len(brwlr.tribe.army.alive_brawlers) <= 0:
            print('La Tribu del atacante ha sido derrotada')
            self.alive_tribes.remove(brwlr.tribe)
            self.eliminated_tribes.append(brwlr.tribe)

        if len(victim.tribe.army.alive_brawlers) <= 0:
            print('La Tribu de la víctima ha sido derrotada')
            self.alive_tribes.remove(victim.tribe)
            self.eliminated_tribes.append(victim.tribe)

        print(f'There are {len(self.alive_tribes)} alive Tribes and {len(self.eliminated_tribes)} eliminated Tribes')

    @staticmethod
    def healing_phase(brwlr):
        if brwlr.stats['life']['value'] > 0:
            brwlr.healing()

    def run_battle(self, tribe_manager, one_round=True):
        if self.status == Status.NOT_SET:
            self.setup_battle(tribe_manager)

        battle_manager.main_battle_loop(tribe_manager, one_round=one_round)


    def main_battle_loop(self, tribe_manager, one_round=True):
        self.set_status(Status.RUNNING)
        print('Main battle loop starting...')

        cols = st.columns([1, 1])  # Reset the columns each round

        # Output variables
        round_header = cols[0].empty()
        cols[1].markdown('#### <span style="color:white">FOO</span>', unsafe_allow_html=True)
        num_brawlers_chart = cols[0].empty()
        avg_life_chart = cols[1].empty()

        while len(self.alive_tribes) > 1 and self.status == Status.RUNNING:  # Mientras más de una Tribu esté viva

            self.round_number += 1
            battle_logger.round_log['round'] = self.round_number

            print(f'Round {self.round_number}')
            # For each slot
            battle_logger.round_log['turn'] = []
            for turn, tribe in enumerate(tribe_manager.tribes):
                # Init round setup
                battle_logger.round_log['turn'].append({'attacker': {}, 'victim': {}})
                self.attacker = tribe
                battle_logger.round_log['turn'][-1]['attacker']['tribe'] = tribe.name

                # 1. Slot Attack
                # 1.1 Select random NFT from attacker army
                brwlr = self.attacker.army.get_random_brawler()  # Seleccionar un NFT random del primer slot

                # 1.2 Select random NFT from rest of armies
                if brwlr is not None:
                    battle_logger.round_log['turn'][-1]['attacker']['brawler'] = brwlr.name
                    victim = self.get_random_enemies(number=1)[0]  # Here always one victim as number=1, so get first

                    if victim is not None:
                        # a. + b. + c. Gestión del reparto de mecos y habilidades
                        battle_logger.round_log['turn'][-1]['victim']['tribe'] = victim.tribe.name
                        battle_logger.round_log['turn'][-1]['victim']['brawler'] = victim.name
                        self.wrestle(brwlr, victim)

                        # d. Se recupera la vida
                        self.healing_phase(brwlr)

            # Output
            round_header = round_header.markdown(f'#### Battle progress - Round {self.round_number}')

            # Plot data
            df = pd.DataFrame(
                {'tribe': pd.Series([tr.name for tr in self.alive_tribes], dtype='category'),
                 'alive_brawlers': [len(tr.army.alive_brawlers) for tr in self.alive_tribes],
                 'average_life': [(int(np.mean([br.stats['life']['value'] for
                                                br in tr.army.alive_brawlers]))) for
                                  tr in self.alive_tribes]},
                columns=['tribe', 'alive_brawlers', 'average_life'])

            # Number of brawlers
            c = alt.Chart(df).mark_bar().encode(
                x=alt.X('tribe', axis=alt.Axis(title='Tribe')),
                y=alt.Y('alive_brawlers', axis=alt.Axis(title='Brawlers'), scale=alt.Scale(domain=[0, 15])),
                # HARDCODED
                tooltip=['alive_brawlers']
            ).properties(
                title='Alive brawlers'
            )
            num_brawlers_chart = num_brawlers_chart.altair_chart(c, use_container_width=True)

            # Average Life
            c = alt.Chart(df).mark_bar().encode(
                x=alt.X('tribe', axis=alt.Axis(title='Tribe')),
                y=alt.Y('average_life', axis=alt.Axis(title='Life'), scale=alt.Scale(domain=[0, 100])),  # HARDCODED
                tooltip=['average_life']
            ).properties(
                title='Average Life'
            )
            avg_life_chart = avg_life_chart.altair_chart(c, use_container_width=True)

            # Log
            battle_logger.add_round_log()

            if one_round:
                self.set_status(Status.PAUSED)

            # Next slot
            self.next_slot(tribe_manager)

        # Json log
        st.json(battle_logger.log[-1])

        with open('battle.log', 'r') as fout:
            st.download_button('Download Battle Log', fout, 'battle.log', 'text/json')

        cols[0].markdown("-------------------"), cols[1].markdown("-------------------")

        if len(self.alive_tribes) == 1:  # TODO: Algo mejor para el fin de la batalla
            self.set_status(Status.FINISHED)
            print(battle_logger.log)
            cols[0].code(f'Event: {"End"}'), cols[1].code(
                f"""Winner Tribe: {[tr.name for tr in self.alive_tribes]}""")


# Instantiate Singletons
battle_manager = BattleManager()
battle_logger = BattleLogger()
