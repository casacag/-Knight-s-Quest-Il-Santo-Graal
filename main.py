"""
Main entry point for pygbag WebAssembly build
Knight's Quest: Il Santo Graal
"""
import asyncio
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def main():
    """Main async function for pygbag"""
    try:
        # Import after path setup
        from src.game import Game
        
        game = Game()
        await game.run()
        
    except ImportError as e:
        print(f"Import error: {e}")
        # Fallback - simple pygame window
        import pygame
        
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Knight's Quest - Loading Error")
        clock = pygame.time.Clock()
        
        font = pygame.font.Font(None, 48)
        error_text = font.render("Game Loading Failed", True, (255, 0, 0))
        info_text = font.render("Check console for details", True, (255, 255, 255))
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            screen.fill((0, 0, 0))
            screen.blit(error_text, (250, 250))
            screen.blit(info_text, (200, 350))
            pygame.display.flip()
            await asyncio.sleep(0.01)
            clock.tick(60)
            
    except Exception as e:
        print(f"General error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 