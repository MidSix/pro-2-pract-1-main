# Parte 3
import sys
import importlib
from unit import *
from civilization import *
import pandas as pd
from typing import Union #Simplemente sirve para decir que una función puede devolver distintos tipos de datos en función de las condiciones que se cumplan

"""
Authors:
Sebastián David Moreno Expósito; sebastian.exposito@udc.es
Xoel Sánchez Dacoba; xoel.sanchez.dacoba@udc.es
"""
def create_units(civilization_object: Civilization, Workers: int = 0, Archers: int = 0, Cavalries: int = 0, Infantries: int = 0) -> None:
    """
    Crea unidades para una civilización dada.

    Parameters
    ----------
    civilization_object : Unit
        La civilización para crear unidades.
    Workers : int, opcional
        Número de trabajadores a crear (por defecto es 0).
    Archers : int, opcional
        Número de arqueros a crear (por defecto es 0).
    Cavalries : int, opcional
        Número de caballerías a crear (por defecto es 0).
    Infantries : int, opcional
        Número de infanterías a crear (por defecto es 0).

    Returns
    -------
    None
    """
    for worker in range(Workers):
        civilization_object.train_unit("Worker")
    for archer in range(Archers):
        civilization_object.train_unit("Archer")
    for cavalry in range(Cavalries):
        civilization_object.train_unit("Cavalry")
    for infantry in range(Infantries):
        civilization_object.train_unit("Infantry")

    return None

def print_phase_1(civ1 : Civilization, civ2 : Civilization) -> None:
    """
    Imprime el estado de las civilizaciones en la fase 1.

    Parameters
    ----------
    civ1 : Civilization
        La primera civilización.
    civ2 : Civilization
        La segunda civilización.

    Returns
    -------
    None
    """
    civilizations = [civ1, civ2]
    unit_list = [Worker, Archer, Cavalry, Infantry]
    for civ in civilizations:
        print(f"{civ.name} Resources: {civ.resources}\n")
        for unit in unit_list:
            for number_unit in range(len(civ.units)):
                if isinstance(civ.units[number_unit], unit):
                    print(f"{unit.__name__}: {civ.units[number_unit].name} ({civ.units[number_unit].hp}/{civ.units[number_unit].total_hp})")
        print()
    return None

def print_phase_2(created_units: list[Unit], civ1, civ2) -> None:
    """
    Imprime el estado de las unidades creadas en la fase 2.

    Parameters
    ----------
    created_units : list[Unit]
        Lista de unidades creadas.
    civ1 : Civilization
        La primera civilización.
    civ2 : Civilization
        La segunda civilización.

    Returns
    -------
    None
    """
    units_by_civ = dict(zip([civ1, civ2], created_units))
    for civ in units_by_civ:
        if units_by_civ[civ] is None:
            print(f"{civ.name} cannot create any unit right now")
        else:
            print(f"{civ.name} creates {units_by_civ[civ].name} ({units_by_civ[civ].unit_type}) Stats: ATT: {units_by_civ[civ].strength} DEF: {units_by_civ[civ].defense}, HP: {units_by_civ[civ].hp}/{units_by_civ[civ].total_hp}")
    return None

def print_phase_3(attacker_oponnent : tuple, control_variable: int, dmg: int, data_p: list) -> None:
    """
    Imprime el estado de la batalla en la fase 3.

    Parameters
    ----------
    attacker_oponnent : tuple
        Tupla que contiene las unidades atacante y oponente.
    control_variable : int
        Variable de control para determinar qué civilización está atacando.
    dmg : int
        Daño infligido en el ataque.
    data_p : list
        Lista para recopilar datos estadísticos.

    Returns
    -------
    None
    """
    #control_variable % 2 == 0 -> muestra la civ1, control_variable % 2 != 0 -> muestra civ2
    
    attacker = attacker_oponnent[0]
    opponent = attacker_oponnent[1]

    if control_variable % 2 == 0:
        print(f"{civ1.name} - {attacker.name} attacks {civ2.name} - {opponent} with damage {dmg} (hp = {opponent.hp}/{opponent.total_hp})")
        stat_collect(attacker,dmg,civ1,opponent,data_p)
    else:
        print(f"{civ2.name} - {attacker.name} attacks {civ1.name} - {opponent} with damage {dmg} (hp = {opponent.hp}/{opponent.total_hp})")
        stat_collect(attacker,dmg,civ2,opponent,data_p)

    return None

