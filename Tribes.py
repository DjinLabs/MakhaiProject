import streamlit as st
from Singleton import Singleton


class TribeManager(metaclass=Singleton):
    def __init__(self):
        self.tribes = None
        self.tribe_names = []

    def create_tribes(self, tribe_names):
        self.tribes = []
        self.tribe_names = tribe_names
        for tribe_name in self.tribe_names:
            self.tribes.append(Tribe(tribe_name))


class Tribe:
    def __init__(self, name):
        self.name = name
        self.slot = None


# Instantiate Singletons
tribe_manager = TribeManager()
