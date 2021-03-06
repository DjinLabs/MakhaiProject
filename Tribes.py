import warnings

from Battle import battle_manager
from Database import db_manager
from Singleton import Singleton
import streamlit as st
import random
import numpy as np
from numpy.random import choice
from Abilities import ability_manager


class TribeManager(metaclass=Singleton):
    def __init__(self):
        self.tribes = None
        self.tribe_names = None

    def create_tribes(self, tribes_dict):
        if self.tribes is None:
            print('Creating tribes...')
            self.tribes = []
            self.tribe_names = tribes_dict.values()
            for tribe_key, tribe_name in tribes_dict.items():
                self.tribes.append(Tribe(tribe_key, tribe_name))

    def create_armies(self):
        with st.spinner('Spawning armies...'):
            for tribe in self.tribes:
                tribe.army.spawn_army(tribe)
        with st.spinner('Loading abilities...'):
            ability_manager.load_abilities()  # TODO: Comprobar si esta llamada es necesaria


class Tribe:
    def __init__(self, key, name):
        self.key: str = key
        self.name: str = name
        self.slot: str = ''
        self.army: Army = Army()
        self.eliminated: bool = False


class Brawler:
    # TODO [logs]: Implementar un toJson para meter al log
    def __init__(self, name: str, tribe: Tribe, tier_key: int, sex: int = -1, *args):
        # General attributes
        self.name: str = name
        self.tribe: Tribe = tribe
        self.tier_key = tier_key
        self.sex: int = sex

        # Buff / Debuff
        # Objeto interno: {'shift': 0, 'rounds': 0}
        # TODO [preAlpha 0.3][Additive]: Creo que una manera de gestionar los cambios aditivos sería añadir un attribute "additive" o
        #  "cummulative" en este objeto (e.g., Refuse Treatment: Tu salud empieza a deteriorarse a X% cada ronda)
        #  obviamente también en la ability así que habrá que cambiar en BD y en AlterStat
        self.buff = {
            'life': [],
            'base_attack': [],
            'num_attacks': [],
            'evade_probability': [],
            'hit_probability': [],
            'heal': [],
        }

        # Invulnerability and Exclusion
        self.invulnerability = {
            # TODO [preAlpha 0.2][Invulnerability]: Check de este attribute por cada vez que se le haga daño a un brawler
            'invulnerable': False,
            'invulnerable_to': [],
            'rounds': 0,
        }
        self.exclusion = {
            # TODO [preAlpha 0.2][Exclusion]: Check de este attribute por cada cosa que se le haga algo un brawler, también para ser elegido como atacante o víctima etc
            'excluded': False,
            'rounds': 0,
        }
        self.skip_abilities = False  # TODO [preAlpha 0.2][Skip]: Check de este attribute por cada habilidad a ejecutar, se resetea al final de ronda

        # Stats
        self.stats = dict()

        # Abilities
        self.abilities = []

    def attack(self, victim):

        success_prob = max(self.stats['hit_probability']['value'] * 1 - victim.stats['evade_probability']['value'], 0)
        succcess = choice([True, False], p=[success_prob, 1 - success_prob])
        if succcess:
            victim.stats['life']['value'] -= self.stats['base_attack']['value']

    def counter_attack(self, victim):
        success_prob = max(self.stats['hit_probability']['value'] * 1 - victim.stats['evade_probability']['value'], 0)
        succcess = choice([True, False], p=[success_prob, 1 - success_prob])
        if succcess:
            victim.stats['life']['value'] -= self.stats['base_attack']['value'] * round(
                random.uniform(battle_manager.damage_reduction[0], battle_manager.damage_reduction[1]), 2)

    def execute_abilities(self, victim, alive_tribes):
        # Pick a random ability

        print(f'EXECUTE ABILITIES: {self.name} with abilities: {[a[0].base_ability.name for a in self.abilities]}')
        ab_tuple = random.choice(
            self.abilities)  # TODO [PreAlpha 0.3][Selection probability]: Aplicar softmax a la probabilidad de pick de las habilidades y tal

        # TODO [PreAlpha 0.2][Disyuntive]: Gestionar las habilidades dobles que son disyuntivas con probabilidades y las que son conjuntivas
        #  Check el ['stats']['probability'], si existe, es disyuntiva y hay que ejecutar una aleatoria basada en las probs

        print(f'Picked Ability: {ab_tuple[0].base_ability.name}')
        self.get_ability_targets(ab_tuple)

        for ability in ab_tuple:
            print(f'Now applying: {ability}')
            ability.cast_ability(victim, alive_tribes)

    def get_ability_targets(self, ab_tuple):

        abilities = [ab for ab in ab_tuple]
        targets_infos = [ab.base_ability.target_info for ab in ab_tuple]

        selves = [ti['self'] for ab, ti in zip(abilities, targets_infos) if ti['self']]
        selves_abilities = [ab for ab, ti in zip(abilities, targets_infos) if ti['self']]

        enemies, enemies_abilities = [], []
        for ab, ti in zip(abilities, targets_infos):
            if isinstance(ti['enemies']['number']['value'], str):
                if ti['enemies']['number']['value'] == 'max':
                    enemies.append(ti['enemies'])
                    enemies_abilities.append(ab)
            else:
                if ti['enemies']['number']['value'] > 0:
                    enemies.append(ti['enemies'])
                    enemies_abilities.append(ab)

        allies, allies_abilities = [], []
        for ab, ti in zip(abilities, targets_infos):
            if isinstance(ti['allies']['number']['value'], str):
                if ti['allies']['number']['value'] == 'max':
                    allies.append(ti['allies'])
                    enemies_abilities.append(ab)
            else:
                if ti['allies']['number']['value'] > 0:
                    allies.append(ti['allies'])
                    enemies_abilities.append(ab)

        # Self
        for a, s in zip(selves_abilities, selves):
            if s:  # It's me!
                a.base_ability.target.append(self)

        # Enemies
        if len(enemies) > 0 and all([e['number']['value'] != 0 for e in enemies]):  # Shared enemies

            if (all(isinstance(e['number']['value'], int) for e in enemies) or all(
                    isinstance(e['number']['value'], float) for e in enemies)) and all(
                e['tiers'] == enemies[0]['tiers'] for e in enemies) and all(
                e['tribes'] == enemies[0]['tribes'] for e in enemies) and all(
                e['sex'] == enemies[0]['sex'] for e in enemies):

                shared_targets = battle_manager.get_random_enemies(tiers=enemies[0]['tiers'],
                                                                   tribes=enemies[0]['tribes'],
                                                                   sexes=enemies[0]['sex'],
                                                                   number=enemies[0]['number']['value'])
                for ab in enemies_abilities:
                    ab.base_ability.target.extend(shared_targets)
            else:
                warnings.warn('ERROR! Mismatching information for abilities targets!'
                              f'Check configs for: {abilities[0].base_abality.name}')

        elif all([e['number']['value'] > 0 for e in enemies]):  # Non-shared enemies

            for ab, e in zip(enemies_abilities, enemies):
                ab.base_ability.target.extend(battle_manager.get_random_enemies(tiers=e['tiers'], tribes=e['tribes'],
                                                                                sexes=e['sex'],
                                                                                number=e['number']['value']))

        # Allies
        if len(allies) > 0 and all([a['number']['value'] != 0 for a in allies]):  # Shared allies

            if (all(isinstance(a['number']['value'], int) for a in allies) or all(
                    isinstance(a['number']['value'], float) for a in allies)) and all(
                a['tiers'] == allies[0]['tiers'] for a in allies) and all(a['sex'] == allies[0]['sex'] for a in allies):

                shared_targets = battle_manager.get_random_allies(tiers=allies[0]['tiers'], sexes=allies[0]['sex'],
                                                                  number=allies[0]['number']['value'])

                for ab in allies_abilities:
                    ab.base_ability.target.extend(shared_targets)
            else:
                warnings.warn('ERROR! Mismatching information for abilities targets!'
                              f'Check configs for: {abilities[0].base_abality.name}')

        elif all([a['number']['value'] > 0 for a in allies]):  # Non-shared allies
            for ab, a in zip(allies_abilities, enemies):
                ab.base_ability.target.extend(battle_manager.get_random_allies(tiers=a['tiers'], sexes=a['sex'],
                                                                               number=a['number']['value']))

    def healing(self):
        self.stats['life']['value'] = min(self.stats['heal']['value'] + self.stats['life']['value'],
                                          self.stats['life']['max'])

    def apply_alter_stat(self, stat, shift, rounds):
        self.stats[stat]['value'] += shift if shift != 'max' else self.stats[stat]['max']
        self.stats[stat]['value'] = min(self.stats[stat]['max'],
                                        max(self.stats[stat]['value'], 0))

        if rounds > 0:  # If temporary buff/debuff hold info on buff attr from Brawler for further revert
            self.buff[stat].append({'shift': shift, 'rounds': rounds})

    def update_alter_stat(self):
        for stat, buffs in self.buff.items():
            for buff in buffs:
                if buff[
                    'rounds'] == -1:  # TODO [preAlpha 0.3][Additive]: Las habilidades "cumulativas" que se aplican todo el rato cada ronda ad infinitum
                    pass
                elif buff['rounds'] == 0:  # Revert the buff
                    self.stats[stat]['value'] -= buff['shift']
                    self.stats[stat]['value'] = min(self.stats[stat]['max'],
                                                    max(self.stats[stat]['value'], 0))
                    buffs.remove(buff)
                else:
                    buff['rounds'] -= 1