def production(turn : int, civilizations: list[Unit]) -> list[Unit]:
    """
    Produce unidades para las civilizaciones en función del número de turno.

    Parameters
    ----------
    turn : int
        El número de turno actual.
    civilizations : list[Unit]
        Lista de civilizaciones.

    Returns
    -------
    list[Unit]
        Lista de unidades creadas.
    """
    units_created = []
    for civ in civilizations:
        if turn % 4 == 0:
            units_created.append(civ.train_unit("Archer"))
        elif turn % 4 == 1:
            units_created.append(civ.train_unit("Cavalry"))
        elif turn % 4 == 2:
            units_created.append(civ.train_unit("Infantry"))
        elif turn % 4 == 3:
            units_created.append(civ.train_unit("Worker"))
    return units_created

def battle(civ1: Civilization, civ2: Civilization) -> Union[bool, None]:
    """
    Simula una batalla entre dos civilizaciones.

    Parameters
    ----------
    civ1 : Civilization
        La primera civilización.
    civ2 : Civilization
        La segunda civilización.

    Returns
    -------
    bool
        True si una civilización ha perdido, False en caso contrario.
    """

    if civ1.all_debilitated() is False or civ2.all_debilitated() is False:
        civ_dict = {civ1 : [], civ2: []}
        for civ in civ_dict:
            for unit in civ.units:
                if isinstance(unit, Worker) and all_military_units_defeated(civ) is False:
                    civ_dict[civ] = list_without_workers(civ)
                    break
                else:
                    civ_dict[civ] = civ.units
                    break
    
    control_attacker = 0
    control_opponent = 1
    alternating_between_civs = 1
    print_who_civ_attacks = 0
    control = 0

    
    civ_list = list(civ_dict)
    while True:
        #choose_who_civ_attack: 0 -> civ1 attacks, 1 -> civ2 attacks
        choose_who_civ_attack = control % 2
        choose_who_civ_is_opponent = control_opponent % 2

        attacker = get_attacker(civ_dict, control_attacker, choose_who_civ_attack)

        if isinstance(attacker, int):
            if not len(list(civ_dict.values())[choose_who_civ_attack]) == len(list(civ_dict.values())[choose_who_civ_is_opponent]):
                if attacker == 0:
                    print(f"\nEnd of alternating sequence: Civilization {civ1.name} has no more attackers left")
                    choose_who_civ_attack = 1
                    attacker = get_attacker(civ_dict, control_attacker, choose_who_civ_attack)
                    if isinstance(attacker, int):
                        print(f"Civilization: {civ2.name} has no more attackers left either")
                        return None
                    else:         
                        print(f"The remaining units of the stronger civilization: {civ2.name} now attacks in sequence")
                        choose_who_civ_is_opponent = 0
                        break
                else:
                    print(f"\nEnd of alternating sequence: Civilization {civ2.name} has no more attackers left")
                    choose_who_civ_attack = 0
                    control_attacker += 1
                    attacker = get_attacker(civ_dict, control_attacker, choose_who_civ_attack)
                    if isinstance(attacker, int):
                        print(f"Civilization: {civ1.name} has no more attackers left either")
                        return None
                    else:
                        print(f"The remaining units of the stronger civilization: {civ1.name} now attacks in sequence")
                        choose_who_civ_is_opponent = 1
                        break
            else:
                print("\nBoth civilizations don't have more attackers")
                return None

        opponent = get_opponent(civ_dict, civ_list[choose_who_civ_is_opponent], attacker)
        end = attack_procedure(civ_dict, attacker, opponent, civ_list[choose_who_civ_is_opponent], print_who_civ_attacks)
        if end is True:
            print(f"Civilization: {civ_list[choose_who_civ_is_opponent].name} has lost against civilization: {civ_list[choose_who_civ_attack].name}")
            return end
        
        #Cada dos iteraciones el índice del atacante debe aumentar, debe permanecer igual por dos iteraciones
        #porque en la primera iteración ataca indice n de civ 1 y luego tiene que atacar indice n
        if alternating_between_civs % 2 == 0:
            control_attacker += 1

        control_opponent += 1
        alternating_between_civs += 1
        print_who_civ_attacks += 1
        control += 1

    count = len(list(civ_dict.values())[choose_who_civ_is_opponent]) - 1
    if choose_who_civ_attack == 1:
        attack_remaining_units(civ_dict, civ_list, count, choose_who_civ_attack, choose_who_civ_is_opponent)

    else:
        attack_remaining_units(civ_dict, civ_list, count, choose_who_civ_attack, choose_who_civ_is_opponent)

    return False

