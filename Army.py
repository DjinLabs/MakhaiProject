from Singleton import Singleton


class ArmyManager(metaclass=Singleton):
    def __init__(self):
        self.tribe = None
        self.brawlers = []


class Brawler:
    def __init__(self):
        pass

    def attack(self):
        pass

    def counter_attack(self):
        pass

    def cast_ability(self):
        pass

    def heal(self):
        pass


# Instantiate Singletons
army_manager = ArmyManager()
