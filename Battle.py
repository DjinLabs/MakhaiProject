import streamlit as st

from Database import db_manager
from Singleton import Singleton
from random import sample, choice, uniform
import itertools
import inflect
import numpy as np

p = inflect.engine()


class BattleManager(metaclass=Singleton):
    def __init__(self):
        self.attacker = None
        self.round_number: int = 0
        self.slots = ['A', 'B', 'C', 'D']
        self.damage_reduction = None
        self.alive_tribes: [] = []
        self.eliminated_tribes: [] = None

    def setup_battle(self, tribe_manager):
        gen_config = list(db_manager.get_general_configuration())[0]
        self.round_number = 0
        self.damage_reduction = gen_config['configs']['damage_reduction']['value']
        self.alive_tribes = [tr for tr in tribe_manager.tribes]  # All tribes are alive at the beginning of the battle
        self.eliminated_tribes = []
        print(f'Setting up battle...\nAlive Tribes: {[tr.name for tr in self.alive_tribes]}')

    def get_slots(self, tribe_manager):
        slots = sample(self.slots, len(self.slots))
        for s, t in zip(slots, tribe_manager.tribes):
            t.slot = s

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

        if isinstance(number, list):
            if len(number) > 1:
                pct = uniform(number[0], number[1])
            else:
                pct = number[0]
            number = round(len(filtered_pool) * pct)
        print(len(filtered_pool), number)
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

        if isinstance(number, list):
            if len(number) > 1:
                pct = uniform(number[0], number[1])
            else:
                pct = number[0]
            number = round(len(filtered_pool) * pct)
        print(len(filtered_pool), number)
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

        # TODO [preAlpha 0.2]: Gestionar el tema de restar rondas a los buffs / debuffs de todos los brawlers, invulerabilidad, etc.
        # sum(buff['value'] for buff in self.buff['base_attack'])

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

    def main_battle_loop(self, tribe_manager):
        print('Main battle loop starting...')
        cols = st.columns([1, 5])

        while len(self.alive_tribes) > 1:  # Mientras más de una Tribu esté viva
            self.round_number += 1
            print(f'Round {self.round_number}')
            # For each slot
            for tribe in tribe_manager.tribes:  # TODO [preAlpha 0.3]: Handle better the slots and battle order with BattleManager
                # Init round setup
                self.attacker = tribe

                # 1. Slot Attack
                # 1.1 Select random NFT from attacker army
                brwlr = self.attacker.army.get_random_brawler()  # Seleccionar un NFT random del primer slot
                # 1.2 Select random NFT from rest of armies
                if brwlr is not None:
                    victim = self.get_random_enemies(number=1)[0]  # Here always one victim as number=1, so get first

                    if victim is not None:
                        # a. + b. + c. Gestión del reparto de mecos y habilidades
                        self.wrestle(brwlr, victim)

                        # d. Se recupera la vida
                        self.healing_phase(brwlr)

            # Output
            cols[0].code(f"""Round {self.round_number}: Status""")
            cols[1].code(
                f"""Alive Tribes & Brawlers: {[(tr.name, len(tr.army.alive_brawlers)) for tr in self.alive_tribes]}""")

            cols[0].code(f"""Round {self.round_number}: Info""")
            cols[1].code(
                f"""Average Health: {[(tr.name, int(np.mean([br.stats['life']['value'] for
                                                             br in tr.army.alive_brawlers]))) for
                                      tr in self.alive_tribes]}""")

            cols[0].markdown("-------------------"), cols[1].markdown("-------------------")

            # TODO [preAlpha 0.3]. Se reubican aleatoriamente las tribus en los slots.

        if len(self.alive_tribes) == 1:
            cols[0].code(f'Event: {"End"}'), cols[1].code(
                f"""Winner Tribe: {[tr.name for tr in self.alive_tribes]}""")

    def reset(self, tribe_manager):
        if tribe_manager.create_armies():
            self.setup_battle(tribe_manager)


# Instantiate Singletons
battle_manager = BattleManager()