def attack_remaining_units(civ_dict : dict, civ_list : list[Unit], count: int, choose_who_civ_attack: int, choose_who_civ_is_opponent: int) -> Union[bool, None]:
    """
    Maneja los ataques restantes cuando una civilización no tiene más atacantes.

    Parameters
    ----------
    civ_dict : dict
        Diccionario de civilizaciones y sus unidades.
    civ_list : list[Unit]
        Lista de civilizaciones.
    count : int
        Contador para el número de ataques.
    choose_who_civ_attack : int
        Índice para elegir qué civilización ataca.
    choose_who_civ_is_opponent : int
        Índice para elegir qué civilización es el oponente.

    Returns
    -------
    None
    """
    while True:
        attacker = get_attacker(civ_dict, count, choose_who_civ_attack)
        if isinstance(attacker, int):
            print(f"Civilization : {civ_list[choose_who_civ_attack].name} has no more attackers left")
            return None
        opponent = get_opponent(civ_dict, civ1,  attacker)
        end = attack_procedure(civ_dict, attacker, opponent, civ_list[choose_who_civ_is_opponent], choose_who_civ_attack)
        if end is True:
            print(f"Civilization: {civ_list[choose_who_civ_is_opponent].name} has lost against civilization: {civ_list[choose_who_civ_attack].name}")
            return end
        count += 1

def list_without_workers(civ: Civilization) -> list[Unit]:
    """
    Obtiene una lista de unidades militares sin trabajadores.

    Parameters
    ----------
    civ : Civilization
        La civilización para filtrar unidades.

    Returns
    -------
    list[Unit]
        Lista de unidades militares sin trabajadores.
    """
    military_units = []
    for unit in civ.units:
        if not isinstance(unit, Worker):
            military_units.append(unit)
    return military_units

def attack_handler(civ_dict: dict, count: int, choice : int) -> Union[Unit, None]:
    """
    Maneja el proceso de ataque y devuelve el atacante.

    Parameters
    ----------
    civ_dict : dict
        Diccionario de civilizaciones y sus unidades.
    count : int
        Contador para el número de ataques.
    choice : int
        Índice para elegir qué civilización ataca.

    Returns
    -------
    Unit
        La unidad atacante.
    """
    #list() para permitir que civ_dict.values() sea scriptable (usar choice y count)
    #civ_dict.values() esto te devuelve los atacantes de civ 1 y civ 2
    #con choice se elige entrar en los atacantes de civ 1 o 2. valores 0 y 1 respectivamente.
    #con count se elige cuál atacante en específico.
    try:
        attacker = list(civ_dict.values())[choice][count]
    except IndexError:
        return None
    else:                  
        return attacker
      
def get_attacker(civ_dict: dict, count: int, choice : int) -> Union[Unit, int]:
    """
    Obtiene la unidad atacante.

    Parameters
    ----------
    civ_dict : dict
        Diccionario de civilizaciones y sus unidades.
    count : int
        Contador para el número de ataques.
    choice : int
        Índice para elegir qué civilización ataca.

    Returns
    -------
    Unit
        La unidad atacante.
    """
    attacker = attack_handler(civ_dict, count, choice)

    if attacker is None:
        return choice 
    
    return attacker

def get_opponent(civ_dict : dict, civ_opponent: Civilization, attacker: Unit) -> Unit:
    """
    Obtiene la unidad oponente para el atacante.

    Parameters
    ----------
    civ_dict : dict
        Diccionario de civilizaciones y sus unidades.
    civ_opponent : Civilization
        La civilización oponente.
    attacker : Unit
        La unidad atacante.

    Returns
    -------
    Unit
        La unidad oponente.
    """
    temp1 = []
    temp2 = []
    for opponent in civ_dict[civ_opponent]:
        effectiveness_point = attacker.effectiveness(opponent)
        if effectiveness_point not in temp1:
            temp1.append(effectiveness_point)
            temp2.append(opponent)
    possible_opponents = dict(zip(temp2, temp1))
    opponent = max(possible_opponents, key=possible_opponents.get)
    return opponent                

