#!/usr/bin/env python3
"""
python test_units.py -v 
"""

import math
import unittest
from unit import Archer, Cavalry, Infantry, Worker

# ============================================================================
# Generic Tests for the Base Unit Methods (via any subclass)
# ============================================================================

class TestUnitProperties(unittest.TestCase):
    def test_name_setter_and_getter(self):
        unit = Infantry(name="OldName", strength=30, defense=30, hp=50, total_hp=50, fury=3)
        self.assertEqual(unit.name, "OldName")
        unit.name = "NewName"
        self.assertEqual(unit.name, "NewName")

    def test_strength_setter_and_getter(self):
        unit = Cavalry(name="Test", strength=40, defense=20, hp=60, total_hp=60, charge=5)
        unit.strength = 100
        self.assertEqual(unit.strength, 100)

    def test_defense_setter_and_getter(self):
        unit = Archer(name="Test", strength=60, defense=20, hp=30, total_hp=30, arrows=3)
        unit.defense = 50
        self.assertEqual(unit.defense, 50)

    def test_total_hp_setter_and_getter(self):
        unit = Worker(name="Test", strength=1, defense=0, hp=5, total_hp=5)
        unit.total_hp = 10
        self.assertEqual(unit.total_hp, 10)

    def test_hp_setter_clamps_negative(self):
        unit = Archer(name="Test", strength=60, defense=20, hp=30, total_hp=30, arrows=3)
        unit.hp = -5
        self.assertEqual(unit.hp, 0)

    def test_is_debilitated_true(self):
        unit = Infantry(name="Test", strength=30, defense=30, hp=50, total_hp=50, fury=3)
        unit.hp = 0
        self.assertTrue(unit.is_debilitated())

    def test_is_debilitated_false(self):
        unit = Cavalry(name="Test", strength=40, defense=20, hp=60, total_hp=60, charge=5)
        unit.hp = 10
        self.assertFalse(unit.is_debilitated())

    def test_str_method_contains_expected_info(self):
        unit = Infantry(name="Arthur", strength=35, defense=40, hp=55, total_hp=55, fury=4)
        s = str(unit)
        self.assertIn("Arthur", s)
        self.assertIn("Infantry", s)
        self.assertIn("ATT", s)
        self.assertIn("DEF", s)
        self.assertIn("HP", s)


# ============================================================================
# Tests for Archer
# ============================================================================

class TestArcherInitialization(unittest.TestCase):
    def test_explicit_initialization(self):
        # Explicit values for Archer.
        name = "Legolas"
        strength = 70
        defense = 25
        hp = 35
        total_hp = 35
        arrows = 3  # Use 3 arrows so that one attack decrements to 2.
        
        archer = Archer(name=name, strength=strength, defense=defense, hp=hp, 
                        total_hp=total_hp, arrows=arrows)
        
        self.assertEqual(archer.name, name)
        self.assertEqual(archer.unit_type, "Archer")  # Set internally in the constructor.
        self.assertEqual(archer.strength, strength)
        self.assertEqual(archer.defense, defense)
        self.assertEqual(archer.hp, hp)
        self.assertEqual(archer.total_hp, total_hp)
        self.assertEqual(archer.arrows, arrows)

class TestArcherStr(unittest.TestCase):
    def test_str_output(self):
        archer = Archer(name="Legolas", strength=70, defense=25, hp=35, total_hp=35, arrows=3)
        s = str(archer)
        self.assertIn("Legolas", s)
        self.assertIn("Archer", s)
        self.assertIn("ATT", s)
        self.assertIn("DEF", s)
        self.assertIn("HP", s)

