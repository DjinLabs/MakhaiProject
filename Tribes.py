from Singleton import Singleton
import streamlit as st
import random


class TribeManager(metaclass=Singleton):
    def __init__(self):
        self.tribes = [Tribe]
        self.tribe_names = []

    def create_tribes(self, tribes_dict):
        self.tribes = []
        self.tribe_names = tribes_dict.values()
        for tribe_key, tribe_name in tribes_dict.items():
            self.tribes.append(Tribe(tribe_key, tribe_name))

    def create_armies(self, config_dict):
        with st.spinner('Spawning armies...'):
            for tribe in self.tribes:
                tribe.army = ArmyManager(tribe)
                tribe.army.spawn_army(config_dict[tribe.key])


class Tribe:
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.slot = None
        self.army = None


class ArmyManager:
    def __init__(self, tribe: Tribe):
        self.tribe = tribe
        self.brawlers = []

    def spawn_army(self, config_dict):
        """
        @NOTE: Esta función se sustituirá por una que lea de <alguna fuente> los NFTs de cada tribu
        Spawns a new army of brawlers
        :return: Populate the self.brawlers list with new brawlers
        (with the specific combination of Gods, Heroes, Champìons and Soldiers)
        """
        [self.brawlers.append(Soldier(self.tribe, config_dict)) for _ in range(500)]  # Hardcoded
        [self.brawlers.append(Champion(self.tribe, config_dict)) for _ in range(290)]
        [self.brawlers.append(Hero(self.tribe, config_dict)) for _ in range(8)]
        [self.brawlers.append(God(self.tribe, config_dict)) for _ in range(2)]
        random.shuffle(self.brawlers)

    def get_random_brawler(self):
        return random.choice(self.brawlers)


class Brawler:
    def __init__(self, tribe: Tribe, config_dict: dict):
        self.tribe = tribe
        self.base_attack = None
        self.hit_probability = None
        self.evade_probability = None

    def attack(self):
        pass

    def counter_attack(self):
        pass

    def cast_ability(self):
        pass

    def heal(self):
        pass


class God(Brawler):
    def __init__(self, tribe: Tribe, config_dict: dict):
        super().__init__(tribe, config_dict)
        self.base_attack = config_dict['solds']['base_attack']
        self.hit_probability = config_dict['solds']['hit_prob']
        self.evade_probability = config_dict['solds']['evade_prob']


class Hero(Brawler):
    def __init__(self, tribe: Tribe, config_dict: dict):
        super().__init__(tribe, config_dict)
        self.base_attack = config_dict['heroes']['base_attack']
        self.hit_probability = config_dict['heroes']['hit_prob']
        self.evade_probability = config_dict['heroes']['evade_prob']


class Champion(Brawler):
    def __init__(self, tribe: Tribe, config_dict: dict):
        super().__init__(tribe, config_dict)
        self.base_attack = config_dict['champs']['base_attack']
        self.hit_probability = config_dict['champs']['hit_prob']
        self.evade_probability = config_dict['champs']['evade_prob']


class Soldier(Brawler):
    def __init__(self, tribe: Tribe, config_dict: dict):
        super().__init__(tribe, config_dict)
        self.base_attack = config_dict['champs']['base_attack']
        self.hit_probability = config_dict['champs']['hit_prob']
        self.evade_probability = config_dict['champs']['evade_prob']


# Instantiate Singletons
tribe_manager = TribeManager()