class God(Brawler):
    def __init__(self, name: str, tribe: Tribe, tier_key: int, sex: int = -1):
        super().__init__(name, tribe, tier_key, sex)


class Hero(Brawler):
    def __init__(self, name: str, tribe: Tribe, tier_key: int, sex: int = -1):
        super().__init__(name, tribe, tier_key, sex)


class Champion(Brawler):
    def __init__(self, name: str, tribe: Tribe, tier_key: int, sex: int):
        super().__init__(name, tribe, tier_key, sex)
        # self.assign_abilities()

    def pick_abilities(self):
        """
        Los campeones tienen 3 habilidades escogidas aleatoriamente de una base de 9
        de las 3 escogidas, máximo 1 puede ser negativa.
        """
        # print('Picking abilities for Champion: ' + self.name)
        pool = []
        for ab_tup in ability_manager.ability_pool:
            # Shared info in both elems from tuple
            if ab_tup[0].base_ability.sex == self.sex and ab_tup[0].base_ability.tribe == self.tribe.key \
                    and ab_tup[0].base_ability.tier == self.tier_key:
                # print(f'Added {ab_tup[0].base_ability.name} ability to pool')
                pool.append(ab_tup)

        num_negative = 0
        while len(self.abilities) < 3:
            ch = pool[choice(len(pool),
                             replace=False)]  # TODO [PreAlpha 0.3][Pick probability]: Ahora con distribución uniforme, luego usar softmax y args p tal que p=[x,y,z]
            for c in ch:
                c.base_ability.brawler = self
            if ch[0].base_ability.positive or num_negative < 1:
                num_negative += 1
                self.abilities.append(ch)
                pool.remove(ch)
            elif ch[0].base_ability.positive:
                self.abilities.append(ch)
                pool.remove(ch)
            else:  # Habilidad negativa y ya se ha cumplido el cupo
                pool.remove(ch)
        # print(f'Picked abilities for Champion: {self.name}: {[p[0].base_ability.name for p in self.abilities]}')


