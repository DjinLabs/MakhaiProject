from Singleton import Singleton
from random import sample

from Tribes import tribe_manager


class BattleManager(metaclass=Singleton):
    def __init__(self):
        self.slots = ['A', 'B', 'C', 'D']

    def get_slots(self):
        slots = sample(self.slots, len(self.slots))
        for s, t in zip(slots, tribe_manager.tribes):
            t.slot = s
        tribe_manager.tribes.sort(key=lambda x: x.slot)


# Instantiate Singletons
battle_manager = BattleManager()
