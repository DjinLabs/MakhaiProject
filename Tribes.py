TRIBE_NAMES = ['Raperos', 'Punks', 'Otakus', 'Jipis']


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
        self.slot = value
