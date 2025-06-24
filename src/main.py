"""
Entry point per Knight's Quest: Il Santo Graal
"""
import asyncio
import sys
import os

# Aggiungi la directory corrente al path per gli import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import Game


async def main() -> None:
    """
    Funzione principale che avvia il gioco
    Compatibile con pygbag per il deploy web
    """
    game = Game()
    await game.run()


if __name__ == "__main__":
    # Per compatibilità con pygbag
    asyncio.run(main()) 