import configuration_screen
from Battle import battle_manager
from Singleton import Singleton
import streamlit as st
import random
from numpy.random import choice


class TribeManager(metaclass=Singleton):
    def __init__(self):
        self.tribes = None
        self.tribe_names = None
        self.config_dict: dict = {}

    def __del__(self):
        print(f"The TRIBEMANAGER object is getting DELETED: {self}")

    def create_tribes(self, tribes_dict):
        if self.tribes is None:
            print('Creating tribes...')
            self.tribes = []
            self.tribe_names = tribes_dict.values()
            for tribe_key, tribe_name in tribes_dict.items():
                self.tribes.append(Tribe(tribe_key, tribe_name))
            print('Assigning slots...')
            battle_manager.get_slots(tribe_manager)  # @ TODO: Probablemente quitar de aqui

    def create_armies(self):
        with st.spinner('Spawning armies...'):
            for tribe in self.tribes:
                if tribe.key in self.config_dict:
                    tribe.army.spawn_army(self.config_dict[tribe.key], tribe)
                else:
                    st.error(
                        f'No configuration found for Tribes.\nPlease, navigate to the Configuration screen.')
                    return False
        return True



class Tribe:
    def __init__(self, key, name):
        self.key: str = key
        self.name: str = name
        self.slot: str = ''
        self.army: Army = Army()
        self.eliminated: bool = False

    def __del__(self):
        print(f"The TRIBE object is getting DELETED: {self}")


class Brawler:
    def __init__(self, config_dict, tier_key, tribe):
        self.tribe: Tribe = tribe
        self.tier_key = tier_key
        self.life = random.randint(config_dict[self.tier_key]['life'][0], config_dict[self.tier_key]['life'][1])
        self.base_attack = random.randint(config_dict[self.tier_key]['base_attack'][0],
                                          config_dict[self.tier_key]['base_attack'][1])
        self.num_attacks = random.randint(config_dict[self.tier_key]['num_attacks'][0],
                                          config_dict[self.tier_key]['num_attacks'][1])
        self.evade_probability = round(
            random.uniform(config_dict[self.tier_key]['evade_prob'][0], config_dict[self.tier_key]['evade_prob'][1]), 2)
        self.hit_probability = round(
            random.uniform(config_dict[self.tier_key]['hit_prob'][0], config_dict[self.tier_key]['hit_prob'][1]), 2)
        self.heal = random.randint(config_dict[self.tier_key]['heal'][0], config_dict[self.tier_key]['heal'][1])

    def attack(self, victim):
        success_prob = max(self.hit_probability * 1 - victim.evade_probability, 0)
        succcess = choice([True, False], p=[success_prob, 1 - success_prob])
        if succcess:
            victim.life -= self.base_attack

    def counter_attack(self, victim):
        success_prob = max(self.hit_probability * 1 - victim.evade_probability, 0)
        succcess = choice([True, False], p=[success_prob, 1 - success_prob])
        if succcess:
            victim.life -= self.base_attack * round(
                random.uniform(battle_manager.damage_reduction[0], battle_manager.damage_reduction[1]), 2)

    def cast_ability(self):
        pass

    def healing(self):
        self.life += self.heal


class God(Brawler):
    def __init__(self, config_dict: dict, tier_key: str, tribe: Tribe):
        super().__init__(config_dict, tier_key, tribe)


class Hero(Brawler):
    def __init__(self, config_dict: dict, tier_key: str, tribe: Tribe):
        super().__init__(config_dict, tier_key, tribe)


class Champion(Brawler):
    def __init__(self, config_dict: dict, tier_key: str, tribe: Tribe):
        super().__init__(config_dict, tier_key, tribe)


class Soldier(Brawler):
    def __init__(self, config_dict: dict, tier_key: str, tribe: Tribe):
        super().__init__(config_dict, tier_key, tribe)


class Army:

    def __init__(self):
        self.alive_brawlers = []
        self.casualties = []

    def __del__(self):
        print(f"The ARMY object is getting DELETED: {self}")

    def spawn_army(self, config_dict: dict, tribe: Tribe):
        """
        @NOTE: Esta función se sustituirá por una que lea de <alguna fuente> los NFTs de cada tribu
        Spawns a new army of brawlers
        :return: Populate the self.brawlers list with new brawlers
        (with the specific combination of Gods, Heroes, Champìons and Soldiers)
        """
        brawlers = []  # TODO: Añadir a config general el número de cada uno de los tipos de brawlers
        [brawlers.append(God(config_dict, st.session_state['GLOBAL_TIERS'][0], tribe)) for _ in
         range(1)]  # Hardcoded (2)
        [brawlers.append(Hero(config_dict, st.session_state['GLOBAL_TIERS'][1], tribe)) for _ in range(2)]  # (8)
        [brawlers.append(Champion(config_dict, st.session_state['GLOBAL_TIERS'][2], tribe)) for _ in range(4)]  # (290)
        [brawlers.append(Soldier(config_dict, st.session_state['GLOBAL_TIERS'][3], tribe)) for _ in range(8)]  # (500)

        random.shuffle(brawlers)

        self.alive_brawlers = brawlers
        self.casualties = []

    def get_random_brawler(self) -> Brawler:
        if len(self.alive_brawlers) > 0:
            return random.choice(self.alive_brawlers)

    def depose_brawler(self, brawler: Brawler):
        self.alive_brawlers.remove(brawler)
        self.casualties.append(brawler)


# Instantiate Singletons
tribe_manager = TribeManager()
