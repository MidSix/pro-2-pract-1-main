# Parte 1
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
"""
Authors:
Sebastián David Moreno Expósito; sebastian.exposito@udc.es
Xoel Sánchez Dacoba; xoel.sanchez.dacoba@udc.es
"""
class Unit(ABC):
    """Clase abstracta que sirve como superclase para todas las unidades.
    
    Attributes
    ----------
    name : str
        El nombre de la unidad.
    unit_type : str
        El tipo de unidad.
    strength : int
        La fuerza de la unidad.
    defense : int
        La defensa de la unidad.
    hp : int
        Los puntos de vida actuales de la unidad.
    total_hp : int
        Los puntos de vida totales de la unidad.
    
    Methods
    -------
    name(self):
        Proporciona el nombre de la unidad.
    name(self, value: str):
        Escribe el nombre de la unidad y comprueba que es válido.
    unit_type(self):
        Proporciona el tipo de la unidad.
    unit_type(self, value: str):
        Escribe el tipo de la unidad y comprueba que es válido.
    strength(self):
        Proporciona la fuerza de la unidad.
    strength(self, value: int):
        Escribe la fuerza de la unidad y comprueba que es válida.
    defense(self):
        Proporciona la defensa de la unidad.
    defense(self, value: int):
        Escribe la defensa de la unidad y comprueba que es válida.
    hp(self):
        Proporciona los puntos de vida actuales de la unidad.
    hp(self, value: int):
        Escribe los puntos de vida actuales de la unidad y comprueba que son válidos.
    total_hp(self):
        Proporciona los puntos de vida totales de la unidad.
    total_hp(self, value: int):
        Escribe los puntos de vida totales de la unidad y comprueba que son válidos.
    attack(self, opponent: "Unit") -> int:
        Ataca a la unidad oponente, reduciendo sus puntos de vida.
    is_debilitated(self) -> bool:
        Verifica si la unidad está debilitada (sin puntos de vida).
    effectiveness(self, opponent: "Unit") -> int:
        Calcula la efectividad del ataque contra la unidad oponente.
    __str__(self) -> str:
        Proporciona una representación en cadena de texto de la unidad.
    """
    
    def __init__(self, name: str, strength: int, defense: int, hp: int, total_hp: int, unit_type: str):
        """Creación de los atributos de esta clase principal.
        
        Parameters
        ----------
        name : str
            El nombre de la unidad.
        strength : int
            La fuerza de la unidad.
        defense : int
            La defensa de la unidad.
        hp : int
            Los puntos de vida actuales de la unidad.
        total_hp : int
            Los puntos de vida totales de la unidad.
        unit_type : str
            El tipo de unidad.
        
        Returns
        -------
        None.
        """
        self.name = name
        self.unit_type = unit_type
        self.strength = strength
        self.defense = defense
        self.hp = hp
        self.total_hp = total_hp
        
    @property
    def name(self):
        """Proporciona el nombre de la unidad.
        
        Returns
        -------
        str
            El nombre de la unidad.
        """
        return self._name
    
    @name.setter
    def name(self, value: str):
        """Escribe el nombre de la unidad y comprueba que es válido y no una línea vacía, dando error si así es.
        
        Parameters
        ----------
        value : str
            El nuevo nombre de la unidad.
        
        Raises
        ------
        ValueError
            Si el nombre de la unidad es una cadena vacía.
        """
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Unit name must be a non-empty string")
                
    @property
    def unit_type(self):
        """Proporciona el tipo de la unidad.
        
        Returns
        -------
        str
            El tipo de la unidad.
        """
        return self._unit_type
    
    @unit_type.setter
    def unit_type(self, value: str):
        """Escribe el tipo de la unidad y comprueba que es válido y no una línea vacía, dando error si así es.
        
        Parameters
        ----------
        value : str
            El nuevo tipo de la unidad.
        
        Raises
        ------
        ValueError
            Si el tipo de la unidad no es una cadena no vacía.
        """
        if isinstance(value, str) and len(value) > 0:
            self._unit_type = value
        else:
            raise ValueError("Unit type must be a non-empty string")
            
    @property
    def strength(self):
        """Proporciona la fuerza de la unidad.
        
        Returns
        -------
        int
            La fuerza de la unidad.
        """
        return self._strength
    
    @strength.setter
    def strength(self, value: int):
        """Escribe la fuerza de la unidad y comprueba que es válida.
        
        Parameters
        ----------
        value : int
            La nueva fuerza de la unidad.
        
        Raises
        ------
        ValueError
            Si la fuerza de la unidad no es un entero no negativo.
        """
        if isinstance(value, int) and value >= 0:
            self._strength = value
        else:
            raise ValueError("Unit strength value must be a non-negative integer")

    @property
    def defense(self):
        """Proporciona la defensa de la unidad.
        
        Returns
        -------
        int
            La defensa de la unidad.
        """
        return self._defense
    
    @defense.setter
    def defense(self, value: int):
        """Escribe la defensa de la unidad y comprueba que es válida.
        
        Parameters
        ----------
        value : int
            La nueva defensa de la unidad.
        
        Raises
        ------
        ValueError
            Si la defensa de la unidad es un entero negativo.
        """
        if isinstance(value, int) and value >= 0:
            self._defense = value
        else:
            raise ValueError("Unit defense value must be a non-negative integer")

    @property
    def hp(self):
        """Proporciona los puntos de vida actuales de la unidad.
        
        Returns
        -------
        int
            Los puntos de vida actuales de la unidad.
        """
        return self._hp
    
    @hp.setter
    def hp(self, value: int):
        """Escribe los puntos de vida actuales de la unidad y comprueba que son válidos.
        
        Parameters
        ----------
        value : int
            Los nuevos puntos de vida de la unidad.
        
        Raises
        ------
        ValueError
            Si los puntos de vida de la unidad no son un entero no negativo.
        """
        if isinstance(value, int):
            self._hp = max(0,value)
        if self.hp < 0:
            raise ValueError("Unit hp value must be a non-negative integer")

    @property
    def total_hp(self):
        """Proporciona los puntos de vida totales de la unidad.
        
        Returns
        -------
        int
            Los puntos de vida totales de la unidad.
        """
        return self._total_hp
    
    @total_hp.setter
    def total_hp(self, value: int):
        """Escribe los puntos de vida totales de la unidad y comprueba que son válidos.
        
        Parameters
        ----------
        value : int
            Los nuevos puntos de vida totales de la unidad.
        
        Raises
        ------
        ValueError
            Si los puntos de vida totales de la unidad no son un entero no negativo.
        """
        if isinstance(value, int) and value >= 0:
            self._total_hp = value
        else:
            raise ValueError("Unit total hp value must be a non-negative integer")

    def attack(self, opponent: "Unit") -> int:
        """Ataca a la unidad oponente, reduciendo sus puntos de vida.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente a la que se ataca.
        
        Returns
        -------
        int
            El daño infligido.
        """
        opponent.hp -= 1
        return 1
    
    def is_debilitated(self) -> bool:
        """Verifica si la unidad está debilitada (sin puntos de vida).
        
        Returns
        -------
        bool
            True si la unidad está debilitada, False en caso contrario.
        """
        return self.hp <= 0
    
    def effectiveness(self, opponent: "Unit") -> int:
        """Calcula la efectividad del ataque contra la unidad oponente.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente.
        
        Returns
        -------
        int
            La efectividad del ataque.
        """
        pass
    
    def __str__(self) -> str:
        """Proporciona una representación en cadena de texto de la unidad.
        
        Returns
        -------
        str
            La representación en cadena de texto de la unidad.
        """
        return f"{self.name} ({self.unit_type}) Stats: ATT: {self.strength}, DEF: {self.defense}, HP: {self.hp}/{self.total_hp}"
    
    def __repr__(self):
        return self.__str__()