class TestArcherAttack(unittest.TestCase):
    def setUp(self):
        self.archer = Archer(name="Legolas", strength=70, defense=25, hp=50, 
                             total_hp=50, arrows=3)  

    def test_attack_vs_cavalry(self):
        enemy = Cavalry(name="Enemy Cavalry", strength=50, defense=30, hp=100, total_hp=100, 
                        charge=10) 
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(1.5 * self.archer.strength - enemy.defense))
        damage = self.archer.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)        
        self.assertEqual(self.archer.arrows, 2)

    def test_attack_vs_archer(self):
        enemy = Archer(name="Enemy Archer", strength=70, defense=25, hp=80, 
                       total_hp=80, arrows=3) 
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(1 * self.archer.strength - enemy.defense))
        damage = self.archer.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)
        self.assertEqual(self.archer.arrows, 2)

    def test_attack_vs_infantry(self):
        enemy = Infantry(name="Enemy Infantry", strength=35, defense=40, hp=90, total_hp=90, fury=4)  
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(0.5 * self.archer.strength - enemy.defense))
        damage = self.archer.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)
        self.assertEqual(self.archer.arrows, 2)

    def test_attack_with_no_arrows(self):
        archer = Archer(name="NoArrows", strength=70, defense=25, hp=50, total_hp=50, arrows=0)  
        enemy = Infantry(name="Enemy Infantry", strength=35, defense=40, hp=60, total_hp=60, fury=4) 
        initial_hp = enemy.hp
        damage = archer.attack(enemy)
        self.assertEqual(damage, 1)  # Should always be 1 if no arrows left
        self.assertEqual(enemy.hp, initial_hp - 1)


class TestArcherEffectiveness(unittest.TestCase):
    def setUp(self):
        self.archer = Archer(name="Legolas", strength=70, defense=25, hp=35, total_hp=35, arrows=3)
        self.cavalry = Cavalry(name="Lancelot", strength=50, defense=30, hp=70, total_hp=70, charge=10)
        self.infantry = Infantry(name="Arthur", strength=35, defense=40, hp=55, total_hp=55, fury=4)
        self.archer2 = Archer(name="GreenArrow", strength=70, defense=25, hp=35, total_hp=35, arrows=3)
        self.worker = Worker(name="Bob", strength=1, defense=0, hp=5, total_hp=5)

    def test_effectiveness_vs_cavalry(self):
        self.assertEqual(self.archer.effectiveness(self.cavalry), 1)

    def test_effectiveness_vs_archer(self):
        self.assertEqual(self.archer.effectiveness(self.archer2), 0)

    def test_effectiveness_vs_infantry(self):
        self.assertEqual(self.archer.effectiveness(self.infantry), -1)

    def test_effectiveness_vs_worker(self):
        self.assertEqual(self.archer.effectiveness(self.worker), 0)


# ============================================================================
# Tests for Cavalry
# ============================================================================

class TestCavalryInitialization(unittest.TestCase):
    def test_explicit_initialization(self):
        name = "Lancelot"
        strength = 50
        defense = 30
        hp = 70
        total_hp = 70
        charge = 10
        
        cavalry = Cavalry(name=name, strength=strength, defense=defense, hp=hp, 
                          total_hp=total_hp, charge=charge)
        
        self.assertEqual(cavalry.name, name)
        self.assertEqual(cavalry.unit_type, "Cavalry")
        self.assertEqual(cavalry.strength, strength)
        self.assertEqual(cavalry.defense, defense)
        self.assertEqual(cavalry.hp, hp)
        self.assertEqual(cavalry.total_hp, total_hp)
        self.assertEqual(cavalry.charge, charge)

class TestCavalryStr(unittest.TestCase):
    def test_str_output(self):
        cavalry = Cavalry(name="Lancelot", strength=50, defense=30, hp=70, total_hp=70, 
                          charge=10)
        s = str(cavalry)
        self.assertIn("Lancelot", s)
        self.assertIn("Cavalry", s)
        self.assertIn("ATT", s)
        self.assertIn("DEF", s)
        self.assertIn("HP", s)


