import streamlit as st
from Singleton import Singleton
from random import sample, choice
import itertools
import inflect
import numpy as np

p = inflect.engine()


class BattleManager(metaclass=Singleton):
    def __init__(self):
        self.attacker = None
        self.round_number: int = 0
        self.slots = ['A', 'B', 'C', 'D']
        self.damage_reduction = (0.4, 0.6)  # @TODO: Assign from config
        self.alive_tribes: [] = []
        self.eliminated_tribes: [] = None

    def setup_battle(self, tribe_manager):
        self.round_number = 0
        self.alive_tribes = [tr for tr in tribe_manager.tribes]  # All tribes are alive at the beginning of the battle
        self.eliminated_tribes = []
        print(f'Setting up battle...\nAlive Tribes: {[tr.name for tr in self.alive_tribes]}')

    def get_slots(self, tribe_manager):
        slots = sample(self.slots, len(self.slots))
        for s, t in zip(slots, tribe_manager.tribes):
            t.slot = s

    def get_random_victim(self):
        victims_pool = list(itertools.chain.from_iterable(
            [tr.army.alive_brawlers for tr in self.alive_tribes if tr != self.attacker]))
        return choice(victims_pool) if victims_pool else None

    def wrestle(self, brwlr, victim):
        # a. Se produce el ataque básico, cuyo daño base está determinado en el Brawler
        # Este ataque puede fallar por: Tu probabilidad base de golpear y la prob. de evadir del adversario.
        brwlr.attack(victim)

        # b. El Brawler defensor responde al ataque
        # Se aplican % de acierto y evasión, el daño será de un valor entre 40 y 60% del daño total del atacado.
        if victim.stats['life'] > 0:
            victim.counter_attack(brwlr)

        # TODO c. Se ejecutan las habilidades [...]
        if brwlr.stats['life'] > 0:
            brwlr.execute_abilities(victim, self.alive_tribes)

        # TODO: Gestionar el tema de restar rondas a los buffs / debuffs de todos los brawlers, invulerabilidad, etc.
        # sum(buff['value'] for buff in self.buff['base_attack'])

        # Checks de salud (matar brawlers)
        if brwlr.stats['life'] <= 0:
            print('Atacante ha muerto')
            brwlr.tribe.army.depose_brawler(brwlr)

        if victim.stats['life'] <= 0:
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
        if brwlr.stats['life'] > 0:
            brwlr.healing()

    def main_battle_loop(self, tribe_manager):
        print('Main battle loop starting...')
        cols = st.columns([1, 5])

        while len(self.alive_tribes) > 1:  # Mientras más de una Tribu esté viva
            self.round_number += 1
            print(f'Round {self.round_number}')
            # For each slot
            for tribe in tribe_manager.tribes:  # TODO: Handle better the slots and battle order with BattleManager
                # Init round setup
                self.attacker = tribe

                # 1. Slot Attack
                # 1.1 Select random NFT from attacker army
                brwlr = self.attacker.army.get_random_brawler()  # Seleccionar un NFT random del primer slot
                # 1.2 Select random NFT from rest of armies
                if brwlr is not None:
                    victim = self.get_random_victim()

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
                f"""Average Health: {[(tr.name, int(np.mean([br.stats['life'] for br in tr.army.alive_brawlers]))) for
                                      tr in self.alive_tribes]}""")

            cols[0].markdown("-------------------"), cols[1].markdown("-------------------")

            # TODO 2. Se reubican aleatoriamente las tribus en los slots.

        if len(self.alive_tribes) == 1:
            cols[0].code(f'Event: {"End"}'), cols[1].code(
                f"""Winner Tribe: {[tr.name for tr in self.alive_tribes]}""")

    def reset(self, tribe_manager):
        if tribe_manager.create_armies():
            self.setup_battle(tribe_manager)


# Instantiate Singletons
battle_manager = BattleManager()
