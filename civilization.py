# Parte 2
from unit import *
"""
Authors:
Sebastián David Moreno Expósito; sebastian.exposito@udc.es
Xoel Sánchez Dacoba; xoel.sanchez.dacoba@udc.es
"""
class Civilization:
    """
    Representa una civilización con recursos y unidades.

    Attributes
    ----------
    unit_name_list : list
        Lista de nombres de tipos de unidades.
    cost_per_unit : dict
        Diccionario que mapea el nombre de la unidad a su costo.
    name : str
        Nombre de la civilización.
    resources : int
        Recursos disponibles de la civilización.
    units : list[Unit]
        Lista de unidades de la civilización.
    _count_unit_type : dict
        Diccionario que cuenta el número de unidades por tipo.
    """
    # class atributes
    unit_name_list = ["Archer", "Cavalry", "Infantry", "Worker"]
    cost_per_unit = dict(zip(unit_name_list, [60,60,60,30]))

    def __init__(self, name: str, resources: int):
        """
        Inicializa una instancia de la clase Civilization.

        Parameters
        ----------
        name : str
            Nombre de la civilización.
        resources : int
            Recursos iniciales de la civilización.

        Returns
        -------
        None
        """
        #instance atributes
        self.name = name
        self.resources = resources
        self._units = []
        self._count_unit_type = dict(zip(self.unit_name_list, [1,1,1,1])) 
    #Access and modify private atributes:

    #atribute name
    @property
    def name(self):
        """
        Obtiene el nombre de la civilización.

        Returns
        -------
        str
            Nombre de la civilización.
        """
        return self._name
    
    @name.setter #Necesita tener el mismo nombre que se define en el property
    def name(self, sentence):
        """
        Establece el nombre de la civilización.

        Parameters
        ----------
        sentence : str
            Nombre de la civilización.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Si el nombre no es una cadena.
        ValueError
            Si el nombre está vacío.
        """
        if not isinstance(sentence,str):
            raise TypeError("name atribute must be type str")
        elif len(sentence) <= 0:
            raise ValueError("name atribute can't be void")
        else:
            self._name = sentence

    #atribute resources
    @property
    def resources(self):
        """
        Obtiene los recursos de la civilización.

        Returns
        -------
        int
            Recursos de la civilización.
        """
        return self._resources
    
    @resources.setter
    def resources(self, value):
        """
        Establece los recursos de la civilización.

        Parameters
        ----------
        value : int
            Recursos de la civilización.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Si los recursos no son un entero.
        ValueError
            Si los recursos son negativos.
        """
        if not isinstance(value, int):
            raise TypeError("resources atribute must be type int")
        elif value < 0:
            raise ValueError("resources atribute must be a positive integer")
        else:
            self._resources = value

    #atribute units
    @property
    def units(self) -> list[Unit]:
        """
        Obtiene la lista de unidades de la civilización.

        Returns
        -------
        list[Unit]
            Lista de unidades de la civilización.
        """
        return self._units
    
    @units.setter
    def units(self, unit):
        """
        Establece la lista de unidades de la civilización.

        Parameters
        ----------
        unit : list
            Lista de unidades.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Si las unidades no son una lista.
        """
        if isinstance(unit, list):
            self._units = unit
        else:
            raise TypeError("units must be type list")

        #methods
        
    def train_unit(self, unit_type: str) -> Unit:
        """
        Entrena una nueva unidad para la civilización.

        Parameters
        ----------
        unit_type : str
            Tipo de unidad a entrenar.

        Returns
        -------
        Unit
            La unidad entrenada.

        Raises
        ------
        ValueError
            Si el tipo de unidad no es válido.
        TypeError
            Si el tipo de unidad no es una cadena.
        """
        if isinstance(unit_type, str):
            if unit_type in self.unit_name_list:
                if self.resources >= self.cost_per_unit[unit_type]:
                    unit = self.new_unit_instance(unit_type)
                    #print(unit)
                    self._count_unit_type[unit_type] += 1
                    self.resources = self.resources - self.cost_per_unit[unit_type] #Resta el costo de la unidad a los recursos
                    self.units.append(unit) #Agrega la unidad a la lista de unidades
                    return unit #Retorna Unit
                else:
                    return None
            else: 
                raise ValueError(f"{unit_type} is not a valid type of unit. It must be one of these: {self.unit_name_list}")
        else:
            raise TypeError("unit_type must be type str")
            
    def collect_resources(self) -> None:
        """
        Recolecta recursos de las unidades de tipo Worker.

        Returns
        -------
        None
        """
        for unit in range(len(self.units)):
            if self.units[unit].unit_type == "Worker": #Mira si unit_type es de tipo worker
                if self.units[unit].is_debilitated() is False: #Ya sabe que es de tipo worker, ahora mira si está vivo
                    self.resources = self.resources + self.units[unit].collect()
        return None

    def all_debilitated(self) -> bool:
        """
        Verifica si todas las unidades de la civilización están debilitadas.

        Returns
        -------
        bool
            True si todas las unidades están debilitadas, False en caso contrario.
        """
        if len(self.units) == 0:
            return True
        for unit in range(len(self.units)):
            if self.units[unit].is_debilitated() is False: #Si hay uno que no está debilitado significa que no todos están debilitados
                return False
        return True
            
    #Used in train_unit() for creating new units dinamically and using the name X_Y, 
    #where X is type_unit and Y the number of units of that type that already exist
    def new_unit_instance(self, unit_type: str) -> Unit:
        """
        Crea una nueva instancia de unidad.

        Parameters
        ----------
        unit_type : str
            Tipo de unidad a crear.

        Returns
        -------
        Unit
            La nueva unidad creada.
        """
        if unit_type == "Archer":
            return Archer(f"{unit_type}_{self._count_unit_type[unit_type]}")
        elif unit_type == "Cavalry":
            return Cavalry(f"{unit_type}_{self._count_unit_type[unit_type]}")
        elif unit_type == "Infantry":
            return Infantry(f"{unit_type}_{self._count_unit_type[unit_type]}")
        elif unit_type == "Worker":
            return Worker(f"{unit_type}_{self._count_unit_type[unit_type]}") 

    #Redefines the list of units with the units that are alive
    def list_units_alive(self, units_list : list[Unit]) -> None:
        """
        Redefine la lista de unidades con las unidades que están vivas.

        Parameters
        ----------
        units_list : list[Unit]
            Lista de unidades.

        Returns
        -------
        None
        """
        alive_units = []
        for unit in units_list:
            if unit.is_debilitated() is not True:
                alive_units.append(unit)
        self.units = alive_units
        return None
                
            
    #Redefine magic methods
    def __str__(self):
        """
        Representación en cadena de la civilización.

        Returns
        -------
        str
            Representación en cadena de la civilización.
        """
        units_str = '\n'.join(str(unit) for unit in self._units)
        return f"Civilization: {self._name}, Resources: {self._resources}, units:\n[{units_str}]"
    
    def __repr__(self):
        """
        Representación oficial en cadena de la civilización.

        Returns
        -------
        str
            Representación oficial en cadena de la civilización.
        """
        units_str = '\n'.join(str(unit) for unit in self._units)
        return f"Civilization: {self._name}, Resources: {self._resources}, units:\n[{units_str}]"