class TestCavalryAttack(unittest.TestCase):
    def setUp(self):
        self.cavalry = Cavalry(name="Lancelot", strength=50, defense=30, hp=80, total_hp=80, 
                               charge=10) 

    def test_attack_vs_infantry(self):
        enemy = Infantry(name="Enemy Infantry", strength=35, defense=40, hp=110, total_hp=110, fury=4)  # HP = 110
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(self.cavalry.charge + 1.5 * self.cavalry.strength - enemy.defense))
        damage = self.cavalry.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)

    def test_attack_vs_cavalry(self):
        enemy = Cavalry(name="Enemy Cavalry", strength=50, defense=30, hp=90, total_hp=90, 
                        charge=10) 
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(self.cavalry.charge + 1 * self.cavalry.strength - enemy.defense))
        damage = self.cavalry.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)

    def test_attack_vs_archer(self):
        enemy = Archer(name="Enemy Archer", strength=70, defense=25, hp=100, total_hp=100, arrows=3)  # HP = 100
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(self.cavalry.charge + 0.5 * self.cavalry.strength - enemy.defense))
        damage = self.cavalry.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)



class TestCavalryEffectiveness(unittest.TestCase):
    def setUp(self):
        self.cavalry = Cavalry(name="Lancelot", strength=50, defense=30, hp=70, total_hp=70, charge=10)
        self.infantry = Infantry(name="Arthur", strength=35, defense=40, hp=55, total_hp=55, fury=4)
        self.cavalry2 = Cavalry(name="Knight", strength=50, defense=30, hp=70, total_hp=70, charge=10)
        self.archer = Archer(name="Legolas", strength=70, defense=25, hp=35, total_hp=35, arrows=3)
        self.worker = Worker(name="Bob", strength=1, defense=0, hp=5, total_hp=5)

    def test_effectiveness_vs_infantry(self):
        self.assertEqual(self.cavalry.effectiveness(self.infantry), 1)

    def test_effectiveness_vs_cavalry(self):
        self.assertEqual(self.cavalry.effectiveness(self.cavalry2), 0)

    def test_effectiveness_vs_archer(self):
        self.assertEqual(self.cavalry.effectiveness(self.archer), -1)

    def test_effectiveness_vs_worker(self):
        self.assertEqual(self.cavalry.effectiveness(self.worker), 0)


# ============================================================================
# Tests for Infantry
# ============================================================================

class TestInfantryInitialization(unittest.TestCase):
    def test_explicit_initialization(self):
        name = "Arthur"
        strength = 35
        defense = 40
        hp = 55
        total_hp = 55
        fury = 4
        
        infantry = Infantry(name=name, strength=strength, defense=defense, hp=hp, 
                            total_hp=total_hp, fury=fury)
        
        self.assertEqual(infantry.name, name)
        self.assertEqual(infantry.unit_type, "Infantry")
        self.assertEqual(infantry.strength, strength)
        self.assertEqual(infantry.defense, defense)
        self.assertEqual(infantry.hp, hp)
        self.assertEqual(infantry.total_hp, total_hp)
        self.assertEqual(infantry.fury, fury)

class TestInfantryStr(unittest.TestCase):
    def test_str_output(self):
        infantry = Infantry(name="Arthur",strength=35, defense=40, hp=55, total_hp=55, fury=4)
        s = str(infantry)
        self.assertIn("Arthur", s)
        self.assertIn("Infantry", s)
        self.assertIn("ATT", s)
        self.assertIn("DEF", s)
        self.assertIn("HP", s)

class TestInfantryAttack(unittest.TestCase):
    def setUp(self):
        self.infantry = Infantry(name="Arthur", strength=35, defense=40, hp=100, 
                                 total_hp=100, fury=4)  

    def test_attack_vs_archer(self):
        enemy = Archer(name="Enemy Archer", strength=70, defense=25, hp=130, 
                       total_hp=130, arrows=3)
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(self.infantry.fury + 1.5 * self.infantry.strength - enemy.defense))
        damage = self.infantry.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)


    def test_attack_vs_infantry(self):
        enemy = Infantry(name="Enemy Infantry", strength=35, defense=40, hp=120, 
                         total_hp=120, fury=4) 
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(self.infantry.fury + 1 * self.infantry.strength - enemy.defense))
        damage = self.infantry.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)

    def test_attack_vs_cavalry(self):
        enemy = Cavalry(name="Enemy Cavalry", strength=50, 
                        defense=30, hp=110, total_hp=110, charge=10)  # HP = 110
        initial_hp = enemy.hp
        expected_damage = max(1, math.floor(self.infantry.fury + 0.5 * self.infantry.strength - enemy.defense))
        damage = self.infantry.attack(enemy)
        self.assertEqual(damage, expected_damage)
        self.assertEqual(enemy.hp, initial_hp - expected_damage)