#--------------------
# Arqueros
#--------------------
class Archer(Unit):
    """Clase que representa una unidad de arquero.
    
    Attributes
    ----------
    name : str
        El nombre de la unidad.
    strength : int
        La fuerza de la unidad.defense : int
        La defensa de la unidad.
    hp : int
        Los puntos de vida actuales de la unidad.
    total_hp : int
        Los puntos de vida totales de la unidad.
    arrows : int
        El número de flechas de la unidad.
    
    Methods
    -------
    arrows(self):
        Proporciona el número de flechas de la unidad.
    arrows(self, value: int):
        Escribe el número de flechas de la unidad y comprueba que es válido.
    attack(self, opponent: "Unit") -> int:
        Ataca a la unidad oponente, infligiendo daño basado en el tipo de unidad y la cantidad de flechas.
    effectiveness(self, opponent: "Unit") -> int:
        Calcula la efectividad del ataque contra la unidad oponente específica.
    """

    def __init__(self, name: str,strength : int =7 , defense : int=2, hp : int=15, total_hp: int = 15, arrows : int =3):
        """Inicializa una unidad de arquero con atributos específicos.
        
        Parameters
        ----------
        name : str
            El nombre de la unidad.
        arrows : int
            El número de flechas de la unidad.
        
        Returns
        -------
        None.
        """
        #Toda unidad nueva creada apartir de la llamada a esta clase tendrá los siguientes atributos en su creación
        #¨Tabla 2, valores de los atributos para las unidades creadas¨
        #Lo único que es variable es el nombre de la unidad

        super().__init__(name, strength, defense, hp, total_hp, "Archer")
        self._arrows = arrows

    @property
    def arrows(self):
        """Proporciona el número de flechas de la unidad.
        
        Returns
        -------
        int
            El número de flechas de la unidad.
        """
        return self._arrows

    @arrows.setter
    def arrows(self, value: int):
        """Escribe el número de flechas de la unidad y comprueba que es válido.
        
        Parameters
        ----------
        value : int
            El nuevo número de flechas de la unidad.
        
        Raises
        ------
        ValueError
            Si el número de flechas no es un entero no negativo.
        """
        if isinstance(value, int) and value >= 0:
            self._arrows = value
        else:
            raise ValueError("Arrows must be a non-negative integer")

    def attack(self, opponent: "Unit") -> int:
        """Ataca a la unidad oponente, infligiendo daño basado en el tipo de unidad y la cantidad de flechas.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente a la que se ataca.
        
        Returns
        -------
        int
            El daño infligido.
        """
        if self.arrows > 0:
            if opponent.unit_type == "Cavalry":
                factor = 1.5
            elif opponent.unit_type == "Archer" or opponent.unit_type == "Worker":
                factor = 1
            elif opponent.unit_type == "Infantry":
                factor = 0.5
            else:
                raise ValueError("opponent class not valid")
            #Con int redondeas al número entero anterior más cercano al decimal puesto que lo que hace int es truncar el decimal y te deja la parte entera
            dmg = max(1, int((factor * self.strength) - opponent.defense))
            self.arrows -= 1
        else:
            dmg = 1

        opponent.hp = max(0, opponent.hp - dmg)
        return dmg
        
    def effectiveness(self, opponent: "Unit") -> int:
        """Calcula la efectividad del ataque contra la unidad oponente específica.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente.
        
        Returns
        -------
        int
            La efectividad del ataque.
        """
        if opponent.unit_type == "Cavalry":
            return 1
        elif opponent.unit_type == "Archer" or opponent.unit_type == "Worker":
            return 0
        else: 
            return -1
        

