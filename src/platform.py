"""
Classi per le piattaforme e rampe del gioco
"""
from typing import List, Tuple
import pygame
from src.config import BROWN, BLACK, GRAY, SCREEN_WIDTH, GROUND_Y


class Platform:
    """Classe per rappresentare una piattaforma"""
    
    def __init__(self, x: int, y: int, width: int, height: int = 25):
        """
        Inizializza una piattaforma (resa più spessa per miglior visibilità)
        
        Args:
            x: Posizione x della piattaforma
            y: Posizione y della piattaforma
            width: Larghezza della piattaforma
            height: Altezza della piattaforma (default 25, era 15)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Rect per collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Disegna la piattaforma
        
        Args:
            screen: Superficie pygame su cui disegnare
        """
        # Corpo principale marrone più scuro
        pygame.draw.rect(screen, (101, 67, 33), self.rect)
        
        # Bordo superiore più chiaro (effetto 3D) - più spesso
        top_rect = pygame.Rect(self.x, self.y, self.width, 6)
        pygame.draw.rect(screen, (180, 120, 70), top_rect)
        
        # Bordo inferiore più scuro - più spesso
        bottom_rect = pygame.Rect(self.x, self.y + self.height - 5, self.width, 5)
        pygame.draw.rect(screen, (60, 40, 20), bottom_rect)
        
        # Bordi laterali neri più spessi
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        
        # Linee decorative per dare texture - più visibili
        for i in range(5, self.width - 5, 25):
            line_x = self.x + i
            pygame.draw.line(screen, (140, 90, 50), 
                           (line_x, self.y + 3), 
                           (line_x, self.y + self.height - 6), 2)
                           
        # Aggiungiamo chiodi/dettagli metallici
        for i in range(15, self.width - 15, 40):
            nail_x = self.x + i
            nail_y = self.y + self.height // 2
            pygame.draw.circle(screen, GRAY, (nail_x, nail_y), 3)
            pygame.draw.circle(screen, BLACK, (nail_x, nail_y), 3, 1)
        
    def get_top_y(self) -> int:
        """
        Restituisce la coordinata Y della superficie superiore
        
        Returns:
            Coordinata Y del top della piattaforma
        """
        return self.y
        
    def contains_point(self, x: int, y: int) -> bool:
        """
        Controlla se un punto è dentro la piattaforma
        
        Args:
            x: Coordinata x del punto
            y: Coordinata y del punto
            
        Returns:
            True se il punto è dentro la piattaforma
        """
        return self.rect.collidepoint(x, y)


class Ramp:
    """Classe per rappresentare una rampa inclinata"""
    
    def __init__(self, x: int, y: int, width: int, height: int, slope_up: bool = True):
        """
        Inizializza una rampa
        
        Args:
            x: Posizione x della rampa
            y: Posizione y della base della rampa
            width: Larghezza della rampa
            height: Altezza della rampa
            slope_up: True se la rampa sale da sx a dx, False se scende
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.slope_up = slope_up
        
        # Rect approssimativo per collision detection iniziale
        self.rect = pygame.Rect(self.x, self.y - height, self.width, self.height)
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Disegna la rampa
        
        Args:
            screen: Superficie pygame su cui disegnare
        """
        # Calcola i punti del triangolo/rampa
        if self.slope_up:
            # Rampa che sale: basso-sx, basso-dx, alto-dx
            points = [
                (self.x, self.y),  # Basso sinistra
                (self.x + self.width, self.y),  # Basso destra
                (self.x + self.width, self.y - self.height),  # Alto destra
                (self.x, self.y)  # Chiude il triangolo
            ]
        else:
            # Rampa che scende: alto-sx, basso-sx, basso-dx
            points = [
                (self.x, self.y - self.height),  # Alto sinistra
                (self.x, self.y),  # Basso sinistra
                (self.x + self.width, self.y),  # Basso destra
                (self.x, self.y - self.height)  # Chiude il triangolo
            ]
        
        # Disegna il corpo della rampa
        pygame.draw.polygon(screen, BROWN, points[:-1])  # Escludi l'ultimo punto duplicato
        
        # Bordo
        pygame.draw.polygon(screen, BLACK, points[:-1], 2)
        
    def get_height_at_x(self, x_pos: int) -> int:
        """
        Calcola l'altezza della rampa a una data posizione x
        
        Args:
            x_pos: Posizione x dove calcolare l'altezza
            
        Returns:
            Altezza Y della superficie della rampa a quella x
        """
        if x_pos < self.x or x_pos > self.x + self.width:
            return self.y  # Fuori dalla rampa
            
        # Calcola la posizione relativa (0-1) lungo la rampa
        relative_x = (x_pos - self.x) / self.width
        
        if self.slope_up:
            # Rampa che sale: altezza aumenta con x
            height_offset = relative_x * self.height
            return self.y - height_offset
        else:
            # Rampa che scende: altezza diminuisce con x
            height_offset = (1 - relative_x) * self.height
            return self.y - height_offset
            
    def is_on_ramp(self, x: int, y: int, tolerance: int = 5) -> bool:
        """
        Controlla se un punto è sulla superficie della rampa
        
        Args:
            x: Posizione x
            y: Posizione y
            tolerance: Tolleranza per la collision detection
            
        Returns:
            True se il punto è sulla rampa
        """
        if x < self.x or x > self.x + self.width:
            return False
            
        expected_y = self.get_height_at_x(x)
        return abs(y - expected_y) <= tolerance