class TestInfantryEffectiveness(unittest.TestCase):
    def setUp(self):
        self.infantry = Infantry(name="Arthur", strength=35, defense=40, hp=55, total_hp=55, fury=4)
        self.archer = Archer(name="Legolas", strength=70, defense=25, hp=35, total_hp=35, arrows=3)
        self.infantry2 = Infantry(name="Soldier", strength=35, defense=40, hp=55, total_hp=55, fury=4)
        self.cavalry = Cavalry(name="Lancelot", strength=50, defense=30, hp=70, total_hp=70, charge=10)
        self.worker = Worker(name="Bob", strength=1, defense=0, hp=5, total_hp=5)

    def test_effectiveness_vs_archer(self):
        self.assertEqual(self.infantry.effectiveness(self.archer), 1)

    def test_effectiveness_vs_infantry(self):
        self.assertEqual(self.infantry.effectiveness(self.infantry2), 0)

    def test_effectiveness_vs_cavalry(self):
        self.assertEqual(self.infantry.effectiveness(self.cavalry), -1)

    def test_effectiveness_vs_worker(self):
        self.assertEqual(self.infantry.effectiveness(self.worker), 0)

# ============================================================================
# Tests for Worker
# ============================================================================

class TestWorkerInitialization(unittest.TestCase):
    def test_explicit_initialization(self):
        worker = Worker(name="Bob", strength=1, defense=0, hp=5, total_hp=5)
        self.assertEqual(worker.name, "Bob")
        self.assertEqual(worker.unit_type, "Worker")
        self.assertEqual(worker.strength, 1)
        self.assertEqual(worker.defense, 0)
        self.assertEqual(worker.hp, 5)
        self.assertEqual(worker.total_hp, 5)

class TestWorkerStr(unittest.TestCase):
    def test_str_output(self):
        worker = Worker(name="Bob", strength=1, defense=0, hp=5, total_hp=5)
        s = str(worker)
        self.assertIn("Bob", s)
        self.assertIn("Worker", s)
        self.assertIn("ATT", s)
        self.assertIn("DEF", s)
        self.assertIn("HP", s)

class TestWorkerAttack(unittest.TestCase):
    def setUp(self):
        self.worker = Worker(name="Bob", strength=2, defense=1, hp=6, total_hp=6)

    def test_attack(self):
        enemy = Infantry(name="Enemy Infantry", strength=35, defense=40, hp=55, total_hp=55, fury=4)
        initial_hp = enemy.hp
        damage = self.worker.attack(enemy) 
        self.assertEqual(damage, 1)
        self.assertEqual(enemy.hp, initial_hp - 1)

class TestWorkerCollect(unittest.TestCase):
    def setUp(self):
        self.worker = Worker(name="Bob", strength=2, defense=1, hp=6, total_hp=6)

class TestWorkerEffectiveness(unittest.TestCase):
    def test_effectiveness_always_minus_one(self):
        worker = Worker(name="Bob", strength=1, defense=0, hp=5, total_hp=5)
        archer = Archer(name="Legolas", strength=70, defense=25, hp=35, total_hp=35, arrows=3)
        cavalry = Cavalry(name="Lancelot", strength=50, defense=30, hp=70, total_hp=70, charge=10)
        infantry = Infantry(name="Arthur", strength=35, defense=40, hp=55, total_hp=55, fury=4)
        self.assertEqual(worker.effectiveness(archer), -1)
        self.assertEqual(worker.effectiveness(cavalry), -1)
        self.assertEqual(worker.effectiveness(infantry), -1)
        self.assertEqual(worker.effectiveness(worker), -1)


# ============================================================================
# Run all the tests
# ============================================================================

if __name__ == '__main__':
    unittest.main()
