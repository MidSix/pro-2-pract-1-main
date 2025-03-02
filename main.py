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

def print_phase_3(attacker_oponnent : dict, control_variable: int, dmg: int):
    attacker = attacker_oponnent[0]
    if control_variable % 2 == 0:
        print(f"{civ1.name} - {attacker.name} attacks {civ2.name} - {attacker_oponnent[1]} with damage {dmg} (hp = {attacker_oponnent[1].hp}/{attacker_oponnent[1].total_hp})")
    else:
        print(f"{civ2.name} - {attacker.name} attacks {civ1.name} - {attacker_oponnent[1]} with damage {dmg} (hp = {attacker_oponnent[1].hp}/{attacker_oponnent[1].total_hp})")

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
        #        
        if len(list(civ_dict.values())[0]) == len(list(civ_dict.values())[1]):
            for count in range(len(list(civ_dict.values())[0])):  
                attack_procedure(civ_dict, count)
        #
        elif len(list(civ_dict.values())[0]) > len(list(civ_dict.values())[1]):

            diferencia = len(list(civ_dict.values())[0]) - len(list(civ_dict.values())[1])
            for count in range(len(list(civ_dict.values())[1])): 
                attack_procedure(civ_dict, count)

            count = len(list(civ_dict.values())[1]) - 1
            while diferencia >= 0:

                op_civ1 = get_opponents(civ_dict, count=count,number_opponent=1, civ_opponent=civ2, civ_attackers=civ1)
                if list(civ_dict.values())[0][count].is_debilitated() is False:
                    list(civ_dict.values())[0][count].attack(op_civ1)
                count += 1
                diferencia -= 1
        #
        else:
            #len(list(civ_dict.values())[1] > len(list(civ_dict.values())[0])
            diferencia = len(list(civ_dict.values())[1]) - len(list(civ_dict.values())[0])
            for count in range(len(list(civ_dict.values())[0])):
                attack_procedure(civ_dict, count)

            count = len(list(civ_dict.values())[0]) - 1
            while diferencia >= 0:

                op_civ2 = get_opponents(civ_dict, count=count,number_opponent=1, civ_opponent=civ1, civ_attackers=civ2) 
                if list(civ_dict.values())[1][count].is_debilitated() is False:
                    list(civ_dict.values())[1][count].attack(op_civ2)
                count += 1
                diferencia -= 1
        return
    else:
        #retorna None si alguna de las dos civilizaciones se queda sin unidades
        return None

def list_without_workers(civ: Civilization) -> list[Unit]:
    military_units = []
    for unit in civ.units:
        if not isinstance(unit, Worker):
            military_units.append(unit)
    return military_units
    
def get_attackers(civ_dict: dict, count: int) -> list[Unit]:
    """
    Devuelve una lista con los atacantes de la civ 1 y civ 2 respectivamente.
    """
    attackers = []
    for unit_list in civ_dict.values():
        attackers.append(unit_list[count])
    return attackers

def get_opponents(civ_dict: dict, attackers: list[Unit] = None , number_opponent : int = 2, civ_opponent : Civilization = None, civ_attackers: Civilization = None, count : int = 0) -> Unit:
    """
    """
    if number_opponent != 1 or number_opponent != 2:
        cnn = 0
        if number_opponent == 2:
            opponents = []
            for opponent_civ in reversed(list(civ_dict.values())):
                list1 = []
                list2 = []
                for opponent in opponent_civ:
                    effectiveness_point = attackers[cnn].effectiveness(opponent)
                    if effectiveness_point not in list1:
                        list1.append(effectiveness_point)
                        list2.append(opponent)
                possible_opponents = dict(zip(list2, list1))
                opponent = max(possible_opponents, key=possible_opponents.get)
                opponents.append(opponent)
                cnn += 1
            return opponents
        
        else:
            #civ: oponente. si es civ2 significa que los atacantes son civ 1
            list1 = []
            list2 = []
            for opponent in civ_dict[civ_opponent]:
                effectiveness_point = list(civ_dict[civ_attackers])[count].effectiveness(opponent)
                if effectiveness_point not in list1:
                    list1.append(effectiveness_point)
                    list2.append(opponent)
        possible_opponents = dict(zip(list2, list1))
        opponent = max(possible_opponents, key=possible_opponents.get)
        return opponent                

    raise ValueError("number_opponent argument must be 1 or 2")

def attack_procedure(civ_dict: dict, count: int):
    attackers = get_attackers(civ_dict, count)
    opponents = get_opponents(civ_dict, attackers)
    attacker_and_opponent = dict(zip(attackers, opponents))
    i = 0
    control_variable = 0
    for attacker in attacker_and_opponent:
        if attacker.is_debilitated() is False:
            dmg = attacker.attack(list(attacker_and_opponent.values())[i])
            print_phase_3(list(attacker_and_opponent.items())[i], control_variable, dmg)
            control_variable += 1
            i += 1
    return attacker_and_opponent

def all_military_units_defeated(civ : Civilization) -> bool:
    for unit in civ.units:
        if not isinstance(unit, Worker):
            return False
    return True

if __name__ == "__main__":
    actual_turn = 1
    # Leer el archivo de configuración desde la línea de comandos o usar el predeterminado
    config_file = sys.argv[1] if len(sys.argv) > 1 else "battle0.txt"

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
        battle(civ1,civ2)

        #phase 3 - report
        #Por cada ataque debe ejercutarse print_phase_3, es decir, será llamado dentro de battle cada que se haga un ataque
        #Esto tiene que ser así porque la vida de la unidad debe reflejar el dmg que se le fue efectuado, si le hicieron 
        #dmg 4 a una unidad de 25 de hp el hp que se muestre debe ser 21, si se quiere llamar a la función print_phase_3 aquí luego de que 
        #todas las unidades hayan atacado entonces una misma unidad muy probablemente haya recibido más de un ataque
        #y el dmg que le fue efectuado por una unidad no reflejará su hp, por ejemplo una le dio dmg 4 a la de 25 hp, pero esa misma recibio 2 ataques más
        # de 5 y 7  dmg, el hp que se mostrará de la unidad será 9 y no 21.

        #Para terminar la batalla si alguna de las dos civilizaciones ha perdido todas sus unidades
        if civ1.all_debilitated() is True or civ2.all_debilitated() is True:
            break
        actual_turn += 1