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
    print("PHASE 1: REPORT")
    print("----------------------------------------")
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
    if created_units[0] == None and created_units[1] == None:
        print(f"{civ1.name} cannot create any unit right now")
    else:
        print(f"{civ1.name} creates {created_units[0].name} ({created_units[0].unit_type}) Stats: ATT: {created_units[0].strength} DEF: {created_units[0].defense}, HP: {created_units[0].hp}/{created_units[0].total_hp}")
    if created_units[1] == None:
        print(f"{civ2.name} cannot create any unit right now")
    else:
        print(f"{civ2.name} creates {created_units[1].name} ({created_units[1].unit_type}) Stats: ATT: {created_units[1].strength} DEF: {created_units[1].defense}, HP: {created_units[1].hp}/{created_units[1].total_hp}")    
    return None


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
    if civ1.all_debilitated() != True or civ2.all_debilitated() != True:
            if len(civ1.units) == len(civ2.units):
                for count in range(len(civ1.units)):
                    op_civ1 = get_opponent(civ1, civ2, count)
                    op_civ2 = get_opponent(civ2, civ1, count)
                    if op_civ1 is not None and op_civ2 is not None:
                        civ1.units[count].attack(op_civ1)
                        civ2.units[count].attack(op_civ2)   
                    elif op_civ1 is None and op_civ2 is not None :
                        civ2.units[count].attack(op_civ2)
                    elif op_civ1 is not None and op_civ2 is None:
                        civ1.units[count].attack(op_civ1)
                    else:
                        pass
            elif len(civ1.units) > len(civ2.units):
                diferencia = len(civ1.units) - len(civ2.units) # La diferencia sera las units de mas que tiene civ 1 sobre civ2, esas units
                #atacaran, haremos un bucle for donde cada iteracion sera una de esas unidades de mas que tiene civ1, por eso el bucle se
                #repetira la diferencia.

                #Atacaran las dos Civilizaciones hasta que se terminen todas las unidades de civ2. 
                #Por ello iteraremos sobre civ2. Apartir de allí solo atacara civ1.
                for count in range(len(civ2.units)):
                    op_civ1 = get_opponent(civ1, civ2, count)
                    op_civ2 = get_opponent(civ2, civ1, count)
                    if op_civ1 is not None and op_civ2 is not None:
                        civ1.units[count].attack(op_civ1)
                        civ2.units[count].attack(op_civ2)   
                    elif op_civ1 is None and op_civ2 is not None :
                        civ2.units[count].attack(op_civ2)
                    elif op_civ1 is not None and op_civ2 is None:
                        civ1.units[count].attack(op_civ1)
                    else:
                        pass
                    #El ataque de las unidades que quedan:
                count = len(civ2.units) - 1
                while diferencia >= 0:
                    op_civ1 = get_opponent(civ1, civ2, count)
                    if op_civ1 is not None:
                        civ1.units[count].attack(op_civ1)
                    count += 1
                    diferencia -= 1
            else:
                #len(civ2.units) > len(civ1.units)
                diferencia = len(civ2.units) - len(civ1.units)
                for count in range(len(civ1.units)):
                    op_civ1 = get_opponent(civ1, civ2, count)
                    op_civ2 = get_opponent(civ2, civ1, count)
                    if op_civ1 is not None and op_civ2 is not None:
                        civ1.units[count].attack(op_civ1)
                        civ2.units[count].attack(op_civ2)   
                    elif op_civ1 is None and op_civ2 is not None :
                        civ2.units[count].attack(op_civ2)
                    elif op_civ1 is not None and op_civ2 is None:
                        civ1.units[count].attack(op_civ1)
                    else:
                        pass

                count = len(civ1.units) - 1
                while diferencia >= 0:
                    op_civ2 = get_opponent(civ2, civ1, count)
                    if op_civ1 is not None:
                        civ2.units[count].attack(op_civ2)
                    count += 1
                    diferencia -= 1
    else:
        #retorna None si alguna de las dos civilizaciones se queda sin unidades
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
    Opponent wil be of civ2
    """
    list1 = []
    list2 = []
    
    attacker = civ1.units[count]

    if isinstance(attacker, Worker) and all_military_units_defeated(civ1) is True:
        if all_military_units_defeated(civ2) is False:
            for opponent in civ2.units:
                if not isinstance(opponent, Worker):
                    effectiveness_point = attacker.effectiveness(opponent)
                    if effectiveness_point not in list1:
                        list1.append(effectiveness_point)
                        list2.append(opponent)
            possible_opponents = dict(zip(list2, list1))
            opponent = max(possible_opponents, key=possible_opponents.get)
            return opponent
        elif all_military_units_defeated(civ2) is True:
            for opponent in civ2.units:
                effectiveness_point = attacker.effectiveness(opponent)
                if effectiveness_point not in list1:
                    list1.append(effectiveness_point)
                    list2.append(opponent)
            possible_opponents = dict(zip(list2, list1))
            opponent = max(possible_opponents, key=possible_opponents.get)
            return opponent
    elif isinstance(attacker, Worker) and all_military_units_defeated(civ1) is False:
        pass
    else:
        if all_military_units_defeated(civ2) is False:        
            for opponent in civ2.units:
                if not isinstance(opponent, Worker):
                    effectiveness_point = attacker.effectiveness(opponent)
                    if effectiveness_point not in list1:
                        list1.append(effectiveness_point)
                        list2.append(opponent)
            possible_opponents = dict(zip(list2, list1))
            opponent = max(possible_opponents, key=possible_opponents.get)
            return opponent
        
        elif all_military_units_defeated(civ2) is True:
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