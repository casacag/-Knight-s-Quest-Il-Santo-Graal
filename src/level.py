"""
Sistema di gestione dei livelli del gioco
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import random
from src.config import SCREEN_WIDTH, GROUND_Y


class LevelObjective(Enum):
    """Tipi di obiettivi dei livelli"""
    COLLECT_ALL_TREASURES = "collect_all_treasures"
    DEFEAT_ALL_ENEMIES = "defeat_all_enemies"
    SURVIVE_TIME = "survive_time"
    REACH_SCORE = "reach_score"
    DEFEAT_BOSS = "defeat_boss"


@dataclass
class LevelConfig:
    """Configurazione di un livello"""
    level_number: int
    name: str
    description: str
    objectives: List[LevelObjective]
    enemy_count: int
    collectible_count: int
    time_limit: Optional[int] = None  # secondi, None = illimitato
    target_score: Optional[int] = None
    boss_type: Optional[str] = None
    background_color: tuple = (20, 20, 40)  # Colore di sfondo
    background_image: Optional[str] = None  # Nome del file di sfondo
    
    
class LevelManager:
    """Gestisce la progressione e gli obiettivi dei livelli"""
    
    def __init__(self):
        """Inizializza il level manager"""
        self.current_level = 1
        self.max_level = 5  # Il quinto livello con il boss finale
        self.levels_config = self._create_level_configs()
        self.level_complete = False
        self.all_levels_complete = False
        
        # Timer per livelli con limite di tempo
        self.level_start_time = 0
        self.level_time_elapsed = 0
        
    def _create_level_configs(self) -> Dict[int, LevelConfig]:
        """
        Crea le configurazioni per tutti i livelli
        
        Returns:
            Dizionario con configurazioni dei livelli
        """
        return {
            1: LevelConfig(
                level_number=1,
                name="La Taverna Abbandonata",
                description="Raccogli tutte le risorse e sconfiggi i demoni",
                objectives=[
                    LevelObjective.COLLECT_ALL_TREASURES,
                    LevelObjective.DEFEAT_ALL_ENEMIES
                ],
                enemy_count=3,
                collectible_count=6,
                background_color=(25, 25, 50),
                background_image="fondale1"
            ),
            
            2: LevelConfig(
                level_number=2,
                name="Le Catacombe Oscure", 
                description="Raccogli tutti i tesori nel tempo limite",
                objectives=[
                    LevelObjective.COLLECT_ALL_TREASURES
                ],
                enemy_count=5,
                collectible_count=8,
                time_limit=120,  # 2 minuti per raccogliere tutto
                background_color=(40, 20, 20),
                background_image="fondale2"
            ),
            
            3: LevelConfig(
                level_number=3,
                name="La Prova di Resistenza",
                description="Sopravvivi 60 secondi O sconfiggi tutti i nemici",
                objectives=[
                    LevelObjective.SURVIVE_TIME,
                    LevelObjective.DEFEAT_ALL_ENEMIES  # BASTA UNO DEI DUE!
                ],
                enemy_count=6,
                collectible_count=4,  # Pochi tesori per cure
                time_limit=60,  # Completa QUANDO raggiungi 60 secondi
                background_color=(50, 25, 25),
                background_image="fondale3"
            ),
            
            4: LevelConfig(
                level_number=4,
                name="La Fortezza del Boss",
                description="Sconfiggi il Boss Demone Finale!",
                objectives=[
                    LevelObjective.DEFEAT_ALL_ENEMIES  # Solo sconfiggere il boss
                ],
                enemy_count=1,  # Un solo boss potente
                collectible_count=3,  # Alcuni tesori per aiutare
                target_score=None,  # Nessun punteggio richiesto
                boss_type="final_boss",
                background_color=(80, 20, 20),  # Rosso più intenso per il boss
                background_image="fondale 4"  # Nota: il file ha uno spazio nel nome
            ),
            
            5: LevelConfig(
                level_number=5,
                name="Il Sanctum del Graal",
                description="Sconfiggi tutti i demoni e ottieni il Santo Graal!",
                objectives=[
                    LevelObjective.DEFEAT_ALL_ENEMIES,
                    LevelObjective.COLLECT_ALL_TREASURES
                ],
                enemy_count=2,  # Pochi nemici per testare facilmente
                collectible_count=1,  # Un solo tesoro per testare facilmente
                boss_type="demon_lord",
                background_color=(60, 10, 10),  # Rosso scuro per il finale
                background_image="fondale 4"  # Riusiamo il fondale4 per il finale epico
            )
        }
        
    def get_current_level_config(self) -> LevelConfig:
        """
        Restituisce la configurazione del livello attuale
        
        Returns:
            Configurazione del livello corrente
        """
        return self.levels_config[self.current_level]
        
    def start_level(self, level_number: int, current_time: int) -> None:
        """
        Inizia un nuovo livello
        
        Args:
            level_number: Numero del livello da iniziare
            current_time: Tempo corrente in millisecondi
        """
        self.current_level = level_number
        self.level_complete = False
        self.level_start_time = current_time
        self.level_time_elapsed = 0
        
    def update_timer(self, current_time: int) -> None:
        """
        Aggiorna il timer del livello
        
        Args:
            current_time: Tempo corrente in millisecondi
        """
        self.level_time_elapsed = (current_time - self.level_start_time) // 1000
        
    def check_level_objectives(self, game_stats: Dict[str, Any]) -> bool:
        """
        Controlla se gli obiettivi del livello sono stati completati
        
        Args:
            game_stats: Statistiche di gioco attuali
            
        Returns:
            True se il livello è completato
        """
        if self.level_complete:
            return True
            
        config = self.get_current_level_config()
        objectives_met = []
        
        for objective in config.objectives:
            if objective == LevelObjective.COLLECT_ALL_TREASURES:
                objectives_met.append(game_stats.get('collectibles_remaining', 1) == 0)
                
            elif objective == LevelObjective.DEFEAT_ALL_ENEMIES:
                objectives_met.append(game_stats.get('enemies_remaining', 1) == 0)
                
            elif objective == LevelObjective.SURVIVE_TIME:
                if config.time_limit:
                    objectives_met.append(self.level_time_elapsed >= config.time_limit)
                    
            elif objective == LevelObjective.REACH_SCORE:
                if config.target_score:
                    objectives_met.append(game_stats.get('total_score', 0) >= config.target_score)
                    
            elif objective == LevelObjective.DEFEAT_BOSS:
                objectives_met.append(game_stats.get('boss_defeated', False))
        
        # Per il livello 3, basta completare UNO degli obiettivi (OR logic)
        # Per tutti gli altri livelli, devono essere completati TUTTI (AND logic)
        if config.level_number == 3:
            self.level_complete = any(objectives_met)  # Basta uno per il livello 3
        else:
            self.level_complete = all(objectives_met)  # Tutti per gli altri livelli
        
        if self.level_complete and self.current_level == self.max_level:
            self.all_levels_complete = True
            
        return self.level_complete
        
    def is_level_failed(self, game_stats: Dict[str, Any]) -> bool:
        """
        Controlla se il livello è fallito (solo per timeout, non per morte del player)
        
        Args:
            game_stats: Statistiche di gioco attuali
            
        Returns:
            True se il livello è fallito per timeout
        """
        config = self.get_current_level_config()
        
        # Per livelli SURVIVE_TIME, NON falliscono per timeout - si completano!
        if LevelObjective.SURVIVE_TIME in config.objectives:
            return False
            
        # Fallimento per timeout per altri tipi di livello
        if config.time_limit and self.level_time_elapsed > config.time_limit:
            return True
            
        # Nota: La morte del player è gestita separatamente nel game loop
        # Non controlliamo player_alive qui per evitare conflitti
            
        return False
        
    def advance_to_next_level(self) -> bool:
        """
        Avanza al livello successivo
        
        Returns:
            True se c'è un livello successivo, False se tutti i livelli sono completati
        """
        if self.current_level < self.max_level:
            self.current_level += 1
            self.level_complete = False
            return True
        else:
            self.all_levels_complete = True
            return False
            
    def get_objectives_text(self) -> List[str]:
        """
        Restituisce una lista di testi che descrivono gli obiettivi del livello
        
        Returns:
            Lista di stringhe con gli obiettivi
        """
        config = self.get_current_level_config()
        objectives_text = []
        
        # Livello 3 speciale - mostra con OR logic
        if config.level_number == 3:
            objectives_text.append("⚔ Sconfiggi tutti i nemici (6)")
            objectives_text.append("       OPPURE")
            objectives_text.append("⏰ Sopravvivi per 60 secondi")
            return objectives_text
        
        # Altri livelli - logica normale
        for objective in config.objectives:
            if objective == LevelObjective.COLLECT_ALL_TREASURES:
                objectives_text.append(f"✦ Raccogli tutti i tesori ({config.collectible_count})")
                
            elif objective == LevelObjective.DEFEAT_ALL_ENEMIES:
                objectives_text.append(f"⚔ Sconfiggi tutti i nemici ({config.enemy_count})")
                
            elif objective == LevelObjective.SURVIVE_TIME:
                if config.time_limit:
                    objectives_text.append(f"⏰ Sopravvivi per {config.time_limit} secondi")
                    
            elif objective == LevelObjective.REACH_SCORE:
                if config.target_score:
                    objectives_text.append(f"🎯 Raggiungi {config.target_score} punti")
                    
            elif objective == LevelObjective.DEFEAT_BOSS:
                objectives_text.append("👹 Sconfiggi il Signore dei Demoni!")
                
        return objectives_text
        
    def get_progress_text(self, game_stats: Dict[str, Any]) -> List[str]:
        """
        Restituisce il progresso attuale verso gli obiettivi
        
        Args:
            game_stats: Statistiche di gioco attuali
            
        Returns:
            Lista di stringhe con il progresso
        """
        config = self.get_current_level_config()
        progress_text = []
        
        for objective in config.objectives:
            if objective == LevelObjective.COLLECT_ALL_TREASURES:
                remaining = game_stats.get('collectibles_remaining', config.collectible_count)
                collected = config.collectible_count - remaining
                progress_text.append(f"Tesori: {collected}/{config.collectible_count}")
                
            elif objective == LevelObjective.DEFEAT_ALL_ENEMIES:
                remaining = game_stats.get('enemies_remaining', config.enemy_count)
                defeated = config.enemy_count - remaining
                progress_text.append(f"Nemici: {defeated}/{config.enemy_count}")
                
            elif objective == LevelObjective.SURVIVE_TIME:
                if config.time_limit:
                    remaining_time = max(0, config.time_limit - self.level_time_elapsed)
                    progress_text.append(f"Tempo: {remaining_time}s")
                    
            elif objective == LevelObjective.REACH_SCORE:
                if config.target_score:
                    current_score = game_stats.get('total_score', 0)
                    progress_text.append(f"Punteggio: {current_score}/{config.target_score}")
                    
            elif objective == LevelObjective.DEFEAT_BOSS:
                boss_defeated = game_stats.get('boss_defeated', False)
                status = "✓" if boss_defeated else "✗"
                progress_text.append(f"Boss: {status}")
                
        return progress_text
        
    def get_time_remaining_text(self) -> Optional[str]:
        """
        Restituisce il testo del tempo rimanente se applicabile
        
        Returns:
            Stringa con il tempo rimanente o None
        """
        config = self.get_current_level_config()
        
        if config.time_limit:
            remaining = max(0, config.time_limit - self.level_time_elapsed)
            minutes = remaining // 60
            seconds = remaining % 60
            return f"Tempo: {minutes:02d}:{seconds:02d}"
            
        return None
        
    def generate_enemy_positions(self, enemy_count: int) -> List[tuple]:
        """
        Genera posizioni casuali per i nemici del livello
        
        Args:
            enemy_count: Numero di nemici da posizionare
            
        Returns:
            Lista di tuple (x, y) con posizioni
        """
        positions = []
        min_distance = 100  # Distanza minima tra nemici
        
        for _ in range(enemy_count):
            attempts = 0
            while attempts < 20:  # Max 20 tentativi per posizione
                x = random.randint(200, SCREEN_WIDTH - 100)
                y = GROUND_Y - 40
                
                # Controlla distanza da altri nemici
                valid_position = True
                for pos_x, pos_y in positions:
                    if abs(x - pos_x) < min_distance:
                        valid_position = False
                        break
                        
                if valid_position:
                    positions.append((x, y))
                    break
                    
                attempts += 1
                
        return positions 