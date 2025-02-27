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

def print_phase_2(created_units: list[Unit], civ1, civ2) -> None:
        
    if created_units[0] == None and created_units[1] == None:
        print(f"{civ1.name} cannot create any unit right now")
        print(f"{civ2.name} cannot create any unit right now")
    elif created_units[1] == None:
        print(f"{civ2.name} cannot create any unit right now")
        print(f"{civ1.name} creates {created_units[0].name} ({created_units[0].unit_type}) Stats: ATT: {created_units[0].strength} DEF: {created_units[0].defense}, HP: {created_units[0].hp}/{created_units[0].total_hp}")
    elif created_units[0] == None:
        print(f"{civ1.name} cannot create any unit right now")
        print(f"{civ2.name} creates {created_units[1].name} ({created_units[1].unit_type}) Stats: ATT: {created_units[1].strength} DEF: {created_units[1].defense}, HP: {created_units[1].hp}/{created_units[1].total_hp}")
    else:
        print(f"{civ1.name} creates {created_units[0].name} ({created_units[0].unit_type}) Stats: ATT: {created_units[0].strength} DEF: {created_units[0].defense}, HP: {created_units[0].hp}/{created_units[0].total_hp}")
        print(f"{civ2.name} creates {created_units[1].name} ({created_units[1].unit_type}) Stats: ATT: {created_units[1].strength} DEF: {created_units[1].defense}, HP: {created_units[1].hp}/{created_units[1].total_hp}")    
    
    #Hipotesis 1 
# def print_phase_3(unit: Unit):

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
    if civ1.all_debilitated() != True and civ2.all_debilitated() != True:
            if len(civ1.units) == len(civ2.units):
                for count in range(len(civ1.units)):
                    op_civ1 = get_opponent(civ1, civ2, count)
                    op_civ2 = get_opponent(civ2, civ1, count)
                    civ1.units[count].attack(op_civ1)
                    civ2.units[count].attack(op_civ2)       

        #     military_units_civ1 = list_without_workers(civ1)
        #     military_units_civ2 = list_without_workers(civ2)
        #     if len(military_units_civ1) == len(military_units_civ2):
        #         for count in range(len(military_units_civ1)):
        #             op_civ1 = get_military_opponent(military_units_civ1, military_units_civ2, count)
        #             op_civ2 = get_military_opponent(military_units_civ2, military_units_civ1, count)
        #             military_units_civ1[count].attack(op_civ1)
        #             military_units_civ2[count].attack(op_civ2)

        # elif all_military_units_defeated(civ1) == True and all_military_units_defeated(civ2) == False:
        #     military_units_civ2 = list_without_workers(civ2)
        #     if len(civ1.units) == len(civ2.units):
        #         for count in range(len(civ1.units)):
        #             op_civ1 = get_military_opponent(civ1.units, military_units_civ2, count)
        #             op_civ2 = get_military_opponent(military_units_civ2, civ1.units, count)
        #             civ1.units[count].attack(op_civ1)
        #             military_units_civ2[count].attack(op_civ2)


        # elif all_military_units_defeated(civ1) == False and all_military_units_defeated(civ2) == True:           
        #     military_units_civ1 = list_without_workers(civ1)
        #     if len(civ1.units) == len(civ2.units):
        #         for count in range(len(civ1.units)):
        #             op_civ1 = get_military_opponent(military_units_civ1, civ2.units, count)
        #             op_civ2 = get_military_opponent(civ2.units, military_units_civ1, count)
        #             military_units_civ1[count].attack(op_civ1)
        #             civ2.units[count].attack(op_civ2)
        # else:
        #     military_units_civ1 = list_without_workers(civ1)
        #     if len(civ1.units) == len(civ2.units):
        #         for count in range(len(civ1.units)):
        #             op_civ1 = get_military_opponent(civ1.units, civ2.units, count)
        #             op_civ2 = get_military_opponent(civ2.units, civ1.units, count)
        #             civ1.units[count].attack(op_civ1)
        #             civ2.units[count].attack(op_civ2)         
        # for unit in civ1.units:
        #     if not isinstance(unit, Worker):
        #         pass
    else:
        #No retorna nada cuando todas las unidades de ambas civilizaciones 
        return None
    
def list_without_workers(civ: Civilization) -> list[Unit]:
    military_units = []
    for unit in civ.units:
        if not isinstance(unit, Worker):
            military_units.append(unit)
    return military_units
    
def get_opponent(civ1: Civilization = None, civ2: Civilization = None, count: int = 0) -> Unit:
    """
    Attacker will be of civ1
    Opponente wil be of civ2
    """
    list1 = []
    list2 = []
    
    attacker = civ1.units[count]

    if isinstance(attacker, Worker) and all_military_units_defeated(civ1) == True:
        if all_military_units_defeated(civ2) == False:
            for opponent in civ2.units:
                if not isinstance(opponent, Worker):
                    effectiveness_point = attacker.effectiveness(opponent)
                    if effectiveness_point not in list1:
                        list1.append(effectiveness_point)
                        list2.append(opponent)
                else:
                    pass
            possible_opponents = dict(zip(list2, list1))
            opponent = max(possible_opponents, key=possible_opponents.get)
            return opponent
        elif all_military_units_defeated(civ2) == True:
            for opponent in civ2.units:
                effectiveness_point = attacker.effectiveness(opponent)
                if effectiveness_point not in list1:
                    list1.append(effectiveness_point)
                    list2.append(opponent)
            possible_opponents = dict(zip(list2, list1))
            opponent = max(possible_opponents, key=possible_opponents.get)
            return opponent
    elif isinstance(attacker, Worker) and all_military_units_defeated(civ1) == False:
        pass
    else:
        if all_military_units_defeated(civ2) == False:        
            for opponent in civ2.units:
                if not isinstance(opponent, Worker):
                    effectiveness_point = attacker.effectiveness(opponent)
                    if effectiveness_point not in list1:
                        list1.append(effectiveness_point)
                        list2.append(opponent)
                else:
                    pass
            possible_opponents = dict(zip(list2, list1))
            opponent = max(possible_opponents, key=possible_opponents.get)
            return opponent
        elif all_military_units_defeated(civ2) == True:
            for opponent in civ2.units:
                effectiveness_point = attacker.effectiveness(opponent)
                if effectiveness_point not in list1:
                    list1.append(effectiveness_point)
                    list2.append(opponent)
            possible_opponents = dict(zip(list2, list1))
            opponent = max(possible_opponents, key=possible_opponents.get)
            return opponent

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

        print("turno:", actual_turn)
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

        battle(civ1,civ2)

        actual_turn += 1