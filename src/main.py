"""
Entry point per Knight's Quest: Il Santo Graal - WebAssembly Compatible
"""
import asyncio
import sys
import os

# Aggiungi la directory corrente al path per gli import
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from game import Game
except ImportError:
    # Fallback per struttura diversa
    import game
    Game = game.Game


async def main() -> None:
    """
    Funzione principale che avvia il gioco
    Compatibile con pygbag per il deploy web
    """
    try:
        game = Game()
        await game.run()
    except Exception as e:
        print(f"Errore durante l'avvio del gioco: {e}")
        # In caso di errore, mantieni il loop attivo per pygbag
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Knight's Quest - Errore")
        clock = pygame.time.Clock()
        
        font = pygame.font.Font(None, 36)
        text = font.render("Errore nel caricamento del gioco", True, (255, 255, 255))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            screen.fill((0, 0, 0))
            screen.blit(text, (200, 300))
            pygame.display.flip()
            await asyncio.sleep(0.01)
            clock.tick(60)


if __name__ == "__main__":
    # Per compatibilità con pygbag
    asyncio.run(main()) 