#--------------------
# Caballeria
#--------------------
class Cavalry(Unit):
    """Clase que representa una unidad de caballería.
    
    Attributes
    ----------
    name : str
        El nombre de la unidad.
    strength : int
        La fuerza de la unidad.
    defense : int
        La defensa de la unidad.
    hp : int
        Los puntos de vida actuales de la unidad.
    total_hp : int
        Los puntos de vida totales de la unidad.
    charge : int
        La carga de la unidad.
    
    Methods
    -------
    charge(self):
        Proporciona la carga de la unidad.
    charge(self, value: int):
        Escribe la carga de la unidad y comprueba que es válida.
    attack(self, opponent: "Unit") -> int:
        Ataca a la unidad oponente, infligiendo daño basado en el tipo de unidad y la carga.
    effectiveness(self, opponent: "Unit") -> int:
        Calcula la efectividad del ataque contra la unidad oponente específica.
    """
    
    def __init__(self, name: str,strength : int =5 , defense : int=2, hp : int=25, total_hp: int = 25, charge : int =5):    
        """Inicializa una unidad de caballería con atributos específicos.
        
        Parameters
        ----------
        name : str
            El nombre de la unidad.
        strength : int
            La fuerza de la unidad.
        defense : int
            La defensa de la unidad.
        hp : int
            Los puntos de vida actuales de la unidad.
        total_hp : int
            Los puntos de vida totales de la unidad.
        charge : int
            La carga de la unidad.
        
        Returns
        -------
        None.
        """
        #Toda unidad nueva creada apartir de la llamada a esta clase tendrá los siguientes atributos en su creación
        #¨Tabla 2, valores de los atributos para las unidades creadas¨
        #Lo único que es variable es el nombre de la unidad

        super().__init__(name, strength, defense, hp, total_hp, "Cavalry")
        self._charge = charge

    @property
    def charge(self):
        """Proporciona la carga de la unidad.
        
        Returns
        -------
        int
            La carga de la unidad.
        """
        return self._charge
    
    @charge.setter
    def charge(self, value: int):
        """Escribe la carga de la unidad y comprueba que es válida.
        
        Parameters
        ----------
        value : int
            La nueva carga de la unidad.
        
        Raises
        ------
        ValueError
            Si la carga de la unidad no es un entero no negativo.
        """
        if isinstance(value, int) and value >= 0:
            self._charge = value
        else:
            raise ValueError("Charge value must be a non-negative integer")
    
    def attack(self, opponent: "Unit") -> int:
        """Ataca a la unidad oponente, infligiendo daño basado en el tipo de unidad y la carga.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente a la que se ataca.
        
        Returns
        -------
        int
            El daño infligido.
        """
        if opponent.unit_type == "Infantry":
            factor = 1.5
        elif opponent.unit_type == "Cavalry" or opponent.unit_type == "Worker":
            factor = 1
        elif opponent.unit_type == "Archer":
            factor = 0.5
        else:
            raise ValueError("opponent class not valid")
        #Con int redondeas al número entero anterior más cercano al decimal puesto que lo que hace int es truncar el decimal y te deja la parte entera
        dmg = max(1, int((self.charge + factor * self.strength) - opponent.defense))
        opponent.hp = max(0, opponent.hp - dmg)
        return dmg
    
    def effectiveness(self, opponent: "Unit") -> int:
        """Calcula la efectividad del ataque contra la unidad oponente específica.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente.
        
        Returns
        -------
        int
            La efectividad del ataque.
        """
        if opponent.unit_type == "Infantry":
            return 1
        elif opponent.unit_type == "Cavalry" or opponent.unit_type == "Worker":
            return 0
        else:
            return -1