class Soldier(Brawler):
    def __init__(self, name: str, tribe: Tribe, tier_key: int, sex: int):
        super().__init__(name, tribe, tier_key, sex)
        # self.assign_abilities()

    def pick_abilities(self):
        """
        Los soldados tienen 3 habilidades escogidas aleatoriamente de una base de 10
        de las 3 escogidas, máximo 2 pueden ser negativas.
        """
        # print('Picking abilities for Soldider: ' + self.name)
        pool = []
        for ab_tup in ability_manager.ability_pool:
            # Shared info in both elems from tuple
            if ab_tup[0].base_ability.sex == self.sex and ab_tup[0].base_ability.tribe == self.tribe.key \
                    and ab_tup[0].base_ability.tier == self.tier_key:
                # print(f'Added {ab_tup[0].base_ability.name} ability to pool')
                pool.append(ab_tup)

        num_negative = 0
        while len(self.abilities) < 3:
            ch = pool[choice(len(pool),
                             replace=False)]  # TODO [preAlpha 0.3]: Ahora con distribución uniforme, luego usar softmax y args p tal que p=[x,y,z]
            for c in ch:
                c.base_ability.brawler = self
            if ch[0].base_ability.positive or num_negative < 2:
                num_negative += 1
                self.abilities.append(ch)
                pool.remove(ch)
            elif ch[0].base_ability.positive:
                self.abilities.append(ch)
                pool.remove(ch)
            else:  # Habilidad negativa y ya se ha cumplido el cupo
                pool.remove(ch)
        # print(f'Picked abilities for Soldier: {self.name}: {[p[0].base_ability.name for p in self.abilities]}')


