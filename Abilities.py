import warnings
from Battle import battle_manager
from Singleton import Singleton
from Database import db_manager

from initializations import init_process


class AbilityManager(metaclass=Singleton):
    def __init__(self):
        init_process()
        self.ability_pool: [] = []
        self.load_abilities()

    def load_abilities(self):
        print("Loading Abilities...")

        abilities = db_manager.get_abilities()

        # Load abilities from BD
        for ability in abilities:

            # print(f"Loading {ability['name']} ability from Tier {ability['tier']} of {ability['tribe']} Tribe")
            new_ability = []
            for ab_type, stats, effects, target_info, related_brwlrs in zip(ability['type'], ability['stats'],
                                                                            ability['effects'],
                                                                            ability['target_information'],
                                                                            ability['related_brawlers']):

                if ab_type == 'AlterStat':

                    base_ability = Ability(name=ability['name'], sex=ability['sex'],
                                           positive=ability['positive'], tribe=ability['tribe'],
                                           tier=ability['tier'], target_info=target_info)

                    new_ability.append(
                        AlterStatAbility(shift=stats['shift'], stat=effects['stat'], rounds=stats['rounds'],
                                         base_ability=base_ability), )

                elif ab_type == 'DirectDamage':
                    base_ability = Ability(name=ability['name'], sex=ability['sex'],
                                           positive=ability['positive'], tribe=ability['tribe'],
                                           tier=ability['tier'], target_info=target_info)

                    new_ability.append(
                        DirectDamageAbility(damage=stats['damage'], base_ability=base_ability), )

                elif ab_type == 'Kill':
                    base_ability = Ability(name=ability['name'], sex=ability['sex'],
                                           positive=ability['positive'], tribe=ability['tribe'],
                                           tier=ability['tier'], target_info=target_info)

                    new_ability.append(
                        KillAbility(base_ability=base_ability), )

                elif ab_type == 'Exclusion':
                    base_ability = Ability(name=ability['name'], sex=ability['sex'],
                                           positive=ability['positive'], tribe=ability['tribe'],
                                           tier=ability['tier'], target_info=target_info)

                    new_ability.append(
                        ExclusionAbility(rounds=stats['rounds'], base_ability=base_ability), )

                elif ab_type == 'Skip':
                    base_ability = Ability(name=ability['name'], sex=ability['sex'],
                                           positive=ability['positive'], tribe=ability['tribe'],
                                           tier=ability['tier'], target_info=target_info)

                    new_ability.append(
                        SkipAbility(rounds=stats['rounds'], base_ability=base_ability), )

                elif ab_type == 'Invulnerability':
                    base_ability = Ability(name=ability['name'], sex=ability['sex'],
                                           positive=ability['positive'], tribe=ability['tribe'],
                                           tier=ability['tier'], target_info=target_info)

                    new_ability.append(
                        InvulnerabilityAbility(rounds=stats['rounds'], invulnerable_to=stats['rounds'],
                                               base_ability=base_ability), )
                else:
                    warnings.warn(f"Ability type not implemented: {ab_type}")

            self.ability_pool.append(new_ability)


class Ability:
    def __init__(self, name: str, sex: int, positive: bool, tribe: str, tier: int, target_info: dict):
        self.name: str = name
        self.sex: int = sex
        self.positive: bool = positive
        self.tribe: str = tribe
        self.tier: int = tier
        self.target_info: dict = target_info
        self.executed: bool = False  # TODO [PreAlpha 0.3][Diferido]: Para acciones en diferido (e.g., Cuando mueras, todos los punks ganan Y%
        self.brawler = None
        self.target = []

    # def get_target(self, victim, alive_tribes): REMOVERRRRRRRRRRRR
    #     """
    #     At battle loop, with the self.target_info information
    #     :return: self.target correctly filled
    #     """
    #     print(self.target_info)
    #     for target in self.target_info:
    #         print(target)
    #         if target['self']:  # It's me!
    #             self.target.append(self.brawler)
    #         else:
    #             print(target['enemies'])
    #             if target['enemies']['number']['value'] != 0:  # Get enemies
    #                 self.target = battle_manager.get_random_enemies(tiers=target['enemies']['tiers'],
    #                                                                 tribes=target['enemies']['tribes'],
    #                                                                 sexes=target['enemies']['sex'],
    #                                                                 number=target['enemies']['number'])
    #             if target['allies']['number']['value'] != 0:  # Get allies
    #                 self.target = battle_manager.get_random_allies(tiers=target['allies']['tiers'],
    #                                                                sexes=target['allies']['sex'],
    #                                                                number=target['allies']['number'])

    def cast_ability(self):
        pass


