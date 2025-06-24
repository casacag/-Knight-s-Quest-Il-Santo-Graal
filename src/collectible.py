"""
Classi per gli oggetti collezionabili del gioco
"""
from typing import Tuple
import pygame
import random
from abc import ABC, abstractmethod
from src.config import (
    COLLECTIBLE_SIZE, GOLD_VALUE, SILVER_VALUE, MYRRH_VALUE,
    GOLD_HEAL_AMOUNT, SILVER_HEAL_AMOUNT, MYRRH_HEAL_AMOUNT,
    GROUND_Y, SCREEN_WIDTH, GOLD, SILVER, WHITE, BLACK
)


class Collectible(ABC):
    """Classe base astratta per tutti gli oggetti collezionabili"""
    
    def __init__(self, x: int, y: int, value: int, heal_amount: int = 0):
        """
        Inizializza l'oggetto collezionabile
        
        Args:
            x: Posizione x
            y: Posizione y  
            value: Valore in punti dell'oggetto
            heal_amount: Quantità di cura fornita
        """
        self.x = x
        self.y = y
        self.size = COLLECTIBLE_SIZE
        self.value = value
        self.heal_amount = heal_amount
        self.collected = False
        
        # Animazione
        self.float_timer = 0
        self.float_speed = 2
        self.float_amplitude = 5
        self.start_y = y
        
        # Rect per collision detection
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
    def update(self) -> None:
        """Aggiorna l'animazione dell'oggetto"""
        if self.collected:
            return
            
        # Animazione di fluttuazione
        self.float_timer += self.float_speed
        offset_y = int(self.float_amplitude * pygame.math.Vector2(0, 1).rotate(self.float_timer).y)
        self.y = self.start_y + offset_y
        
        # Aggiorna il rect
        self.rect.y = self.y
        
    def collect(self) -> Tuple[int, int]:
        """
        Raccoglie l'oggetto
        
        Returns:
            Tupla (valore, heal_amount)
        """
        self.collected = True
        return (self.value, self.heal_amount)
        
    def is_collected(self) -> bool:
        """
        Controlla se l'oggetto è stato raccolto
        
        Returns:
            True se raccolto, False altrimenti
        """
        return self.collected
        
    def get_position(self) -> Tuple[int, int]:
        """
        Restituisce la posizione dell'oggetto
        
        Returns:
            Tupla (x, y) della posizione
        """
        return (self.x, self.y)
        
    @abstractmethod
    def get_resource_type(self) -> str:
        """
        Restituisce il tipo di risorsa
        
        Returns:
            Nome del tipo di risorsa
        """
        pass
        
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Disegna l'oggetto sullo schermo
        
        Args:
            screen: Superficie pygame su cui disegnare
        """
        pass


class Gold(Collectible):
    """Moneta d'oro - risorsa comune"""
    
    def __init__(self, x: int, y: int):
        """
        Inizializza la moneta d'oro
        
        Args:
            x: Posizione x
            y: Posizione y
        """
        super().__init__(x, y, GOLD_VALUE, GOLD_HEAL_AMOUNT)
        self.resource_type = "oro"
        
    def get_resource_type(self) -> str:
        """Restituisce il tipo di risorsa oro"""
        return self.resource_type
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Disegna la moneta d'oro (più grande e visibile!)
        
        Args:
            screen: Superficie pygame su cui disegnare
        """
        if self.collected:
            return
            
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        radius = self.size // 2
            
        # Cerchio dorato più luminoso
        pygame.draw.circle(screen, (255, 223, 0), (center_x, center_y), radius)
        
        # Cerchio interno per effetto metallico
        pygame.draw.circle(screen, (255, 239, 150), (center_x, center_y), radius - 3)
        
        # Bordo scuro più spesso
        pygame.draw.circle(screen, BLACK, (center_x, center_y), radius, 3)
        
        # Simbolo $ al centro più grande e visibile
        font_size = self.size - 6
        font = pygame.font.Font(None, font_size)
        text = font.render("$", True, BLACK)
        text_rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, text_rect)
        
        # Piccoli riflessi per effetto lucido
        pygame.draw.circle(screen, WHITE, (center_x - radius//3, center_y - radius//3), 3)
        pygame.draw.circle(screen, WHITE, (center_x + radius//4, center_y + radius//4), 2)


class Silver(Collectible):
    """Lingotto d'argento - risorsa intermedia"""
    
    def __init__(self, x: int, y: int):
        """
        Inizializza il lingotto d'argento
        
        Args:
            x: Posizione x
            y: Posizione y
        """
        super().__init__(x, y, SILVER_VALUE, SILVER_HEAL_AMOUNT)
        self.resource_type = "argento"
        
    def get_resource_type(self) -> str:
        """Restituisce il tipo di risorsa argento"""
        return self.resource_type
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Disegna il lingotto d'argento (più grande e dettagliato!)
        
        Args:
            screen: Superficie pygame su cui disegnare
        """
        if self.collected:
            return
            
        # Rettangolo argentato principale più grande
        silver_rect = pygame.Rect(self.x + 3, self.y + 5, self.size - 6, self.size - 10)
        
        # Gradiente argentato (simulato con rettangoli sovrapposti)
        pygame.draw.rect(screen, (192, 192, 192), silver_rect)  # Base argento
        
        # Effetto metallico con sfumature
        top_rect = pygame.Rect(self.x + 3, self.y + 5, self.size - 6, (self.size - 10) // 3)
        pygame.draw.rect(screen, (220, 220, 220), top_rect)  # Parte superiore più chiara
        
        # Bordo scuro più spesso
        pygame.draw.rect(screen, BLACK, silver_rect, 3)
        
        # Linee decorative più spesse e visibili
        line_thickness = 2
        line1_y = self.y + self.size // 3
        line2_y = self.y + 2 * self.size // 3
        
        pygame.draw.line(screen, WHITE, (self.x + 5, line1_y), (self.x + self.size - 5, line1_y), line_thickness)
        pygame.draw.line(screen, WHITE, (self.x + 5, line2_y), (self.x + self.size - 5, line2_y), line_thickness)
        
        # Riflessi sui bordi
        pygame.draw.line(screen, WHITE, (self.x + 4, self.y + 6), (self.x + 4, self.y + self.size - 6), 1)
        pygame.draw.line(screen, WHITE, (self.x + self.size - 4, self.y + 6), (self.x + self.size - 4, self.y + self.size - 6), 1)


class Myrrh(Collectible):
    """Mirra - risorsa rara e preziosa"""
    
    def __init__(self, x: int, y: int):
        """
        Inizializza la mirra
        
        Args:
            x: Posizione x
            y: Posizione y
        """
        super().__init__(x, y, MYRRH_VALUE, MYRRH_HEAL_AMOUNT)
        self.resource_type = "mirra"
        self.sparkle_timer = 0
        
    def get_resource_type(self) -> str:
        """Restituisce il tipo di risorsa mirra"""
        return self.resource_type
        
    def update(self) -> None:
        """Aggiorna l'animazione della mirra con effetto scintillio"""
        super().update()
        if not self.collected:
            self.sparkle_timer += 1
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Disegna la mirra con effetto scintillio (molto più spettacolare!)
        
        Args:
            screen: Superficie pygame su cui disegnare
        """
        if self.collected:
            return
            
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
            
        # Colore base viola/rosso scuro più intenso
        base_color = (138, 43, 226)  # Viola scuro
        highlight_color = (180, 80, 255)  # Viola chiaro
        
        # Forma esagonale (semplificata come rombo) più grande
        points = [
            (center_x, self.y + 3),  # Top
            (self.x + self.size - 3, center_y),  # Right
            (center_x, self.y + self.size - 3),  # Bottom
            (self.x + 3, center_y)  # Left
        ]
        
        # Rombo principale
        pygame.draw.polygon(screen, base_color, points)
        
        # Rombo interno per effetto di profondità
        inner_points = [
            (center_x, self.y + 6),  # Top
            (self.x + self.size - 6, center_y),  # Right
            (center_x, self.y + self.size - 6),  # Bottom
            (self.x + 6, center_y)  # Left
        ]
        pygame.draw.polygon(screen, highlight_color, inner_points)
        
        # Bordo dorato più spesso
        pygame.draw.polygon(screen, GOLD, points, 3)
        
        # Effetto scintillio potenziato
        if self.sparkle_timer % 30 < 15:  # Scintilla ogni mezzo secondo
            sparkle_color = WHITE
            
            # Stella scintillante al centro più grande
            star_size = 5
            pygame.draw.line(screen, sparkle_color, (center_x - star_size, center_y), (center_x + star_size, center_y), 3)
            pygame.draw.line(screen, sparkle_color, (center_x, center_y - star_size), (center_x, center_y + star_size), 3)
            pygame.draw.line(screen, sparkle_color, (center_x - 4, center_y - 4), (center_x + 4, center_y + 4), 2)
            pygame.draw.line(screen, sparkle_color, (center_x - 4, center_y + 4), (center_x + 4, center_y - 4), 2)
            
            # Scintille aggiuntive sui vertici
            for point in points:
                pygame.draw.circle(screen, sparkle_color, point, 2)
                
        # Effetto alone se non sta scintillando
        else:
            # Alone viola intorno al diamante
            glow_points = [
                (center_x, self.y + 1),  # Top
                (self.x + self.size - 1, center_y),  # Right
                (center_x, self.y + self.size - 1),  # Bottom
                (self.x + 1, center_y)  # Left
            ]
            pygame.draw.polygon(screen, (100, 20, 150), glow_points, 2)


def create_random_collectible(x: int, y: int) -> Collectible:
    """
    Crea un oggetto collezionabile casuale
    
    Args:
        x: Posizione x
        y: Posizione y
        
    Returns:
        Oggetto collezionabile casuale
    """
    rand = random.random()
    
    if rand < 0.6:  # 60% oro
        return Gold(x, y)
    elif rand < 0.9:  # 30% argento
        return Silver(x, y)
    else:  # 10% mirra
        return Myrrh(x, y)


def spawn_collectibles_in_area(area_width: int, area_height: int, ground_y: int, count: int, platforms: list = None) -> list:
    """
    Spawn di collezionabili in un'area specifica
    
    Args:
        area_width: Larghezza dell'area
        area_height: Altezza dell'area
        ground_y: Posizione Y del terreno
        count: Numero di oggetti da creare
        platforms: Lista di piattaforme per posizionamento strategico
        
    Returns:
        Lista di oggetti collezionabili
    """
    collectibles = []
    
    # Posizioni strategiche: alcune a terra, alcune su piattaforme
    ground_positions = [
        (150, ground_y - 30),
        (300, ground_y - 35),
        (450, ground_y - 30),
        (600, ground_y - 35),
        (750, ground_y - 30),
    ]
    
    # Se ci sono piattaforme, aggiungi posizioni su di esse
    platform_positions = []
    if platforms:
        for platform in platforms:
            platform_positions.append((
                platform.x + platform.width // 2,
                platform.y - 30
            ))
    
    # Combina tutte le posizioni disponibili
    all_positions = ground_positions + platform_positions
    
    # Seleziona posizioni casuali per i collezionabili
    selected_positions = random.sample(all_positions, min(count, len(all_positions)))
    
    for x, y in selected_positions:
        # Aggiungi un po' di variazione casuale
        x += random.randint(-20, 20)
        y += random.randint(-10, 10)
        
        # Assicurati che rimanga nei confini
        x = max(30, min(x, area_width - 30))
        y = max(50, min(y, ground_y - 25))
        
        collectible = create_random_collectible(x, y)
        collectibles.append(collectible)
        
    return collectibles 