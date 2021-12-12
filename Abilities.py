import streamlit as st
from Singleton import Singleton
from Database import db_manager

from initializations import init_process


class AbilityManager(metaclass=Singleton):
    def __init__(self):
        init_process()
        self.ability_pool: dict = {st.session_state['GLOBAL_TIERS'][0]: [],
                                   st.session_state['GLOBAL_TIERS'][1]: [],
                                   st.session_state['GLOBAL_TIERS'][2]: [],
                                   st.session_state['GLOBAL_TIERS'][3]: [], }


class Ability:
    def __init__(self, name: str, tribe: str, tier: int):
        self.name: str = ""
        self.tribe = None
        self.tier: str = ""
        self.target: [] = None
        self.executed: bool = False  # TODO: Para acciones en diferido (e.g., Cuando mueras, todos los punks ganan Y%

    def get_target(self):
        pass

    def cast_ability(self, *args):
        pass


class DirectDamageAbility:
    def __init__(self, damage: int, base_ability: Ability):
        self.base_ability = base_ability
        self.damage = damage

    def verbose(self):
        print(f'Casting {self.base_ability.name} ability deals {self.damage} damage')

    def get_targets(self, *args):
        self.base_ability.target = []  # Reset target list
        pass  # TODO

    def cast_ability(self, *args):
        self.base_ability.target.append(self.get_targets(args))
        self.verbose()
        self.base_ability.target[0] -= self.damage


class AlterStatAbility:
    """
    Change a Brawler's stat either permanently or as a temporary buff/debuff
    """

    def __init__(self, effect: bool, stat: str, boost, rounds: int, targets: [], base_ability: Ability):
        self.base_ability = base_ability
        self.effect: bool = True
        self.stat: str = stat
        self.boost = boost
        self.rounds: int = rounds
        self.targets: list = []

    def verbose(self):
        print(f'Casting {self.base_ability.name} ability shifting {self.stat} by {self.boost} to {self.targets}')

    def get_targets(self):
        pass

    def cast_ability(self):
        self.verbose()
        for target in self.targets:
            if self.effect:
                target.stats[self.stat] += self.boost
            else:
                target.stats[self.stat] -= self.boost


class DamageAndStatAbility():
    pass


def load_abilities():
    # @TODO: Los datos de las habilidades se cargan desde BD
    abilities = db_manager.abilities_collection.find()

    # Load abilities from BD
    for ability in abilities:
        print(ability)
        1 / 0
        if ability.type == 'DirectDamage':
            ability_manager.ability_pool[st.session_state['GLOBAL_TIERS'][ability['tier']]].append(
                DirectDamageAbility(damage=ability['stats']['damage'],
                                    base_ability=Ability(ability['name'], ability['tribe'], ability['tier']))
            )


# Ability manager
ability_manager = AbilityManager()
