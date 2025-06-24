import pygame
import os
from typing import Dict, Optional

class SpriteManager:
    """Gestisce il caricamento e il caching degli sprite"""
    
    def __init__(self):
        """Inizializza il sprite manager"""
        self.sprites: Dict[str, pygame.Surface] = {}
        self.sprite_path = "sprites"
        
    def load_sprite(self, name: str, size: Optional[tuple] = None) -> pygame.Surface:
        """
        Carica uno sprite e lo ridimensiona se necessario
        
        Args:
            name: Nome del file (senza estensione)
            size: Tuple (width, height) per ridimensionare, None per dimensione originale
            
        Returns:
            Surface di pygame con lo sprite caricato
        """
        cache_key = f"{name}_{size}" if size else name
        
        if cache_key in self.sprites:
            return self.sprites[cache_key]
            
        # Carica l'immagine
        image_path = os.path.join(self.sprite_path, f"{name}.png")
        
        if not os.path.exists(image_path):
            # Fallback - crea un rettangolo colorato se l'immagine non esiste
            print(f"⚠️ Sprite non trovato: {image_path}")
            fallback_size = size if size else (64, 64)
            surface = pygame.Surface(fallback_size)
            surface.fill((255, 0, 255))  # Magenta per indicare sprite mancante
            self.sprites[cache_key] = surface
            return surface
            
        try:
            sprite = pygame.image.load(image_path).convert_alpha()
            
            # Ridimensiona se necessario
            if size:
                sprite = pygame.transform.scale(sprite, size)
                
            self.sprites[cache_key] = sprite
            print(f"✅ Sprite caricato: {name} -> {sprite.get_size()}")
            return sprite
            
        except pygame.error as e:
            print(f"❌ Errore caricamento sprite {name}: {e}")
            # Fallback
            fallback_size = size if size else (64, 64)
            surface = pygame.Surface(fallback_size)
            surface.fill((255, 0, 0))  # Rosso per errore
            self.sprites[cache_key] = surface
            return surface
    
    def load_background(self, name: str, screen_size: tuple) -> pygame.Surface:
        """
        Carica un fondale e lo ridimensiona per lo schermo
        
        Args:
            name: Nome del file fondale (es. "fondale1")
            screen_size: Dimensione dello schermo (width, height)
            
        Returns:
            Surface ridimensionata per lo schermo
        """
        return self.load_sprite(name, screen_size)
    
    def get_player_sprite(self, attacking: bool = False, size: tuple = (64, 80)) -> pygame.Surface:
        """
        Ottiene lo sprite corretto del player (dimensioni aumentate!)
        
        Args:
            attacking: True se il player sta attaccando
            size: Dimensione dello sprite (default aumentato a 64x80)
            
        Returns:
            Surface con lo sprite del player
        """
        sprite_name = "cavaliereattacco" if attacking else "cavaliereariposo"
        return self.load_sprite(sprite_name, size)
    
    def get_enemy_sprite(self, is_boss: bool = False, size: tuple = (56, 74)) -> pygame.Surface:
        """
        Ottiene lo sprite corretto del nemico (dimensioni aumentate!)
        
        Args:
            is_boss: True se è un boss
            size: Dimensione dello sprite (default aumentato a 56x74 per demoni normali)
            
        Returns:
            Surface con lo sprite del nemico
        """
        sprite_name = "boss" if is_boss else "demone"
        # Boss ancora più grandi
        if is_boss and size == (56, 74):  # Se sta usando la dimensione di default
            size = (80, 110)
        return self.load_sprite(sprite_name, size)

# Istanza globale del sprite manager
sprite_manager = SpriteManager() 