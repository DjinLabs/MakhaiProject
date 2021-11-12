import streamlit as st
from random import sample


class TribeManager:
    def __init__(self):
        self.tribes = []
        self.tribe_names = []
        self._slots = ['A', 'B', 'C', 'D']

    def create_tribes(self, tribe_names):
        self.tribe_names = tribe_names
        for tribe_name in self.tribe_names:
            self.tribes.append(Tribe(tribe_name))

    def get_slots(self):
        slots = sample(self._slots, len(self._slots))
        for s, t in zip(slots, self.tribes):
            t.slot = s
        self.tribes.sort(key=lambda x: x.slot)

    @property
    def slots(self):
        return self._slots

class Tribe:
    def __init__(self, name):
        self._name = name
        self._slot = None

    @property
    def name(self):
        return self._name

    @property
    def slot(self):
        return self._slot

    @slot.setter
    def slot(self, value):
        self._slot = value




