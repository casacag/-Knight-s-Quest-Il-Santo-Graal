"""
Classe Game principale per la gestione del gioco
"""
from typing import Dict, Optional
import pygame
import sys
import asyncio
from src.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, GREEN, RED,
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_PAUSED,
    GAME_STATE_GAME_OVER, GAME_STATE_VICTORY, KEY_QUIT,
    GAME_STATE_LEVEL_INTRO, GAME_STATE_LEVEL_COMPLETE, GAME_STATE_LEVEL_FAILED,
    GROUND_Y, BROWN, PLAYER_ATTACK_DAMAGE
)
from src.player import Player
from src.enemy import DemonArmed
from src.collectible import Collectible, spawn_collectibles_in_area
from src.platform import create_default_platforms
from src.level import LevelManager
from src.sprite_manager import sprite_manager
from typing import List


class Game:
    """Classe principale che gestisce il gioco"""
    
    def __init__(self):
        """Inizializza il gioco"""
        pygame.init()
        pygame.display.set_caption("Knight's Quest: Il Santo Graal")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GAME_STATE_MENU
        
        # Font per UI
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Inizializza il player (aggiustata posizione per nuove dimensioni)
        self.player = Player(100, GROUND_Y - 80)
        
        # Sistema di livelli
        self.level_manager = LevelManager()
        
        # Piattaforme
        self.platforms = create_default_platforms()
        
        # Lista dei nemici
        self.enemies: List[DemonArmed] = []
        
        # Lista dei collezionabili
        self.collectibles: List[Collectible] = []
        
        # Statistiche di gioco
        self.enemies_killed = 0
        self.total_score = 0
        
        # Inizializza il primo livello
        self._start_level(1)
        
        # Stato dei tasti
        self.keys_pressed: Dict[int, bool] = {}
        
    async def run(self) -> None:
        """Loop principale del gioco - compatibile con pygbag"""
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            
            # Per pygbag, usiamo asyncio.sleep invece di clock.tick
            try:
                # Calcola il tempo per mantenere 60 FPS
                await asyncio.sleep(1.0 / FPS)
            except:
                # Fallback per esecuzione normale
                self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def _handle_events(self) -> None:
        """Gestisce gli eventi pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed[event.key] = True
                
                # Menu principale
                if self.state == GAME_STATE_MENU:
                    if event.key == pygame.K_RETURN:
                        self.state = GAME_STATE_PLAYING
                    elif event.key == KEY_QUIT:
                        self.running = False
                        
                # Durante il gioco
                elif self.state == GAME_STATE_PLAYING:
                    if event.key == KEY_QUIT:
                        self.state = GAME_STATE_MENU
                    elif event.key == pygame.K_p:
                        self.state = GAME_STATE_PAUSED
                    # CHEAT: Premi 4 per saltare al boss e 5 per santo graal
                    elif event.key == pygame.K_4:
                        self._start_level(4)
                    elif event.key == pygame.K_5:
                        self._start_level(5)
                        
                # In pausa
                elif self.state == GAME_STATE_PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GAME_STATE_PLAYING
                    elif event.key == KEY_QUIT:
                        self.state = GAME_STATE_MENU
                        
                # Game Over
                elif self.state == GAME_STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self._restart_current_level()
                    elif event.key == pygame.K_RETURN:
                        self._restart_game()  # Ricomincia dall'inizio
                    elif event.key == KEY_QUIT:
                        self.state = GAME_STATE_MENU
                        
                # Level Intro
                elif self.state == GAME_STATE_LEVEL_INTRO:
                    if event.key == pygame.K_RETURN:
                        self.state = GAME_STATE_PLAYING
                        
                # Level Complete
                elif self.state == GAME_STATE_LEVEL_COMPLETE:
                    if event.key == pygame.K_RETURN:
                        self._advance_to_next_level()
                    elif event.key == KEY_QUIT:
                        self.state = GAME_STATE_MENU
                        
                # Level Failed
                elif self.state == GAME_STATE_LEVEL_FAILED:
                    if event.key == pygame.K_r:
                        self._restart_current_level()
                    elif event.key == KEY_QUIT:
                        self.state = GAME_STATE_MENU
                        
                # Victory
                elif self.state == GAME_STATE_VICTORY:
                    if event.key == KEY_QUIT:
                        self.state = GAME_STATE_MENU
                    elif event.key == pygame.K_RETURN:
                        # Riavvia completamente il gioco
                        self._restart_game()
                        self.state = GAME_STATE_PLAYING
                        
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed[event.key] = False
                    
    def _update(self) -> None:
        """Aggiorna la logica del gioco"""
        if self.state == GAME_STATE_PLAYING:
            # Aggiorna il timer del livello
            self.level_manager.update_timer(pygame.time.get_ticks())
            
            # Aggiorna il player
            self.player.update(self.keys_pressed, self.platforms)
            
            # Aggiorna i nemici
            for enemy in self.enemies[:]:  # Copia la lista per rimozione sicura
                if enemy.is_alive():
                    enemy.update(self.player.x, self.player.y)
                else:
                    self.enemies.remove(enemy)
                    self.enemies_killed += 1
            
            # Aggiorna i collezionabili
            for collectible in self.collectibles[:]:  # Copia la lista per rimozione sicura
                if not collectible.is_collected():
                    collectible.update()
                else:
                    self.collectibles.remove(collectible)
            
            # Gestisci collisioni
            self._handle_collisions()
            
            # Controlla obiettivi del livello
            game_stats = {
                'collectibles_remaining': len(self.collectibles),
                'enemies_remaining': len(self.enemies),
                'total_score': self.total_score,
                'player_alive': self.player.is_alive(),
                'boss_defeated': False  # TODO: implementare boss
            }
            
            # Controlla se il player è morto (priorità massima)
            if not self.player.is_alive():
                self.state = GAME_STATE_GAME_OVER
                
            # Verifica se il livello è completato
            elif self.level_manager.check_level_objectives(game_stats):
                if self.level_manager.all_levels_complete:
                    self.state = GAME_STATE_VICTORY
                else:
                    self.state = GAME_STATE_LEVEL_COMPLETE
                    
            # Verifica se il livello è fallito (solo per timeout, non per morte)
            elif self.level_manager.is_level_failed(game_stats):
                self.state = GAME_STATE_LEVEL_FAILED
                
            # Limita il player ai bordi dello schermo
            if self.player.x < 0:
                self.player.x = 0
            elif self.player.x > SCREEN_WIDTH - self.player.width:
                self.player.x = SCREEN_WIDTH - self.player.width
                
    def _draw(self) -> None:
        """Disegna tutto sullo schermo"""
        self.screen.fill(BLACK)
        
        if self.state == GAME_STATE_MENU:
            self._draw_menu()
        elif self.state == GAME_STATE_LEVEL_INTRO:
            self._draw_level_intro()
        elif self.state == GAME_STATE_PLAYING:
            self._draw_game()
        elif self.state == GAME_STATE_PAUSED:
            self._draw_game()
            self._draw_pause_overlay()
        elif self.state == GAME_STATE_LEVEL_COMPLETE:
            self._draw_level_complete()
        elif self.state == GAME_STATE_LEVEL_FAILED:
            self._draw_level_failed()
        elif self.state == GAME_STATE_GAME_OVER:
            self._draw_game_over()
        elif self.state == GAME_STATE_VICTORY:
            self._draw_victory()
            
        pygame.display.flip()
        
    def _draw_menu(self) -> None:
        """Disegna il menu principale"""
        title_text = self.font_large.render("Knight's Quest: Il Santo Graal", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
        
        start_text = self.font_medium.render("Premi ENTER per iniziare", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        cheat_text = self.font_small.render("CHEAT: Premi 4 (boss) o 5 (santo graal) durante il gioco!", True, (255, 255, 0))
        cheat_rect = cheat_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(cheat_text, cheat_rect)
        
        quit_text = self.font_small.render("Premi ESC per uscire", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(quit_text, quit_rect)
        
    def _draw_game(self) -> None:
        """Disegna la schermata di gioco"""
        # Disegna lo sfondo del livello
        level_config = self.level_manager.get_current_level_config()
        
        if level_config.background_image:
            # Carica e disegna l'immagine di sfondo
            background = sprite_manager.load_background(
                level_config.background_image,
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            self.screen.blit(background, (0, 0))
        else:
            # Fallback al colore di sfondo
            self.screen.fill(level_config.background_color)
            
            # Disegna il terreno
            ground_rect = pygame.Rect(0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
            pygame.draw.rect(self.screen, BROWN, ground_rect)
        
        # Disegna le piattaforme
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Disegna il player
        self.player.draw(self.screen)
        
        # Disegna i nemici
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Disegna i collezionabili
        for collectible in self.collectibles:
            collectible.draw(self.screen)
        
        # Disegna l'HUD
        self._draw_hud()
        
    def _draw_hud(self) -> None:
        """Disegna l'interfaccia utente (HUD)"""
        # Barra della salute
        health_text = self.font_small.render(f"Salute: {self.player.health}/100", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # Barra della salute grafica
        health_bar_width = 200
        health_bar_height = 20
        health_percentage = self.player.health / 100
        
        # Sfondo barra salute
        health_bg_rect = pygame.Rect(10, 35, health_bar_width, health_bar_height)
        pygame.draw.rect(self.screen, WHITE, health_bg_rect, 2)
        
        # Barra salute attuale
        if health_percentage > 0:
            health_fill_width = int(health_bar_width * health_percentage)
            health_fill_rect = pygame.Rect(10, 35, health_fill_width, health_bar_height)
            color = GREEN if health_percentage > 0.3 else (255, 165, 0) if health_percentage > 0.1 else (255, 0, 0)
            pygame.draw.rect(self.screen, color, health_fill_rect)
            
        # Risorse
        resources_y = 70
        for resource_type, amount in self.player.resources.items():
            resource_text = self.font_small.render(f"{resource_type.capitalize()}: {amount}", True, WHITE)
            self.screen.blit(resource_text, (10, resources_y))
            resources_y += 25
            
        # Statistiche nemici
        enemies_text = self.font_small.render(f"Demoni uccisi: {self.enemies_killed}", True, WHITE)
        self.screen.blit(enemies_text, (10, resources_y))
        
        enemies_remaining_text = self.font_small.render(f"Demoni rimanenti: {len(self.enemies)}", True, WHITE)
        self.screen.blit(enemies_remaining_text, (10, resources_y + 25))
        
        # Statistiche collezionabili
        collectibles_remaining_text = self.font_small.render(f"Tesori rimanenti: {len(self.collectibles)}", True, WHITE)
        self.screen.blit(collectibles_remaining_text, (10, resources_y + 50))
        
        score_text = self.font_small.render(f"Punteggio: {self.total_score}", True, WHITE)
        self.screen.blit(score_text, (10, resources_y + 75))
        
        # Informazioni livello e obiettivi
        level_config = self.level_manager.get_current_level_config()
        level_text = self.font_small.render(f"Livello {level_config.level_number}: {level_config.name}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 300, 10))
        
        # Timer se necessario
        time_text = self.level_manager.get_time_remaining_text()
        if time_text:
            timer_color = (255, 0, 0) if "00:" in time_text and int(time_text.split(":")[1]) <= 10 else WHITE
            timer_render = self.font_small.render(time_text, True, timer_color)
            self.screen.blit(timer_render, (SCREEN_WIDTH - 300, 35))
        
        # Obiettivi
        objectives_y = 60 if time_text else 35
        game_stats = {
            'collectibles_remaining': len(self.collectibles),
            'enemies_remaining': len(self.enemies),
            'total_score': self.total_score,
            'boss_defeated': False
        }
        
        progress_list = self.level_manager.get_progress_text(game_stats)
        for i, progress in enumerate(progress_list):
            progress_render = self.font_small.render(progress, True, WHITE)
            self.screen.blit(progress_render, (SCREEN_WIDTH - 300, objectives_y + i * 20))
            
        # DEBUG: Mostra stato completamento livello finale
        if self.level_manager.current_level >= 4:
            debug_y = objectives_y + len(progress_list) * 20 + 10
            
            # DEBUG più grande e visibile
            debug_title = self.font_medium.render("🏆 LIVELLO FINALE - DEBUG 🏆", True, (255, 255, 0))
            self.screen.blit(debug_title, (SCREEN_WIDTH - 400, debug_y))
            
            debug_text2 = f"Nemici rimanenti: {len(self.enemies)} (devono essere 0)"
            debug_render2 = self.font_small.render(debug_text2, True, (255, 100, 100) if len(self.enemies) > 0 else (100, 255, 100))
            self.screen.blit(debug_render2, (SCREEN_WIDTH - 400, debug_y + 30))
            
            debug_text3 = f"Tesori rimanenti: {len(self.collectibles)} (devono essere 0)"
            debug_render3 = self.font_small.render(debug_text3, True, (255, 100, 100) if len(self.collectibles) > 0 else (100, 255, 100))
            self.screen.blit(debug_render3, (SCREEN_WIDTH - 400, debug_y + 50))
            
            debug_text4 = f"Livello completato: {self.level_manager.level_complete}"
            debug_render4 = self.font_small.render(debug_text4, True, (100, 255, 100) if self.level_manager.level_complete else (255, 100, 100))
            self.screen.blit(debug_render4, (SCREEN_WIDTH - 400, debug_y + 70))
            
            debug_text5 = f"Tutti livelli completati: {self.level_manager.all_levels_complete}"
            debug_render5 = self.font_small.render(debug_text5, True, (100, 255, 100) if self.level_manager.all_levels_complete else (255, 100, 100))
            self.screen.blit(debug_render5, (SCREEN_WIDTH - 400, debug_y + 90))
            
            # Messaggio grande se tutto è pronto
            if len(self.enemies) == 0 and len(self.collectibles) == 0:
                victory_ready = self.font_large.render("VITTORIA PROSSIMA!", True, (255, 255, 0))
                self.screen.blit(victory_ready, (50, 200))
            
        # Comandi
        commands_text = self.font_small.render("Frecce: Movimento | SPAZIO: Salto | X: Attacco | P: Pausa | ESC: Menu", True, WHITE)
        commands_rect = commands_text.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 10)
        self.screen.blit(commands_text, commands_rect)
        
    def _draw_pause_overlay(self) -> None:
        """Disegna l'overlay di pausa"""
        # Overlay semi-trasparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Testo pausa
        pause_text = self.font_large.render("PAUSA", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        resume_text = self.font_medium.render("Premi P per continuare", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(resume_text, resume_rect)
        
    def _draw_game_over(self) -> None:
        """Disegna la schermata di game over"""
        self.screen.fill((20, 0, 0))  # Rosso molto scuro
        
        # Titolo
        game_over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Messaggio di morte
        death_text = self.font_medium.render("Il Cavaliere è caduto in battaglia!", True, WHITE)
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(death_text, death_rect)
        
        # Opzioni
        retry_text = self.font_medium.render("R - Riprova questo livello", True, WHITE)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(retry_text, retry_rect)
        
        restart_text = self.font_medium.render("ENTER - Ricomincia dal Livello 1", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_small.render("ESC - Torna al Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(menu_text, menu_rect)
        
    def _draw_victory(self) -> None:
        """Disegna la schermata di vittoria epica del Santo Graal"""

        
        # Sfondo dorato scintillante
        self.screen.fill((20, 20, 0))
        
        # Effetto scintillio con rettangoli dorati casuali
        import random
        for _ in range(30):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(2, 8)
            alpha = random.randint(50, 200)
            sparkle_color = (255, 215 + random.randint(-50, 40), random.randint(0, 100))
            pygame.draw.rect(self.screen, sparkle_color, (x, y, size, size))
        
        # Titolo VITTORIA gigante
        victory_text = self.font_large.render("⚔ VITTORIA! ⚔", True, (255, 215, 0))
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 40))
        self.screen.blit(victory_text, victory_rect)
        
        # Disegna il Santo Graal (rappresentazione ASCII art style)
        grail_y = SCREEN_HEIGHT // 2 - 60
        
        # Graal - Coppa
        pygame.draw.ellipse(self.screen, (255, 215, 0), 
                          (SCREEN_WIDTH // 2 - 40, grail_y, 80, 30))
        pygame.draw.ellipse(self.screen, (255, 255, 0), 
                          (SCREEN_WIDTH // 2 - 35, grail_y + 5, 70, 20))
        
        # Graal - Stelo
        pygame.draw.rect(self.screen, (200, 150, 0), 
                        (SCREEN_WIDTH // 2 - 5, grail_y + 25, 10, 40))
        
        # Graal - Base
        pygame.draw.ellipse(self.screen, (255, 215, 0), 
                          (SCREEN_WIDTH // 2 - 25, grail_y + 60, 50, 15))
        
        # Effetto brillare attorno al graal
        for i in range(8):
            angle = (pygame.time.get_ticks() / 200 + i * 45) % 360
            import math
            offset_x = int(60 * math.cos(math.radians(angle)))
            offset_y = int(30 * math.sin(math.radians(angle)))
            star_x = SCREEN_WIDTH // 2 + offset_x
            star_y = grail_y + 30 + offset_y
            
            # Stelle brillanti
            points = []
            for j in range(8):
                star_angle = j * 45
                if j % 2 == 0:
                    radius = 8
                else:
                    radius = 4
                px = star_x + int(radius * math.cos(math.radians(star_angle)))
                py = star_y + int(radius * math.sin(math.radians(star_angle)))
                points.append((px, py))
            
            if len(points) >= 3:  # Ensure we have enough points
                pygame.draw.polygon(self.screen, (255, 255, 200), points)
        
        # Testo del Graal
        grail_text = self.font_medium.render("🏆 IL SANTO GRAAL È TUO! 🏆", True, (255, 215, 0))
        grail_rect = grail_text.get_rect(center=(SCREEN_WIDTH // 2, grail_y + 120))
        self.screen.blit(grail_text, grail_rect)
        
        # Messaggio epico
        hero_text = self.font_medium.render("Sei diventato il Cavaliere Leggendario!", True, WHITE)
        hero_rect = hero_text.get_rect(center=(SCREEN_WIDTH // 2, grail_y + 150))
        self.screen.blit(hero_text, hero_rect)
        
        # Statistiche finali
        stats_y = grail_y + 190
        score_text = self.font_small.render(f"Punteggio Finale: {self.total_score}", True, (255, 215, 0))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y))
        self.screen.blit(score_text, score_rect)
        
        enemies_text = self.font_small.render(f"Demoni Sconfitti: {self.enemies_killed}", True, (255, 215, 0))
        enemies_rect = enemies_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + 25))
        self.screen.blit(enemies_text, enemies_rect)
        
        # Comandi
        menu_text = self.font_medium.render("Premi ESC per tornare al menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(menu_text, menu_rect)
        
        restart_text = self.font_small.render("Premi ENTER per giocare di nuovo", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(restart_text, restart_rect)
        
    def _restart_game(self) -> None:
        """Riavvia il gioco"""
        # Reset player
        self.player = Player(100, GROUND_Y - 48)
        
        # Reset piattaforme
        self.platforms = create_default_platforms()
        
        # Reset statistiche
        self.enemies_killed = 0
        self.total_score = 0
        
        # Reset level manager e ricomincia dal livello 1
        self.level_manager = LevelManager()
        self._start_level(1)
        

                
    def _handle_collisions(self) -> None:
        """Gestisce tutte le collisioni del gioco"""
        
        # Collisioni attacco player -> nemici
        if self.player.is_attacking and not self.player.damage_dealt_this_attack:
            player_attack_rect = self.player.get_attack_rect()
            for enemy in self.enemies:
                if (enemy.is_alive() and 
                    player_attack_rect.colliderect(enemy.rect)):
                    enemy.take_damage(PLAYER_ATTACK_DAMAGE)
                    self.player.damage_dealt_this_attack = True
                    break  # Solo un nemico per attacco
                    
        # Collisioni attacco nemici -> player (SOLO quando stanno attaccando)
        for enemy in self.enemies:
            if (enemy.is_alive() and 
                enemy.is_attacking and 
                not enemy.damage_dealt_this_attack):
                enemy_attack_rect = enemy.get_attack_rect()
                # Controlla che l'area di attacco sia valida (non vuota)
                if (enemy_attack_rect.width > 0 and 
                    enemy_attack_rect.height > 0 and
                    enemy_attack_rect.colliderect(self.player.rect)):
                    self.player.take_damage(enemy.get_damage())
                    enemy.damage_dealt_this_attack = True
                    
        # Collisioni corpo a corpo (nemico tocca player) - SOLO RESPINGIMENTO
        for enemy in self.enemies:
            if (enemy.is_alive() and 
                not enemy.is_attacking and  # Solo se NON sta attaccando
                enemy.rect.colliderect(self.player.rect)):
                # Respingi player e nemico per evitare sovrapposizioni
                overlap_x = min(self.player.x + self.player.width - enemy.x,
                               enemy.x + enemy.width - self.player.x)
                
                if overlap_x > 0:
                    if enemy.x < self.player.x:
                        # Nemico a sinistra, respingi player a destra
                        self.player.x += overlap_x // 2 + 1
                        enemy.x -= overlap_x // 2 + 1
                    else:
                        # Nemico a destra, respingi player a sinistra  
                        self.player.x -= overlap_x // 2 + 1
                        enemy.x += overlap_x // 2 + 1
                        
                    # Assicurati che restino nei limiti dello schermo
                    self.player.x = max(0, min(SCREEN_WIDTH - self.player.width, self.player.x))
                    enemy.x = max(0, min(SCREEN_WIDTH - enemy.width, enemy.x))
                    
                    # Aggiorna i rect
                    self.player.rect.x = self.player.x
                    enemy.rect.x = enemy.x
                    
        # Collisioni player -> collezionabili
        for collectible in self.collectibles[:]:
            if not collectible.is_collected() and collectible.rect.colliderect(self.player.rect):
                # Raccogli l'oggetto
                value, heal_amount = collectible.collect()
                
                # Aggiungi alla risorsa appropriata
                resource_type = collectible.get_resource_type()
                self.player.collect_resource(resource_type, 1)
                
                # Applica effetti
                if heal_amount > 0:
                    self.player.heal(heal_amount)
                    
                # Aggiorna punteggio
                self.total_score += value
                
    def _start_level(self, level_number: int) -> None:
        """
        Inizia un nuovo livello
        
        Args:
            level_number: Numero del livello da iniziare
        """
        # Resetta timer e stato livello
        self.level_manager.start_level(level_number, pygame.time.get_ticks())
        
        # Resetta player position e salute (aggiustata per nuove dimensioni)
        self.player.x = 100
        self.player.y = GROUND_Y - 80
        self.player.vel_y = 0
        self.player.on_ground = True
        self.player.health = 100  # Reset salute completa
        
        # Resetta nemici e collezionabili
        self.enemies.clear()
        self.collectibles.clear()
        self.enemies_killed = 0
        
        # Spawn nemici e collezionabili basati sul livello
        level_config = self.level_manager.get_current_level_config()
        self._spawn_enemies_for_level(level_config)
        self._spawn_collectibles_for_level(level_config)
        
        # Inizia con schermata introduttiva
        self.state = GAME_STATE_LEVEL_INTRO
        
    def _spawn_enemies_for_level(self, level_config) -> None:
        """
        Spawn nemici per il livello specificato
        
        Args:
            level_config: Configurazione del livello
        """
        positions = self.level_manager.generate_enemy_positions(level_config.enemy_count)
        
        for i, (x, y) in enumerate(positions):
            # Crea boss più forte per livelli speciali
            if level_config.boss_type == "final_boss":
                # Boss del livello 4 - Super forte!
                demon = DemonArmed(x, y, is_boss=True)
            elif level_config.boss_type == "demon_lord":
                # Boss del livello 5 - Santo Graal
                demon = DemonArmed(x, y, is_boss=True)
            else:
                # Nemico normale
                demon = DemonArmed(x, y, is_boss=False)
                
            self.enemies.append(demon)
            
    def _spawn_collectibles_for_level(self, level_config) -> None:
        """
        Spawn collezionabili per il livello specificato
        
        Args:
            level_config: Configurazione del livello
        """
        new_collectibles = spawn_collectibles_in_area(
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, 
            GROUND_Y, 
            level_config.collectible_count,
            self.platforms
        )
        self.collectibles.extend(new_collectibles)
        
    def _advance_to_next_level(self) -> None:
        """Avanza al livello successivo"""
        if self.level_manager.advance_to_next_level():
            self._start_level(self.level_manager.current_level)
        else:
            self.state = GAME_STATE_VICTORY
            
    def _restart_current_level(self) -> None:
        """Riavvia il livello corrente"""
        current_level = self.level_manager.current_level
        self._start_level(current_level)
        
    def _draw_level_intro(self) -> None:
        """Disegna la schermata di introduzione del livello"""
        # Sfondo con colore del livello
        level_config = self.level_manager.get_current_level_config()
        self.screen.fill(level_config.background_color)
        
        # Titolo del livello
        title_text = self.font_large.render(f"LIVELLO {level_config.level_number}", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50))
        self.screen.blit(title_text, title_rect)
        
        # Nome del livello
        name_text = self.font_medium.render(level_config.name, True, (255, 215, 0))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(name_text, name_rect)
        
        # Descrizione
        desc_text = self.font_small.render(level_config.description, True, WHITE)
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 40))
        self.screen.blit(desc_text, desc_rect)
        
        # Obiettivi
        objectives_title = self.font_medium.render("OBIETTIVI:", True, WHITE)
        objectives_rect = objectives_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(objectives_title, objectives_rect)
        
        objectives = self.level_manager.get_objectives_text()
        for i, objective in enumerate(objectives):
            obj_text = self.font_small.render(objective, True, GREEN)
            obj_rect = obj_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40 + i * 25))
            self.screen.blit(obj_text, obj_rect)
        
        # Istruzioni
        start_text = self.font_medium.render("Premi ENTER per iniziare", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(start_text, start_rect)
        
    def _draw_level_complete(self) -> None:
        """Disegna la schermata di livello completato"""
        self.screen.fill((0, 50, 0))  # Verde scuro
        
        # Titolo
        complete_text = self.font_large.render("LIVELLO COMPLETATO!", True, (0, 255, 0))
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(complete_text, complete_rect)
        
        # Statistiche
        stats_y = SCREEN_HEIGHT // 2
        score_text = self.font_medium.render(f"Punteggio: {self.total_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y))
        self.screen.blit(score_text, score_rect)
        
        enemies_text = self.font_medium.render(f"Nemici sconfitti: {self.enemies_killed}", True, WHITE)
        enemies_rect = enemies_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + 30))
        self.screen.blit(enemies_text, enemies_rect)
        
        # Istruzioni
        if self.level_manager.current_level < self.level_manager.max_level:
            next_text = self.font_medium.render("Premi ENTER per il prossimo livello", True, WHITE)
        else:
            next_text = self.font_medium.render("Ultimo livello completato!", True, (255, 215, 0))
            
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(next_text, next_rect)
        
        menu_text = self.font_small.render("Premi ESC per il menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(menu_text, menu_rect)
        
    def _draw_level_failed(self) -> None:
        """Disegna la schermata di livello fallito"""
        self.screen.fill((50, 0, 0))  # Rosso scuro
        
        # Titolo
        failed_text = self.font_large.render("LIVELLO FALLITO", True, (255, 0, 0))
        failed_rect = failed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(failed_text, failed_rect)
        
        # Motivo fallimento
        if not self.player.is_alive():
            reason = "Il cavaliere è caduto in battaglia!"
        else:
            reason = "Tempo scaduto!"
            
        reason_text = self.font_medium.render(reason, True, WHITE)
        reason_rect = reason_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(reason_text, reason_rect)
        
        # Istruzioni
        retry_text = self.font_medium.render("Premi R per riprovare", True, WHITE)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(retry_text, retry_rect)
        
        menu_text = self.font_small.render("Premi ESC per il menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(menu_text, menu_rect) 