def attack_procedure(civ_dict: dict, attacker : Unit, opponent: Unit, civ : Civilization, print_civ: int) -> Union[bool, None]:
    """
    Ejecuta el procedimiento de ataque.

    Parameters
    ----------
    civ_dict : dict
        Diccionario de civilizaciones y sus unidades.
    attacker : Unit
        La unidad atacante.
    opponent : Unit
        La unidad oponente.
    civ : Civilization
        La civilización del oponente.
    print_civ : int
        Índice para determinar qué civilización está atacando.

    Returns
    -------
    bool
        True si la civilización oponente ha perdido, False en caso contrario.
    """
    if attacker.hp > 0:
        dmg = attacker.attack(opponent)
        if opponent.hp <= 0:
            if civ.all_debilitated() is True:
                print_phase_3((attacker, opponent), print_civ, dmg, data_p)
                return True 
        print_phase_3((attacker, opponent), print_civ, dmg, data_p)
        return None
    else:
        pass

def all_military_units_defeated(civ : Civilization) -> bool:
    """
    Verifica si todas las unidades militares de una civilización están derrotadas.

    Parameters
    ----------
    civ : Civilization
        La civilización a verificar.

    Returns
    -------
    bool
        True si todas las unidades militares están derrotadas, False en caso contrario.
    """
    for unit in civ.units:
        if not isinstance(unit, Worker):
            return False
    return True

def stat_collect(attacker: Unit, dmg: int, civilization: Civilization, opponent: Unit, data_p: list) -> list:
    """
    Recopila datos estadísticos de la batalla.

    Parameters
    ----------
    attacker : Unit
        La unidad atacante.
    dmg : int
        Daño infligido en el ataque.
    civilization : Civilization
        La civilización del atacante.
    opponent : Unit
        La unidad oponente.
    data_p : list
        Lista para recopilar datos estadísticos.

    Returns
    -------
    list
        Lista actualizada con los datos recopilados.
    """
    new_data = [attacker.name, type(attacker).__name__, dmg, civilization.name, type(opponent).__name__]
    data_p.append(new_data)
    return data_p

def statistics_show(data_p: list) -> None:
    """
    Muestra las estadísticas de la batalla.

    Parameters
    ----------
    data_p : list
        Lista de datos estadísticos recopilados.

    Returns
    -------
    None
    """
    main_data_frame = pd.DataFrame(data_p, columns=["Attacker", "Type", "Dmg", "Civilization", "Opponent"])
    
    # Calcular el daño promedio y la desviación estándar por unidad para cada civilización
    avg_std_damage_per_unit_civ = main_data_frame.groupby(["Civilization", "Attacker"])["Dmg"].agg(["mean", "std"]).reset_index()
    avg_std_damage_per_unit_civ.columns = ["Civilization", "Attacker", "Average Damage", "Standard Deviation"]
    
    print("Average Damage and Standard Deviation per Unit for each Civilization:")
    print(avg_std_damage_per_unit_civ)
    
    # Calcular el daño promedio y la desviación estándar por tipo de unidad para cada civilización
    avg_std_damage_per_unit_type_civ = main_data_frame.groupby(["Civilization", "Type"])["Dmg"].agg(["mean", "std"]).reset_index()
    avg_std_damage_per_unit_type_civ.columns = ["Civilization", "Type", "Average Damage", "Standard Deviation"]
    
    print("Average Damage and Standard Deviation per Unit Type for each Civilization:")
    print(avg_std_damage_per_unit_type_civ)
    
    # Calcular el daño promedio que cada tipo de unidad inflige a cada uno de los otros tipos, para cada civilización
    avg_damage_per_unit_type_opponent = main_data_frame.groupby(["Civilization", "Type", "Opponent"])["Dmg"].mean().reset_index()
    avg_damage_per_unit_type_opponent.columns = ["Civilization", "Attacker Type", "Opponent Type", "Average Damage"]
    
    print("Average Damage per Unit Type to each Opponent Type for each Civilization:")
    print(avg_damage_per_unit_type_opponent)
    
    return None

