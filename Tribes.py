from Battle import battle_manager
from Singleton import Singleton
import streamlit as st
import random


class TribeManager(metaclass=Singleton):
    def __init__(self):
        self.tribes = None
        self.tribe_names = None

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
            battle_manager.get_slots(tribe_manager)

    def create_armies(self, config_dict):
        with st.spinner('Spawning armies...'):
            for tribe in self.tribes:
                tribe.spawn_army(config_dict[tribe.key], tribe)


class Tribe:
    def __init__(self, key, name):
        self.key: str = key
        self.name: str = name
        self.slot: str = None
        self.army: Army = Army()
        self.alive: bool = True

    def __del__(self):
        print(f"The TRIBE object is getting DELETED: {self}")

    def spawn_army(self, config_dict, tribe):
        self.army.alive_brawlers = self.army.spawn_army(config_dict, tribe)


class Brawler:
    def __init__(self, config_dict, tier_key, tribe):
        self.tribe: Tribe = tribe
        self.tier_key = tier_key
        self.life = config_dict[self.tier_key]['life']
        self.base_attack = config_dict[self.tier_key]['base_attack']
        self.num_attacks = config_dict[self.tier_key]['num_attacks']
        self.evade_probability = config_dict[self.tier_key]['evade_prob']
        self.hit_probability = config_dict[self.tier_key]['hit_prob']
        self.heal = config_dict[self.tier_key]['heal']

    def attack(self):
        pass

    def counter_attack(self):
        pass

    def cast_ability(self):
        pass

    def heal(self):
        pass


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

    def spawn_army(self, config_dict: dict, tribe: Tribe) -> list:
        """
        @NOTE: Esta función se sustituirá por una que lea de <alguna fuente> los NFTs de cada tribu
        Spawns a new army of brawlers
        :return: Populate the self.brawlers list with new brawlers
        (with the specific combination of Gods, Heroes, Champìons and Soldiers)
        """
        brawlers = []
        [brawlers.append(God(config_dict, st.session_state['GLOBAL_TIERS'][0], tribe)) for _ in
         range(1)]  # Hardcoded (2)
        [brawlers.append(Hero(config_dict, st.session_state['GLOBAL_TIERS'][1], tribe)) for _ in range(2)]  # (8)
        [brawlers.append(Champion(config_dict, st.session_state['GLOBAL_TIERS'][2], tribe)) for _ in range(4)]  # (290)
        [brawlers.append(Soldier(config_dict, st.session_state['GLOBAL_TIERS'][3], tribe)) for _ in range(8)]  # (500)

        random.shuffle(brawlers)
        return brawlers

    def get_random_brawler(self) -> Brawler:
        return random.choice(self.alive_brawlers)


# Instantiate Singletons
tribe_manager = TribeManager()
