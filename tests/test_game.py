"""
Test unitari per la classe Game
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame
from src.game import Game
from src.config import (
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_PAUSED,
    GAME_STATE_GAME_OVER, SCREEN_WIDTH, SCREEN_HEIGHT
)


class TestGame(unittest.TestCase):
    """Test per la classe Game"""

    def setUp(self):
        """Setup per ogni test"""
        # Mock pygame per evitare apertura finestre durante i test
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.font.Font'):
            self.game = Game()
            
    def tearDown(self):
        """Cleanup dopo ogni test"""
        # Non chiamiamo pygame.quit() nei test mock
        pass

    def test_init(self):
        """Test inizializzazione del game"""
        self.assertTrue(self.game.running)
        self.assertEqual(self.game.state, GAME_STATE_MENU)
        self.assertIsNotNone(self.game.player)
        self.assertEqual(self.game.keys_pressed, {})

    def test_initial_state_is_menu(self):
        """Test che lo stato iniziale sia il menu"""
        self.assertEqual(self.game.state, GAME_STATE_MENU)

    def test_player_initialization(self):
        """Test che il player venga inizializzato correttamente"""
        self.assertIsNotNone(self.game.player)
        self.assertEqual(self.game.player.x, 100)

    @patch('pygame.event.get')
    def test_handle_quit_event(self, mock_event_get):
        """Test gestione evento quit"""
        mock_quit_event = Mock()
        mock_quit_event.type = pygame.QUIT
        mock_event_get.return_value = [mock_quit_event]
        
        self.game._handle_events()
        self.assertFalse(self.game.running)

    @patch('pygame.event.get')
    def test_menu_to_playing_transition(self, mock_event_get):
        """Test transizione da menu a playing con ENTER"""
        mock_keydown_event = Mock()
        mock_keydown_event.type = pygame.KEYDOWN
        mock_keydown_event.key = pygame.K_RETURN
        mock_event_get.return_value = [mock_keydown_event]
        
        self.game.state = GAME_STATE_MENU
        self.game._handle_events()
        self.assertEqual(self.game.state, GAME_STATE_PLAYING)

    @patch('pygame.event.get')
    def test_playing_to_paused_transition(self, mock_event_get):
        """Test transizione da playing a paused con P"""
        mock_keydown_event = Mock()
        mock_keydown_event.type = pygame.KEYDOWN
        mock_keydown_event.key = pygame.K_p
        mock_event_get.return_value = [mock_keydown_event]
        
        self.game.state = GAME_STATE_PLAYING
        self.game._handle_events()
        self.assertEqual(self.game.state, GAME_STATE_PAUSED)

    @patch('pygame.event.get')
    def test_paused_to_playing_transition(self, mock_event_get):
        """Test transizione da paused a playing con P"""
        mock_keydown_event = Mock()
        mock_keydown_event.type = pygame.KEYDOWN
        mock_keydown_event.key = pygame.K_p
        mock_event_get.return_value = [mock_keydown_event]
        
        self.game.state = GAME_STATE_PAUSED
        self.game._handle_events()
        self.assertEqual(self.game.state, GAME_STATE_PLAYING)

    def test_update_player_when_playing(self):
        """Test che il player si aggiorni quando lo stato è PLAYING"""
        self.game.state = GAME_STATE_PLAYING
        self.game.player = Mock()
        self.game.player.is_alive.return_value = True
        self.game.player.x = 100
        self.game.player.width = 32
        
        self.game._update()
        
        self.game.player.update.assert_called_once_with(self.game.keys_pressed)

    def test_game_over_when_player_dies(self):
        """Test transizione a game over quando il player muore"""
        self.game.state = GAME_STATE_PLAYING
        self.game.player = Mock()
        self.game.player.is_alive.return_value = False
        self.game.player.x = 100
        self.game.player.width = 32
        
        self.game._update()
        
        self.assertEqual(self.game.state, GAME_STATE_GAME_OVER)

    def test_player_boundary_left(self):
        """Test che il player non esca dai confini a sinistra"""
        self.game.state = GAME_STATE_PLAYING
        self.game.player.is_alive = Mock(return_value=True)
        self.game.player.x = -10  # Fuori dai confini
        self.game.player.width = 32
        
        self.game._update()
        
        self.assertEqual(self.game.player.x, 0)

    def test_player_boundary_right(self):
        """Test che il player non esca dai confini a destra"""
        self.game.state = GAME_STATE_PLAYING
        self.game.player.is_alive = Mock(return_value=True)
        self.game.player.x = SCREEN_WIDTH + 10  # Fuori dai confini
        self.game.player.width = 32
        
        self.game._update()
        
        self.assertEqual(self.game.player.x, SCREEN_WIDTH - 32)

    def test_restart_game(self):
        """Test riavvio del gioco"""
        old_player = self.game.player
        self.game._restart_game()
        
        # Dovrebbe essere creato un nuovo player
        self.assertNotEqual(self.game.player, old_player)
        self.assertEqual(self.game.state, GAME_STATE_PLAYING)

    @patch('pygame.event.get')
    def test_restart_from_game_over(self, mock_event_get):
        """Test riavvio da game over con R"""
        mock_keydown_event = Mock()
        mock_keydown_event.type = pygame.KEYDOWN
        mock_keydown_event.key = pygame.K_r
        mock_event_get.return_value = [mock_keydown_event]
        
        self.game.state = GAME_STATE_GAME_OVER
        old_player = self.game.player
        self.game._handle_events()
        
        # Dovrebbe essere riavviato il gioco
        self.assertNotEqual(self.game.player, old_player)
        self.assertEqual(self.game.state, GAME_STATE_PLAYING)

    @patch('pygame.event.get')
    def test_keyup_event(self, mock_event_get):
        """Test gestione evento keyup"""
        # Prima premiamo un tasto
        self.game.keys_pressed[pygame.K_LEFT] = True
        
        # Poi lo rilasciamo
        mock_keyup_event = Mock()
        mock_keyup_event.type = pygame.KEYUP
        mock_keyup_event.key = pygame.K_LEFT
        mock_event_get.return_value = [mock_keyup_event]
        
        self.game._handle_events()
        
        self.assertFalse(self.game.keys_pressed.get(pygame.K_LEFT, False))


if __name__ == "__main__":
    unittest.main() 