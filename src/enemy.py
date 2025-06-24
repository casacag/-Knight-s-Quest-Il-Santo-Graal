"""Classi per i nemici del gioco"""
from typing import Tuple
import pygame
import random
from abc import ABC, abstractmethod
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, RED, BLACK, GRAY,
    DEMON_HP, DEMON_ATTACK_DAMAGE, BOSS_HP, BOSS_ATTACK_DAMAGE
)
from src.sprite_manager import sprite_manager


class Enemy(ABC):
    """Classe base astratta per tutti i nemici"""
    
    def __init__(self, x: int, y: int, width: int, height: int, health: int, speed: int):
        """Inizializza il nemico base"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = health
        self.health = health
        self.speed = speed
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 20
        self.attack_cooldown = 60
        self.attack_cooldown_timer = 0
        self.damage_dealt_this_attack = False  # Previene danni multipli per attacco
        self.is_alive_flag = True
        
        # AI state
        self.ai_state = "patrol"
        self.patrol_direction = 1 if random.choice([True, False]) else -1
        self.patrol_distance = random.randint(100, 200)
        self.start_x = x
        
        # Rect per collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, player_x: int, player_y: int) -> None:
        """Aggiorna il nemico"""
        if not self.is_alive_flag:
            return
            
        self._update_ai(player_x, player_y)
        self._apply_gravity()
        self._update_attack()
        self._update_position()
        
    def _update_ai(self, player_x: int, player_y: int) -> None:
        """Aggiorna l'IA del nemico"""
        distance_to_player = abs(player_x - self.x)
        
        if self.ai_state == "patrol":
            self._patrol_behavior()
            if distance_to_player < 150:
                self.ai_state = "chase"
                
        elif self.ai_state == "chase":
            self._chase_behavior(player_x)
            # Distanza di attacco ridotta per evitare sovrapposizioni
            if distance_to_player < 70:  # Era 50, ora 70 per più spazio
                self.ai_state = "attack"
            elif distance_to_player > 250:
                self.ai_state = "patrol"
                
        elif self.ai_state == "attack":
            self._attack_behavior(player_x)
            # Aumentata la distanza per uscire dalla modalità attacco
            if distance_to_player > 100:  # Era 80, ora 100
                self.ai_state = "chase"
                
    def _patrol_behavior(self) -> None:
        """Comportamento di pattugliamento"""
        self.x += self.speed * self.patrol_direction * 0.5
        
        if abs(self.x - self.start_x) > self.patrol_distance:
            self.patrol_direction *= -1
            self.facing_right = self.patrol_direction > 0
            
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.patrol_direction *= -1
            self.facing_right = self.patrol_direction > 0
            
    def _chase_behavior(self, player_x: int) -> None:
        """Comportamento di inseguimento"""
        if player_x > self.x:
            self.x += self.speed
            self.facing_right = True
        elif player_x < self.x:
            self.x -= self.speed
            self.facing_right = False
            
    def _attack_behavior(self, player_x: int) -> None:
        """Comportamento di attacco"""
        self.facing_right = player_x > self.x
        
        if not self.is_attacking and self.attack_cooldown_timer <= 0:
            self.start_attack()
            
    def _apply_gravity(self) -> None:
        """Applica la gravità"""
        if not self.on_ground:
            self.vel_y += 1
            
    def _update_attack(self) -> None:
        """Aggiorna lo stato dell'attacco"""
        if self.is_attacking:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
                self.attack_cooldown_timer = self.attack_cooldown
                
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1
            
    def _update_position(self) -> None:
        """Aggiorna la posizione"""
        self.y += self.vel_y
        
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    def start_attack(self) -> None:
        """Inizia un attacco"""
        if self.attack_cooldown_timer <= 0:
            self.is_attacking = True
            self.attack_timer = 0
            self.damage_dealt_this_attack = False
            
    def get_attack_rect(self) -> pygame.Rect:
        """Restituisce il rettangolo dell'attacco"""
        if not self.is_attacking:
            return pygame.Rect(0, 0, 0, 0)
            
        attack_width = 35
        attack_height = 25
        
        if self.facing_right:
            attack_x = self.x + self.width
        else:
            attack_x = self.x - attack_width
            
        attack_y = self.y + self.height // 3
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)
        
    def take_damage(self, damage: int) -> None:
        """Il nemico subisce danno"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive_flag = False
            self.ai_state = "dead"
            
    def is_alive(self) -> bool:
        """Controlla se il nemico è vivo"""
        return self.is_alive_flag
        
    def get_damage(self) -> int:
        """Restituisce il danno che infligge questo nemico"""
        return 15
        
    def get_position(self) -> Tuple[int, int]:
        """Restituisce la posizione del nemico"""
        return (self.x, self.y)
        
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Disegna il nemico sullo schermo"""
        pass


class DemonArmed(Enemy):
    """Demone armato - nemico corpo a corpo"""
    
    def __init__(self, x: int, y: int, is_boss: bool = False):
        """Inizializza il demone armato"""
        if is_boss:
            # Boss è più grande e forte (richiede 10 colpi per morire)
            super().__init__(x, y, width=80, height=110, health=BOSS_HP, speed=1)
            self.enemy_type = "boss"
        else:
            # Demoni normali (richiedono 3 colpi per morire)
            super().__init__(x, y, width=56, height=74, health=DEMON_HP, speed=2)
            self.enemy_type = "demon_armed"
        
        self.is_boss = is_boss
        
    def get_damage(self) -> int:
        """Restituisce il danno del demone armato"""
        return BOSS_ATTACK_DAMAGE if self.is_boss else DEMON_ATTACK_DAMAGE
        
    def draw(self, screen: pygame.Surface) -> None:
        """Disegna il demone armato sullo schermo"""
        if not self.is_alive_flag:
            return
            
        # Carica lo sprite appropriato (demone normale o boss)
        sprite = sprite_manager.get_enemy_sprite(
            is_boss=self.is_boss,
            size=(self.width, self.height)
        )
        
        # Capovolgi l'immagine se il nemico sta guardando a sinistra
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Disegna lo sprite
        screen.blit(sprite, (self.x, self.y))
        
        # Se sta attaccando, disegna un'area di attacco semi-trasparente
        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            attack_surface = pygame.Surface((attack_rect.width, attack_rect.height))
            attack_surface.set_alpha(120)  # Semi-trasparente
            attack_color = (255, 0, 0) if self.is_boss else (255, 100, 0)  # Rosso per boss, arancione per demoni
            attack_surface.fill(attack_color)
            screen.blit(attack_surface, (attack_rect.x, attack_rect.y))
            
        # Barra della vita (se danneggiato)
        if self.health < self.max_health:
            self._draw_health_bar(screen)
            
    def _draw_health_bar(self, screen: pygame.Surface) -> None:
        """Disegna la barra della vita sopra il nemico"""
        bar_width = self.width
        bar_height = 4
        bar_x = self.x
        bar_y = self.y - 8
        
        # Sfondo barra (rosso)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, RED, bg_rect)
        
        # Barra vita attuale (verde)
        if self.health > 0:
            health_percentage = self.health / self.max_health
            health_width = int(bar_width * health_percentage)
            health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
            color = (0, 255, 0) if health_percentage > 0.3 else (255, 165, 0)
            pygame.draw.rect(screen, color, health_rect)
