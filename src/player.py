"""
Classe Player per il cavaliere protagonista
"""
from typing import Dict, List, Tuple
import pygame
from src.config import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_SPEED,
    PLAYER_MAX_HEALTH, GRAVITY, GROUND_Y, WHITE, BROWN, SILVER,
    KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_ATTACK, SCREEN_WIDTH
)
from src.sprite_manager import sprite_manager


class Player:
    """Classe che rappresenta il cavaliere protagonista"""
    
    def __init__(self, x: int, y: int):
        """
        Inizializza il player
        
        Args:
            x: Posizione x iniziale
            y: Posizione y iniziale
        """
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.health = PLAYER_MAX_HEALTH
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 15  # frames
        self.damage_dealt_this_attack = False  # Previene danni multipli per attacco
        
        # Inventario risorse
        self.resources: Dict[str, int] = {
            "oro": 0,
            "argento": 0,
            "mirra": 0
        }
        
        # Rect per collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, keys_pressed: Dict[int, bool], platforms: list = None) -> None:
        """
        Aggiorna lo stato del player
        
        Args:
            keys_pressed: Dizionario dei tasti premuti
            platforms: Lista di piattaforme (opzionale)
        """
        self._handle_input(keys_pressed)
        self._apply_gravity()
        self._update_attack()
        self._update_position(platforms)
        
    def _handle_input(self, keys_pressed: Dict[int, bool]) -> None:
        """Gestisce l'input del giocatore"""
        # Movimento orizzontale
        if keys_pressed.get(KEY_LEFT, False):
            self.x -= self.speed
            self.facing_right = False
            
        if keys_pressed.get(KEY_RIGHT, False):
            self.x += self.speed
            self.facing_right = True
            
        # Salto
        if keys_pressed.get(KEY_JUMP, False) and self.on_ground:
            self.vel_y = PLAYER_JUMP_SPEED
            self.on_ground = False
            
        # Attacco
        if keys_pressed.get(KEY_ATTACK, False) and not self.is_attacking:
            self.start_attack()
            
    def _apply_gravity(self) -> None:
        """Applica la gravità al player"""
        if not self.on_ground:
            self.vel_y += GRAVITY
            
    def _update_attack(self) -> None:
        """Aggiorna lo stato dell'attacco"""
        if self.is_attacking:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0
                
    def _update_position(self, platforms: list = None) -> None:
        """
        Aggiorna la posizione del player
        
        Args:
            platforms: Lista di piattaforme (opzionale)
        """
        if platforms is None:
            platforms = []
            
        # Aggiorna posizione Y
        self.y += self.vel_y
        
        # Controlla limiti orizzontali
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        
        # Crea rect per collision detection
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Controlla collisioni con piattaforme (solo se sta cadendo)
        if self.vel_y > 0 and platforms:  # Sta cadendo
            from src.platform import check_platform_collision
            is_on_platform, platform_y = check_platform_collision(player_rect, self.vel_y, platforms)
            if is_on_platform:
                self.y = platform_y - self.height
                self.vel_y = 0
                self.on_ground = True
                self.rect.x = self.x
                self.rect.y = self.y
                return
            
        # Controlla collisione con il terreno
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Aggiorna il rect
        self.rect.x = self.x
        self.rect.y = self.y
        
    def start_attack(self) -> None:
        """Inizia un attacco"""
        self.is_attacking = True
        self.attack_timer = 0
        self.damage_dealt_this_attack = False
        
    def get_attack_rect(self) -> pygame.Rect:
        """
        Restituisce il rettangolo dell'attacco
        
        Returns:
            Rect dell'area di attacco
        """
        if not self.is_attacking:
            return pygame.Rect(0, 0, 0, 0)
            
        attack_width = 40
        attack_height = 20
        
        if self.facing_right:
            attack_x = self.x + self.width
        else:
            attack_x = self.x - attack_width
            
        attack_y = self.y + self.height // 3
        
        return pygame.Rect(attack_x, attack_y, attack_width, attack_height)
        
    def take_damage(self, damage: int) -> None:
        """
        Il player subisce danno
        
        Args:
            damage: Quantità di danno
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0
            
    def heal(self, amount: int) -> None:
        """
        Cura il player
        
        Args:
            amount: Quantità di cure
        """
        self.health += amount
        if self.health > PLAYER_MAX_HEALTH:
            self.health = PLAYER_MAX_HEALTH
            
    def collect_resource(self, resource_type: str, amount: int = 1) -> None:
        """
        Raccoglie una risorsa
        
        Args:
            resource_type: Tipo di risorsa ("oro", "argento", "mirra")
            amount: Quantità da raccogliere
        """
        if resource_type in self.resources:
            self.resources[resource_type] += amount
            
    def is_alive(self) -> bool:
        """
        Controlla se il player è vivo
        
        Returns:
            True se vivo, False altrimenti
        """
        return self.health > 0
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Disegna il player sullo schermo
        
        Args:
            screen: Superficie pygame su cui disegnare
        """
        # Carica lo sprite appropriato (cavaliere a riposo o in attacco)
        sprite = sprite_manager.get_player_sprite(
            attacking=self.is_attacking,
            size=(self.width, self.height)
        )
        
        # Capovolgi l'immagine se il player sta guardando a sinistra
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        # Disegna lo sprite
        screen.blit(sprite, (self.x, self.y))
        
        # Se sta attaccando, disegna un'area di attacco semi-trasparente
        if self.is_attacking:
            attack_rect = self.get_attack_rect()
            attack_surface = pygame.Surface((attack_rect.width, attack_rect.height))
            attack_surface.set_alpha(100)  # Semi-trasparente
            attack_surface.fill((255, 255, 0))  # Giallo per evidenziare l'attacco
            screen.blit(attack_surface, (attack_rect.x, attack_rect.y))
            
    def get_position(self) -> Tuple[int, int]:
        """
        Restituisce la posizione del player
        
        Returns:
            Tupla (x, y) della posizione
        """
        return (self.x, self.y)
        
    def set_position(self, x: int, y: int) -> None:
        """
        Imposta la posizione del player
        
        Args:
            x: Nuova posizione x
            y: Nuova posizione y
        """
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y 