if __name__ == "__main__":
    actual_turn = 1
    # Leer el archivo de configuración desde la línea de comandos o usar el predeterminado
    config_file = sys.argv[1] if len(sys.argv) > 1 else "battle1.txt"

    # Intentar abrir el archivo especificado
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: El archivo '{config_file}' no existe.", file=sys.stderr)
        sys.exit(1)

    # Resto del código de la simulación...
    print(f"Leyendo configuración desde: {config_file}")

    civ1_data = lines[0].split(":")
    civ1_name = civ1_data[0]
    resources1 = int(civ1_data[1])
    
    civ2_data = lines[1].split(":")
    civ2_name = civ2_data[0]
    resources2 = int(civ2_data[1])
    
    turns_line = lines[2]
    parts = turns_line.replace(":", ",").split(",")
    turns = int(parts[1].strip()) #Numero de turnos leidos desde el archivo .txt

    # Leer la cantidad inicial de cada tipo de unidad
    workers_line = lines[3]
    workers = int(workers_line.split(":")[1].strip())

    archers_line = lines[4]
    archers = int(archers_line.split(":")[1].strip())

    cavalry_line = lines[5]
    cavalry = int(cavalry_line.split(":")[1].strip())

    infantry_line = lines[6]
    infantry = int(infantry_line.split(":")[1].strip())

    # Parte 3 : 

    # Crear instancias de civilización

    print (f"[TODO: Create civilization: {civ1_name} with {resources1} initial resources]")
    print (f"[TODO: Create civilization: {civ2_name} with {resources2} initial resources]")
    civ1 = Civilization(civ1_name, resources1)
    civ2 = Civilization(civ2_name, resources2)
    civilizations_list = [civ1, civ2]

    # Crear unidades según la cantidad especificada en el fichero de batalla escogido
    
    print (f"[TODO: Create {workers} workers for {civ1_name}]") 
    print (f"[TODO: Create {workers} workers for {civ2_name}]")
    print (f"[TODO: Create {archers} archers for {civ1_name}]")
    print (f"[TODO: Create {archers} archers for {civ2_name}]")
    print (f"[TODO: Create {cavalry} cavalry for {civ1_name}]")
    print (f"[TODO: Create {cavalry} cavalry for {civ2_name}]")
    print (f"[TODO: Create {infantry} infantry for {civ1_name}]")
    print (f"[TODO: Create {infantry} infantry for {civ2_name}]")

    create_units(civ1,workers,archers,cavalry,infantry) # Crea las unidades para la civilizacion 1
    create_units(civ2,workers,archers,cavalry,infantry) # Crea las unidades para la civilizacion 2

    data_p=[] #inicializacion de la matriz para pandas

    #Implementación de la lógica de batalla
    while actual_turn <= turns:
        #fase 1 - recolección:      
        print("TURNO:\n", actual_turn)
        print("PHASE 1: REPORT")
        print("----------------------------------------")
        civ1.collect_resources()
        civ2.collect_resources()
        #Phase 1 report

        #Redefine la lista de units con aquellas unidades que siguen con vida.
        civ1.list_units_alive(civ1.units)
        civ2.list_units_alive(civ2.units)
        print_phase_1(civ1, civ2)

        #fase 2 - producción:
        print("PHASE 2: PRODUCTION")
        print("----------------------------------------")
        created_units = production(actual_turn, civilizations_list)

        #phase 2 - report

        print_phase_2(created_units, civ1, civ2)

        #fase 3 - Batalla
        print()
        print("PHASE 3: BATTLE STATUS")
        print("----------------------------------------") 
        end = battle(civ1,civ2)
        if end is True:
            break
        #phase 3 - report
        #Por cada ataque debe ejercutarse print_phase_3, es decir, será llamado dentro de battle cada que se haga un ataque
        #Esto tiene que ser así porque la vida de la unidad debe reflejar el dmg que se le fue efectuado, si le hicieron 
        #dmg 4 a una unidad de 25 de hp el hp que se muestre debe ser 21, si se quiere llamar a la función print_phase_3 aquí luego de que 
        #todas las unidades hayan atacado entonces una misma unidad muy probablemente haya recibido más de un ataque
        #y el dmg que le fue efectuado por una unidad no reflejará su hp, por ejemplo una le dio dmg 4 a la de 25 hp, pero esa misma recibio 2 ataques más
        # de 5 y 7  dmg, el hp que se mostrará de la unidad será 9 y no 21.
        actual_turn += 1
    print("\nFin de la simulación")
    print("Estadísticas: ")
    statistics_show(data_p)