def spawn_heroes(tribe, stats_configuration):
    """
    Spawnear los Heroes según la lista de Heroes de la BD
    """
    brawlers = []
    heroes = list(db_manager.get_heroes(tribe_key=tribe.key))
    stats_configuration = list(db_manager.config_collection.find({"custom_id": "stats_configuration"}))[0]
    config = stats_configuration['configs']['heroes'][tribe.key]['stats']

    for hero in heroes:
        # print(f'Spawning Hero: {hero["name"]} from tribe {st.session_state["GLOBAL_TRIBES_DICT"][hero["tribe"]]}')
        new_hero = Hero(hero['name'], tribe, hero['tier'], hero['sex'])

        # Set stats
        life = random.randint(config['life']['value'][0], config['life']['value'][1])
        new_hero.stats = {
            'life': {'max': life, 'value': life},
            'base_attack': {'max': np.inf, 'value': random.randint(config['base_attack']['value'][0],
                                                                   config['base_attack']['value'][1])},
            'num_attacks': {'max': np.inf, 'value': random.randint(config['num_attacks']['value'][0],
                                                                   config['num_attacks']['value'][1])},

            'evade_probability': {'max': 1.0, 'value': round(
                random.uniform(config['evade_probability']['value'][0],
                               config['evade_probability']['value'][1]), 2)},
            'hit_probability': {'max': 1.0, 'value': round(
                random.uniform(config['hit_probability']['value'][0],
                               config['hit_probability']['value'][1]), 2)},
            'heal': {'max': np.inf, 'value': random.randint(config['heal']['value'][0],
                                                            config['heal']['value'][1])},
        }

        brawlers.append(new_hero)

    return brawlers


