import streamlit as st
from Singleton import Singleton
from random import sample, choice
import itertools
import inflect

p = inflect.engine()


class Round:
    def __init__(self, round_number, attacker):
        self.round_number: int = round_number
        self.attacker = attacker
        self.defender_army = None

    def setup_round(self, tribe_manager):
        self.defender_army = list(itertools.chain.from_iterable(
            [tribe.army.alive_brawlers for tribe in tribe_manager.tribes if tribe != self.attacker]))


class BattleManager(metaclass=Singleton):
    def __init__(self):
        self.slots = ['A', 'B', 'C', 'D']
        self.damage_reduction = (0.4, 0.6)  # @TODO: Assign from config
        self.alive_tribes = []
        self.eliminated_tribes = []

    def get_slots(self, tribe_manager):
        slots = sample(self.slots, len(self.slots))
        for s, t in zip(slots, tribe_manager.tribes):
            t.slot = s
        tribe_manager.tribes.sort(key=lambda x: x.slot)

    @staticmethod
    def get_random_victim(curr_round: Round):
        return choice(curr_round.defender_army)

    def wrestle(self, brwlr, victim):
        # a. Se produce el ataque básico, cuyo daño base está determinado en el Brawler
        # Este ataque puede fallar por: Tu probabilidad base de golpear y la prob. de evadir del adversario.
        brwlr.attack(victim)

        # b. El Brawler defensor responde al ataque
        # Se aplican % de acierto y evasión, el daño será de un valor entre 40 y 60% del daño total del atacado.
        if victim.life > 0:
            victim.counter_attack(brwlr)

        # TODO c. Se ejecutan las habilidades [...]

        # Checks de salud (matar brawlers)
        if brwlr.life <= 0:
            brwlr.tribe.army.depose_brawler(brwlr)

        if victim.life <= 0:
            victim.tribe.army.depose_brawler(victim)

        # Check de unidades (eliminar tribus)
        if brwlr.tribe.army.alive_brawlers <= 0:
            self.alive_tribes.remove(brwlr.tribe)
            self.eliminated_tribes.append(brwlr.tribe)

        if victim.tribe.army.alive_brawlers <= 0:
            self.alive_tribes.remove(victim.tribe)
            self.eliminated_tribes.append(victim.tribe)

    def healing_phase(self, brwlr, victim):
        if brwlr.life > 0:
            brwlr.heal()

    def main_battle_loop(self, tribe_manager):
        cols = st.columns([0.75, 5])

        while len(self.alive_tribes) > 1:  # Mientras más de una Tribu esté viva
            # For each slot
            for round_number, tribe in enumerate(tribe_manager.tribes):
                # Init round setup
                curr_round = Round(round_number=round_number, attacker=tribe)
                curr_round.setup_round(tribe_manager)

                # 1. Slot Attack
                # 1.1 Select random NFT from attacker army
                brwlr = curr_round.attacker.army.get_random_brawler()  # Seleccionar un NFT random del primer slot
                # 1.2 Select random NFT from rest of armies
                victim = self.get_random_victim(curr_round)

                cols[0].code(f'Event: {"Info"}'), cols[1].code(
                    f"""Size of defender army: {len(curr_round.defender_army)}""")
                cols[0].code(f'Event: {1}.{round_number}'), cols[1].code(
                    f"""The first chosen brawler is from "{brwlr.tribe.name}" Tribe and "{brwlr.tier_key.title()}" Tier""")
                cols[0].code(f'Event: {2}.{round_number}'), cols[1].code(
                    f"""The victim is from "{victim.tribe.name}" Tribe and "{victim.tier_key.title()}" Tier""")

                # a. + b. + c. Gestión del reparto de mecos y habilidades
                self.wrestle(brwlr, victim)

                # d. Se recupera la vida
                self.healing_phase(brwlr, victim)

            # TODO 2. Se reubican aleatoriamente las tribus en los slots.


# Instantiate Singletons
battle_manager = BattleManager()