def create_default_platforms() -> List[Platform]:
    """
    Crea un set di piattaforme predefinite per il livello
    
    Returns:
        Lista di piattaforme
    """
    platforms = []
    
    # Piattaforma sinistra bassa - facile da raggiungere (più spessa)
    platforms.append(Platform(120, GROUND_Y - 80, 160, 25))
    
    # Piattaforma centrale media - ben distanziata (più spessa)
    platforms.append(Platform(320, GROUND_Y - 130, 140, 25))
    
    # Piattaforma destra media - accessibile (più spessa)
    platforms.append(Platform(540, GROUND_Y - 90, 150, 25))
    
    # Piattaforma alta sinistra - per salti avanzati (più spessa)
    platforms.append(Platform(80, GROUND_Y - 180, 120, 25))
    
    # Piattaforma alta destra - per salti avanzati (più spessa)
    platforms.append(Platform(720, GROUND_Y - 160, 130, 25))
    
    return platforms


def create_default_ramps() -> List[Ramp]:
    """
    Crea un set di rampe predefinite per il livello
    NOTA: Attualmente disabilitato - restituisce lista vuota
    
    Returns:
        Lista vuota (rampe disabilitate)
    """
    ramps = []
    
    # Rampe disabilitate per migliorare il gameplay
    # Focus solo su piattaforme orizzontali
    
    return ramps


def check_platform_collision(player_rect: pygame.Rect, player_vel_y: int, platforms: List[Platform]) -> Tuple[bool, int]:
    """
    Controlla le collisioni del player con le piattaforme
    
    Args:
        player_rect: Rect del player
        player_vel_y: Velocità verticale del player
        platforms: Lista di piattaforme
        
    Returns:
        Tupla (is_on_platform, platform_y) - True se su piattaforma e Y della piattaforma
    """
    if player_vel_y <= 0:  # Solo se sta cadendo
        return False, 0
        
    # Controlla ogni piattaforma
    for platform in platforms:
        # Il player deve essere sopra la piattaforma e in caduta
        # Collision detection migliorata per precisione
        if (player_rect.bottom <= platform.get_top_y() + 8 and 
            player_rect.bottom >= platform.get_top_y() - 3 and
            player_rect.right > platform.x + 5 and 
            player_rect.left < platform.x + platform.width - 5):
            return True, platform.get_top_y()
            
    return False, 0


def check_ramp_collision(player_rect: pygame.Rect, ramps: List[Ramp]) -> Tuple[bool, int]:
    """
    Controlla le collisioni del player con le rampe
    
    Args:
        player_rect: Rect del player
        ramps: Lista di rampe
        
    Returns:
        Tupla (is_on_ramp, ramp_y) - True se su rampa e Y della superficie della rampa
    """
    player_center_x = player_rect.centerx
    player_bottom = player_rect.bottom
    
    for ramp in ramps:
        if ramp.is_on_ramp(player_center_x, player_bottom, tolerance=10):
            ramp_surface_y = ramp.get_height_at_x(player_center_x)
            return True, ramp_surface_y
            
    return False, 0 