#--------------------
# Infantería
#--------------------
class Infantry(Unit):
    """Clase que representa una unidad de infantería.
    
    Attributes
    ----------
    name : str
        El nombre de la unidad.
    strength : int
        La fuerza de la unidad.
    defense : int
        La defensa de la unidad.
    hp : int
        Los puntos de vida actuales de la unidad.
    total_hp : int
        Los puntos de vida totales de la unidad.
    fury : int
        La furia de la unidad.
    
    Methods
    -------
    fury(self):
        Proporciona la furia de la unidad.
    fury(self, value: int):
        Escribe la furia de la unidad y comprueba que es válida.
    attack(self, opponent: "Unit") -> int:
        Ataca a la unidad oponente, infligiendo daño basado en el tipo de unidad y la furia.
    effectiveness(self, opponent: "Unit") -> int:
        Calcula la efectividad del ataque contra la unidad oponente específica.
    """
    
    def __init__(self, name: str,strength : int =3 , defense : int=2, hp : int=25, total_hp: int = 25, fury : int =3):   
        """Inicializa una unidad de infantería con atributos específicos.
        
        Parameters
        ----------
        name : str
            El nombre de la unidad.
        strength : int
            La fuerza de la unidad.
        defense : int
            La defensa de la unidad.
        hp : int
            Los puntos de vida actuales de la unidad.
        total_hp : int
            Los puntos de vida totales de la unidad.
        fury : int
            La furia de la unidad.
        
        Returns
        -------
        None.
        """
        #Toda unidad nueva creada apartir de la llamada a esta clase tendrá los siguientes atributos en su creación
        #¨Tabla 2, valores de los atributos para las unidades creadas¨
        #Lo único que es variable es el nombre de la unidad
        super().__init__(name, strength, defense, hp, total_hp, "Infantry")
        self._fury = fury

    @property
    def fury(self):
        """Proporciona la furia de la unidad.
        
        Returns
        -------
        int
            La furia de la unidad.
        """
        return self._fury

    @fury.setter
    def fury(self, value: int):
        """Escribe la furia de la unidad y comprueba que es válida.
        
        Parameters
        ----------
        value : int
            La nueva furia de la unidad.
        
        Raises
        ------
        ValueError
            Si la furia de la unidad no es un entero no negativo.
        """
        if isinstance(value, int) and value >= 0:
            self._fury = value
        else:
            raise ValueError("Fury value must be a non-negative integer")

    def attack(self, opponent: "Unit") -> int:
        """Ataca a la unidad oponente, infligiendo daño basado en el tipo de unidad y la furia.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente a la que se ataca.
        
        Returns
        -------
        int
            El daño infligido.
        """
        if opponent.unit_type == "Archer":
            factor = 1.5
        elif opponent.unit_type == "Infantry" or opponent.unit_type == "Worker":
            factor = 1
        elif opponent.unit_type == "Cavalry":
            factor = 0.5
        else:
            raise ValueError("opponent class not valid")
        #Con int redondeas al número entero anterior más cercano al decimal puesto que lo que hace int es truncar el decimal y te deja la parte entera
        dmg = max(1, int((self._fury + factor * self.strength) - opponent.defense))
        opponent.hp = max(0, opponent.hp - dmg)
        return dmg

    def effectiveness(self, opponent: "Unit") -> int:
        """Calcula la efectividad del ataque contra la unidad oponente específica.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente.
        
        Returns
        -------
        int
            La efectividad del ataque.
        """
        if opponent.unit_type == "Archer":
            return 1
        elif opponent.unit_type == "Infantry" or opponent.unit_type == "Worker":
            return 0
        else:
            return -1

