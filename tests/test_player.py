"""
Test unitari per la classe Player
"""
import unittest
from unittest.mock import Mock, patch
import pygame
from src.player import Player
from src.config import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_SPEED,
    PLAYER_MAX_HEALTH, GROUND_Y, KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_ATTACK
)


class TestPlayer(unittest.TestCase):
    """Test per la classe Player"""

    def setUp(self):
        """Setup per ogni test"""
        pygame.init()
        self.player = Player(100, 200)
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()

    def test_init(self):
        """Test inizializzazione del player"""
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 200)
        self.assertEqual(self.player.width, PLAYER_WIDTH)
        self.assertEqual(self.player.height, PLAYER_HEIGHT)
        self.assertEqual(self.player.health, PLAYER_MAX_HEALTH)
        self.assertTrue(self.player.facing_right)
        self.assertFalse(self.player.is_attacking)
        self.assertEqual(self.player.resources["oro"], 0)
        self.assertEqual(self.player.resources["argento"], 0)
        self.assertEqual(self.player.resources["mirra"], 0)

    def test_movement_left(self):
        """Test movimento verso sinistra"""
        initial_x = self.player.x
        keys = {KEY_LEFT: True}
        self.player._handle_input(keys)
        
        self.assertEqual(self.player.x, initial_x - PLAYER_SPEED)
        self.assertFalse(self.player.facing_right)

    def test_movement_right(self):
        """Test movimento verso destra"""
        initial_x = self.player.x
        keys = {KEY_RIGHT: True}
        self.player._handle_input(keys)
        
        self.assertEqual(self.player.x, initial_x + PLAYER_SPEED)
        self.assertTrue(self.player.facing_right)

    def test_jump_on_ground(self):
        """Test salto quando il player è a terra"""
        self.player.on_ground = True
        keys = {KEY_JUMP: True}
        self.player._handle_input(keys)
        
        self.assertEqual(self.player.vel_y, PLAYER_JUMP_SPEED)
        self.assertFalse(self.player.on_ground)

    def test_jump_in_air(self):
        """Test che non si può saltare quando si è in aria"""
        self.player.on_ground = False
        initial_vel_y = self.player.vel_y
        keys = {KEY_JUMP: True}
        self.player._handle_input(keys)
        
        self.assertEqual(self.player.vel_y, initial_vel_y)

    def test_attack(self):
        """Test attacco"""
        keys = {KEY_ATTACK: True}
        self.player._handle_input(keys)
        
        self.assertTrue(self.player.is_attacking)
        self.assertEqual(self.player.attack_timer, 0)

    def test_attack_duration(self):
        """Test durata dell'attacco"""
        self.player.start_attack()
        
        # Simula alcuni frame
        for _ in range(self.player.attack_duration):
            self.player._update_attack()
            
        self.assertFalse(self.player.is_attacking)
        self.assertEqual(self.player.attack_timer, 0)

    def test_gravity(self):
        """Test applicazione della gravità"""
        self.player.on_ground = False
        initial_vel_y = self.player.vel_y
        self.player._apply_gravity()
        
        self.assertEqual(self.player.vel_y, initial_vel_y + 1)  # GRAVITY = 1

    def test_ground_collision(self):
        """Test collisione con il terreno"""
        self.player.y = GROUND_Y  # Oltre il terreno
        self.player.vel_y = 5
        self.player._update_position()
        
        self.assertEqual(self.player.y, GROUND_Y - self.player.height)
        self.assertEqual(self.player.vel_y, 0)
        self.assertTrue(self.player.on_ground)

    def test_take_damage(self):
        """Test subire danno"""
        initial_health = self.player.health
        damage = 20
        self.player.take_damage(damage)
        
        self.assertEqual(self.player.health, initial_health - damage)

    def test_take_damage_below_zero(self):
        """Test che la salute non va sotto zero"""
        self.player.take_damage(200)  # Danno maggiore della salute massima
        self.assertEqual(self.player.health, 0)

    def test_heal(self):
        """Test cure"""
        self.player.health = 50
        self.player.heal(30)
        
        self.assertEqual(self.player.health, 80)

    def test_heal_above_max(self):
        """Test che la salute non va sopra il massimo"""
        self.player.health = 90
        self.player.heal(50)
        
        self.assertEqual(self.player.health, PLAYER_MAX_HEALTH)

    def test_collect_resource(self):
        """Test raccolta risorse"""
        self.player.collect_resource("oro", 5)
        self.player.collect_resource("argento", 3)
        self.player.collect_resource("mirra", 2)
        
        self.assertEqual(self.player.resources["oro"], 5)
        self.assertEqual(self.player.resources["argento"], 3)
        self.assertEqual(self.player.resources["mirra"], 2)

    def test_collect_invalid_resource(self):
        """Test raccolta risorsa non valida"""
        initial_resources = self.player.resources.copy()
        self.player.collect_resource("diamante", 1)  # Risorsa non esistente
        
        self.assertEqual(self.player.resources, initial_resources)

    def test_is_alive_healthy(self):
        """Test is_alive con salute > 0"""
        self.assertTrue(self.player.is_alive())

    def test_is_alive_dead(self):
        """Test is_alive con salute = 0"""
        self.player.health = 0
        self.assertFalse(self.player.is_alive())

    def test_get_attack_rect_not_attacking(self):
        """Test get_attack_rect quando non sta attaccando"""
        attack_rect = self.player.get_attack_rect()
        self.assertEqual(attack_rect.width, 0)
        self.assertEqual(attack_rect.height, 0)

    def test_get_attack_rect_attacking_right(self):
        """Test get_attack_rect quando attacca verso destra"""
        self.player.facing_right = True
        self.player.start_attack()
        attack_rect = self.player.get_attack_rect()
        
        self.assertEqual(attack_rect.x, self.player.x + self.player.width)
        self.assertEqual(attack_rect.width, 40)
        self.assertEqual(attack_rect.height, 20)

    def test_get_attack_rect_attacking_left(self):
        """Test get_attack_rect quando attacca verso sinistra"""
        self.player.facing_right = False
        self.player.start_attack()
        attack_rect = self.player.get_attack_rect()
        
        self.assertEqual(attack_rect.x, self.player.x - 40)
        self.assertEqual(attack_rect.width, 40)
        self.assertEqual(attack_rect.height, 20)

    def test_get_set_position(self):
        """Test get_position e set_position"""
        new_x, new_y = 300, 400
        self.player.set_position(new_x, new_y)
        
        self.assertEqual(self.player.get_position(), (new_x, new_y))
        self.assertEqual(self.player.rect.x, new_x)
        self.assertEqual(self.player.rect.y, new_y)

    def test_update_integration(self):
        """Test integrazione del metodo update"""
        keys = {KEY_RIGHT: True, KEY_JUMP: True}
        self.player.on_ground = True
        initial_x = self.player.x
        
        self.player.update(keys)
        
        # Dovrebbe essersi mosso a destra e aver saltato
        self.assertEqual(self.player.x, initial_x + PLAYER_SPEED)
        # Dopo update(), il player ha saltato (PLAYER_JUMP_SPEED) e subito la gravità (+1)
        self.assertEqual(self.player.vel_y, PLAYER_JUMP_SPEED + 1)  # -15 + 1 = -14
        self.assertFalse(self.player.on_ground)
        self.assertTrue(self.player.facing_right)


if __name__ == "__main__":
    unittest.main() 