class Army:

    def __init__(self):
        self.alive_brawlers = []
        self.casualties = []

    # def __del__(self):
    #     print(f"The ARMY object is getting DELETED: {self}")

    def spawn_army(self, tribe: Tribe):
        """
        @NOTE: Esta función se sustituirá por una que lea de <alguna fuente> los NFTs de cada tribu
        Spawns a new army of brawlers
        :return: Populate the self.brawlers list with new brawlers
        (with the specific combination of Gods, Heroes, Champìons and Soldiers)
        """
        # print(f"Spawning a new army of {tribe.key} -> {tribe.name} in slot {tribe.slot}")

        brawlers = []
        stats_configuration = list(db_manager.config_collection.find({"custom_id": "stats_configuration"}))[0]
        gen_configuration = list(db_manager.get_general_configuration())[0]

        # Spawning the Gods
        brawlers.extend(self.spawn_gods(tribe))
        # Spawning the Heroes
        brawlers.extend(spawn_heroes(tribe, stats_configuration))

        # Spawning the Champions and Soldiers
        brawlers.extend(self.spawn_champions(tribe, stats_configuration, gen_configuration))
        brawlers.extend(self.spawn_soldiers(tribe, stats_configuration, gen_configuration))

        random.shuffle(brawlers)

        self.alive_brawlers = brawlers
        self.casualties = []

    @staticmethod
    def spawn_gods(tribe):
        """
        Spawnear los Gods según la lista de Gods de la BD
        """
        brawlers = []
        gods = list(db_manager.get_gods(tribe_key=tribe.key))

        for god in gods:
            # print(f'Spawning God: {god["name"]} from tribe {st.session_state["GLOBAL_TRIBES_DICT"][god["tribe"]]}')
            new_god = God(god['name'], tribe, god['tier'])

            # Set stats

            new_god.stats = {
                'life': {'max': god['stats']['life']['value'], 'value': god['stats']['life']['value']},
                'base_attack': {'max': np.inf, 'value': god['stats']['base_attack']['value']},
                'num_attacks': {'max': np.inf, 'value': god['stats']['num_attacks']['value']},
                'evade_probability': {'max': 1.0, 'value': god['stats']['evade_probability']['value']},
                'hit_probability': {'max': 1.0, 'value': god['stats']['hit_probability']['value']},
                'heal': {'max': np.inf, 'value': god['stats']['heal']['value']},
            }

            brawlers.append(new_god)

        return brawlers

    @staticmethod
    def spawn_champions(tribe, stats_configuration, gen_configuration):
        """
        Spawnear los Champions y asignar sus habilidades según la pool de habilidades de Champions
        """
        brawlers = []

        config = stats_configuration['configs']['champions'][tribe.key]['stats']

        for i in range(gen_configuration['configs']['num_champions']['value']):

            sex = random.randint(0, 1) if tribe.key != 'tribe1' else -1
            if sex == 0:
                pre_name = tribe.name[:-2].title() + "o"
            elif sex == 1:
                pre_name = tribe.name[:-2].title() + "a"
            else:
                pre_name = tribe.name[:-1].title()

            new_champ = Champion(f"{pre_name}Champion{random.randint(0, 2500)}",
                                 tribe, 2, sex)

            # Set stats
            life = random.randint(config['life']['value'][0], config['life']['value'][1])
            new_champ.stats = {
                'life': {'max': life, 'value': life},
                'base_attack': {'max': np.inf, 'value': random.randint(config['base_attack']['value'][0],
                                                                       config['base_attack']['value'][1])},
                'num_attacks': {'max': np.inf, 'value': random.randint(config['num_attacks']['value'][0],
                                                                       config['num_attacks']['value'][1])},

                'evade_probability': {'max': 1.0, 'value': round(
                    random.uniform(config['evade_probability']['value'][0],
                                   config['evade_probability']['value'][1]), 2)},
                'hit_probability': {'max': 1.0, 'value': round(
                    random.uniform(config['hit_probability']['value'][0],
                                   config['hit_probability']['value'][1]), 2)},
                'heal': {'max': np.inf, 'value': random.randint(config['heal']['value'][0],
                                                                config['heal']['value'][1])},
            }

            new_champ.pick_abilities()

            brawlers.append(new_champ)  # (290)

        return brawlers

    @staticmethod
    def spawn_soldiers(tribe, stats_configuration, gen_configuration):
        """
        Spawnear los Soldiers y asignar sus habilidades según la pool de habilidades de Soldiers
        """
        brawlers = []

        config = stats_configuration['configs']['soldiers'][tribe.key]['stats']

        for i in range(gen_configuration['configs']['num_soldiers']['value']):

            sex = random.randint(0, 1) if tribe.key != 'tribe1' else -1
            if sex == 0:
                pre_name = tribe.name[:-2].title() + "o"
            elif sex == 1:
                pre_name = tribe.name[:-2].title() + "a"
            else:
                pre_name = tribe.name[:-1].title()

            new_soldier = Soldier(f"{pre_name}Soldier{random.randint(0, 5000)}",
                                  tribe, 3, sex)

            # Set stats
            life = random.randint(config['life']['value'][0], config['life']['value'][1])
            new_soldier.stats = {
                'life': {'max': life, 'value': life},
                'base_attack': {'max': np.inf, 'value': random.randint(config['base_attack']['value'][0],
                                                                       config['base_attack']['value'][1])},
                'num_attacks': {'max': np.inf, 'value': random.randint(config['num_attacks']['value'][0],
                                                                       config['num_attacks']['value'][1])},

                'evade_probability': {'max': 1.0, 'value': round(
                    random.uniform(config['evade_probability']['value'][0],
                                   config['evade_probability']['value'][1]), 2)},
                'hit_probability': {'max': 1.0, 'value': round(
                    random.uniform(config['hit_probability']['value'][0],
                                   config['hit_probability']['value'][1]), 2)},
                'heal': {'max': np.inf, 'value': random.randint(config['heal']['value'][0],
                                                                config['heal']['value'][1])},
            }

            new_soldier.pick_abilities()

            brawlers.append(new_soldier)  # (290)

        return brawlers

    def get_random_brawler(self) -> Brawler:
        if len(self.alive_brawlers) > 0:
            return random.choice(self.alive_brawlers)

    def depose_brawler(self, brawler: Brawler):
        # TODO [preAlpha 0.3][Diferido en muerte]: Gestionar acciones en diferido a la muerte del brawler
        #  (i.e., Refuse Treatment: Tu salud empieza a deteriorarse a X% cada ronda.
        #  Cuando mueras, todos los punks ganan Y% en todas las habilidades.)
        self.alive_brawlers.remove(brawler)
        self.casualties.append(brawler)


# Instantiate Singletons
# Tribe Manager
tribe_manager = TribeManager()
