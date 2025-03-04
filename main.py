import sys
import importlib
from unit import *
from civilization import *

def create_units(civilization_object: Unit, Workers: int = 0, Archers: int = 0, Cavalries: int = 0, Infantries: int = 0) -> None:
    for worker in range(Workers):
        civilization_object.train_unit("Worker")
    for archer in range(Archers):
        civilization_object.train_unit("Archer")
    for cavalry in range(Cavalries):
        civilization_object.train_unit("Cavalry")
    for infantry in range(Infantries):
        civilization_object.train_unit("Infantry")

def print_phase_1(civ1 : Civilization, civ2 : Civilization) -> None:
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
    print("PHASE 2: PRODUCTION")
    print("----------------------------------------")
    units_by_civ = dict(zip([civ1, civ2], created_units))
    for civ in units_by_civ:
        if units_by_civ[civ] is None:
            print(f"{civ.name} cannot create any unit right now")
        else:
            print(f"{civ.name} creates {units_by_civ[civ].name} ({units_by_civ[civ].unit_type}) Stats: ATT: {units_by_civ[civ].strength} DEF: {units_by_civ[civ].defense}, HP: {units_by_civ[civ].hp}/{units_by_civ[civ].total_hp}")
    return None

def print_phase_3(attacker_oponnent : tuple, control_variable: int, dmg: int):
    #control_variable % 2 == 0 -> muestra la civ1, control_variable % 2 != 0 -> muestra civ2

    attacker = attacker_oponnent[0]
    opponent = attacker_oponnent[1]

    if control_variable % 2 == 0:
        print(f"{civ1.name} - {attacker.name} attacks {civ2.name} - {opponent} with damage {dmg} (hp = {opponent.hp}/{opponent.total_hp})")
    else:
        print(f"{civ2.name} - {attacker.name} attacks {civ1.name} - {opponent} with damage {dmg} (hp = {opponent.hp}/{opponent.total_hp})")

def production(turn : int, civilizations: list[Unit]) -> list[Unit]:
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

def battle(civ1: Civilization, civ2: Civilization):

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
    
    diff = abs(len(list(civ_dict.values())[choose_who_civ_attack]) - len(list(civ_dict.values())[choose_who_civ_is_opponent]))

    if choose_who_civ_attack == 1:
        count = len(list(civ_dict.values())[choose_who_civ_is_opponent]) - 1
        while diff >= 0:
            attacker = list(civ_dict.values())[choose_who_civ_attack][count]
            opponent = get_opponent(civ_dict, civ_list[0], attacker)
            dmg = attacker.attack(opponent)
            if opponent.hp <= 0:
                civ.units.remove(opponent)
                if civ.all_debilitated() is True:
                    print_phase_3((attacker, opponent), choose_who_civ_attack, dmg)
                    return True 
            print_phase_3((attacker, opponent), choose_who_civ_attack, dmg)
            diff -= 1
            count += 1
    else:
        count = len(list(civ_dict.values())[choose_who_civ_is_opponent]) - 1
        while diff >= 0:
            attacker = list(civ_dict.values())[choose_who_civ_attack][count]
            opponent = get_opponent(civ_dict, civ_list[1], attacker)
            dmg = attacker.attack(opponent)
            if opponent.hp <= 0:
                civ.units.remove(opponent)
                if civ.all_debilitated() is True:
                    print_phase_3((attacker, opponent), choose_who_civ_attack, dmg)
                    return True 
            print_phase_3((attacker, opponent), choose_who_civ_attack, dmg)
            diff -= 1
            count += 1

    return False

def list_without_workers(civ: Civilization) -> list[Unit]:
    military_units = []
    for unit in civ.units:
        if not isinstance(unit, Worker):
            military_units.append(unit)
    return military_units

def attack_handler(civ_dict: dict, count: int, choice : int):
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
      
def get_attacker(civ_dict: dict, count: int, choice : int) -> Unit:
    """
    Devuelve al atacante.
    """
    attacker = attack_handler(civ_dict, count, choice)

    if attacker is None:
        return choice 
    
    return attacker

def get_opponent(civ_dict : dict, civ_opponent: Civilization, attacker: Unit) -> Unit:
    """
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

def attack_handler(civ_dict: dict, count: int, choice : int):
    try:
        attacker = list(civ_dict.values())[choice][count]
    except IndexError:
        return None
    else:                  
        return attacker

def attack_procedure(civ_dict: dict, attacker : Unit, opponent: Unit, civ : Civilization, print_civ: int):

    dmg = attacker.attack(opponent)
    if opponent.hp <= 0:
        civ.units.remove(opponent)
        if civ.all_debilitated() is False:
            for unit in civ.units:
                if isinstance(unit, Worker) and all_military_units_defeated(civ) is False:
                    civ_dict[civ] = list_without_workers(civ)
                    break
                else:
                    civ_dict[civ] = civ.units
                    break
        else:
            print_phase_3((attacker, opponent), print_civ, dmg)
            return True 
    print_phase_3((attacker, opponent), print_civ, dmg)
    return None

def all_military_units_defeated(civ : Civilization) -> bool:
    for unit in civ.units:
        if not isinstance(unit, Worker):
            return False
    return True

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