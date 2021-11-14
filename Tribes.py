from Singleton import Singleton
import streamlit as st


class TribeManager(metaclass=Singleton):
    def __init__(self):
        self.tribes = None
        self.tribe_names = []

    def create_tribes(self, tribe_names):
        self.tribes = []
        self.tribe_names = tribe_names
        for tribe_name in self.tribe_names:
            self.tribes.append(Tribe(tribe_name))
        self.create_armies()

    def create_armies(self):
        for tribe in self.tribes:
            tribe.army = ArmyManager(tribe)
            tribe.army.spawn_army()


class Tribe:
    def __init__(self, name):
        self.name = name
        self.slot = None
        self.army = None


import random
from Tribes import Tribe


class ArmyManager:
    def __init__(self, tribe: Tribe):
        self.tribe = tribe
        self.brawlers = []

    def spawn_army(self):
        """
        @NOTE: Esta función se sustituirá por una que lea de <alguna fuente> los NFTs de cada tribu
        Spawns a new army of brawlers
        :return: Populate the self.brawlers list with new brawlers
        (with the specific combination of Gods, Heroes, Champìons and Soldiers)
        """
        self.brawlers.append(Soldier(self.tribe))

    def get_random_brawler(self):
        return random.choice(self.brawlers)


class Brawler:
    def __init__(self, tribe: Tribe):
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
    def __init__(self, tribe: Tribe):
        super().__init__(tribe)


class Hero(Brawler):
    def __init__(self, tribe: Tribe):
        super().__init__(tribe)


class Champion(Brawler):
    def __init__(self, tribe: Tribe):
        super().__init__(tribe)


class Soldier(Brawler):
    def __init__(self, tribe: Tribe):
        super().__init__(tribe)


# Instantiate Singletons
tribe_manager = TribeManager()