#--------------------
# Trabajadores
#--------------------
class Worker(Unit):
    """Clase que representa una unidad de trabajador.
    
    Attributes
    ----------
    name : str
        El nombre de la unidad.
    strength : int
        La fuerza de la unidad.
    defense : int
        La defensa de la unidad.
    hp : int
        Los puntos de vida actuales de la unidad.
    total_hp : int
        Los puntos de vida totales de la unidad.
    
    Methods
    -------
    collect(self) -> int:
        Realiza una acción de recolección.
    effectiveness(self, opponent: "Unit") -> int:
        Calcula la efectividad del ataque contra la unidad oponente específica.
    """
    
    #def __init__(self, name: str):
    def __init__(self, name: str,strength : int =1 , defense : int=0, hp : int=5, total_hp: int = 5):  
        """Inicializa una unidad de trabajador con atributos específicos.
        
        Parameters
        ----------
        name : str
            El nombre de la unidad.
        strength : int
            La fuerza de la unidad.
        defense : int
            La defensa de la unidad.
        hp : int
            Los puntos de vida actuales de la unidad.
        total_hp : int
            Los puntos de vida totales de la unidad.
        
        Returns
        -------
        None.
        """
        #Toda unidad nueva creada apartir de la llamada a esta clase tendrá los siguientes atributos en su creación
        #¨Tabla 2, valores de los atributos para las unidades creadas¨
        #Lo único que es variable es el nombre de la unidad
        
        super().__init__(name, strength, defense, hp, total_hp, "Worker")
    
    def collect(self) -> int:
        """Realiza una acción de recolección.
        
        Returns
        -------
        int
            La cantidad recolectada.
        """
        return 10

    def effectiveness(self, opponent: "Unit") -> int:
        """Calcula la efectividad del ataque contra la unidad oponente específica.
        
        Parameters
        ----------
        opponent : Unit
            La unidad oponente.
        
        Returns
        -------
        int
            La efectividad del ataque.
        """
        return -1

# for testing things    
# if __name__ == "__main__":
#     pepito = Archer("Archer_1", 4)

#     print(pepito)