class DirectDamageAbility:
    def __init__(self, damage: int, base_ability: Ability):
        self.base_ability = base_ability
        self.damage = damage

    def verbose(self):
        print(f'Casting {self.base_ability.name} ability deals {self.damage} damage '
              f'to {[t.name for t in self.base_ability.target]}')

    def cast_ability(self, victim, alive_tribes):
        self.verbose()
        for target in self.base_ability.target:
            target.stats['life']['value'] -= self.damage
        self.base_ability.target = []  # Clear targets


class AlterStatAbility:
    """
    Change a Brawler's stat either permanently or as a temporary buff/debuff
    """

    def __init__(self, shift, stat: str, rounds: int, base_ability: Ability):
        self.base_ability = base_ability
        self.shift = shift
        self.stat: str = stat
        self.rounds: int = int(rounds)

    def verbose(self):
        print(
            f'Casting {self.base_ability.name} ability shifting {self.stat} by {self.shift} '
            f'to {[t.name for t in self.base_ability.target]}')

    def cast_ability(self, victim, alive_tribes):
        self.verbose()
        for target in self.base_ability.target:
            target.apply_alter_stat(self.stat, self.shift, self.rounds)

        self.base_ability.target = []  # Clear targets


class KillAbility:
    def __init__(self, base_ability: Ability):
        self.base_ability = base_ability

    def verbose(self):
        print(f'Casting {self.base_ability.name} ability kills {[t.name for t in self.base_ability.target]}')

    def cast_ability(self, victim, alive_tribes):
        self.verbose()
        for target in self.base_ability.target:
            target.stats['life']['value'] = 0

        self.base_ability.target = []  # Clear targets


class ExclusionAbility:
    """
    El brawler targeteado no puede participar ni recibir ningún efecto (ni positivo ni negativo) por el número de rondas
    """

    def __init__(self, rounds: int, base_ability: Ability):
        self.base_ability = base_ability
        self.rounds: int = rounds

    def verbose(self):
        print(f'Casting {self.base_ability.name} ability excludes {[t.name for t in self.base_ability.target]} for'
              f' {self.rounds} rounds')

    def cast_ability(self, victim, alive_tribes):
        self.verbose()
        for target in self.base_ability.target:
            target.exclusion['excluded'] = True
            target.exclusion['rounds'] = self.rounds
        self.base_ability.target = []  # Clear targets


class SkipAbility:
    """
    El brawler targeteado no ejecuta el resto de habilidades en caso de que esta no sea la última
    """

    def __init__(self, rounds: int, base_ability: Ability):
        self.base_ability = base_ability
        self.rounds: int = rounds

    def verbose(self):
        print(
            f'Casting {self.base_ability.name} ability skips next abiilities '
            f'for {[t.name for t in self.base_ability.target]}')

    def cast_ability(self, victim, alive_tribes):
        self.verbose()
        for target in self.base_ability.target:
            target.skip_abilities = True
        self.base_ability.target = []  # Clear targets


class InvulnerabilityAbility:
    """
    El brawler targeteado no puede recibir daño durante el número de rondas indicado
    """

    def __init__(self, rounds: int, invulnerable_to: list, base_ability: Ability):
        self.base_ability = base_ability
        self.rounds: int = rounds
        self.invulnerable_to: list = invulnerable_to

    def verbose(self):
        print(f'Casting {self.base_ability.name} ability invulnerates {[t.name for t in self.base_ability.target]} for'
              f' {self.rounds} rounds')

    def cast_ability(self, victim, alive_tribes):
        self.verbose()
        for target in self.base_ability.target:
            target.invulnerability['invulnerable'] = True
            target.invulnerability['rounds'] = self.rounds
            target.invulnerability['invulnerable_to'] = self.invulnerable_to
        self.base_ability.target = []  # Clear targets


# Ability manager
ability_manager = AbilityManager()
