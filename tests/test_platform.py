"""
Test per il modulo delle piattaforme
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Aggiunge src al path per gli import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.platform import Platform, Ramp, create_default_platforms, create_default_ramps
from src.platform import check_platform_collision, check_ramp_collision


class TestPlatform(unittest.TestCase):
    """Test per la classe Platform"""
    
    def setUp(self):
        """Configurazione iniziale per ogni test"""
        self.platform = Platform(100, 200, 150, 20)
        
    def test_platform_initialization(self):
        """Test inizializzazione piattaforma"""
        self.assertEqual(self.platform.x, 100)
        self.assertEqual(self.platform.y, 200)
        self.assertEqual(self.platform.width, 150)
        self.assertEqual(self.platform.height, 20)
        
    def test_platform_get_top_y(self):
        """Test metodo get_top_y"""
        self.assertEqual(self.platform.get_top_y(), 200)
        
    def test_platform_contains_point(self):
        """Test collision detection point"""
        # Punto dentro la piattaforma
        self.assertTrue(self.platform.contains_point(150, 210))
        
        # Punto fuori dalla piattaforma
        self.assertFalse(self.platform.contains_point(50, 210))
        self.assertFalse(self.platform.contains_point(150, 150))
        
    @patch('pygame.draw.rect')
    @patch('pygame.Rect')
    def test_platform_draw(self, mock_rect, mock_draw):
        """Test disegno piattaforma"""
        mock_screen = Mock()
        
        self.platform.draw(mock_screen)
        
        # Verifica che draw.rect sia stato chiamato
        self.assertTrue(mock_draw.called)


class TestRamp(unittest.TestCase):
    """Test per la classe Ramp"""
    
    def setUp(self):
        """Configurazione iniziale per ogni test"""
        self.ramp_up = Ramp(100, 300, 100, 50, slope_up=True)
        self.ramp_down = Ramp(100, 300, 100, 50, slope_up=False)
        
    def test_ramp_initialization(self):
        """Test inizializzazione rampa"""
        self.assertEqual(self.ramp_up.x, 100)
        self.assertEqual(self.ramp_up.y, 300)
        self.assertEqual(self.ramp_up.width, 100)
        self.assertEqual(self.ramp_up.height, 50)
        self.assertTrue(self.ramp_up.slope_up)
        self.assertFalse(self.ramp_down.slope_up)
        
    def test_ramp_get_height_at_x_slope_up(self):
        """Test calcolo altezza rampa che sale"""
        # Inizio rampa (x=100)
        self.assertEqual(self.ramp_up.get_height_at_x(100), 300)
        
        # Fine rampa (x=200) 
        self.assertEqual(self.ramp_up.get_height_at_x(200), 250)
        
        # Metà rampa (x=150)
        self.assertEqual(self.ramp_up.get_height_at_x(150), 275)
        
        # Fuori dalla rampa
        self.assertEqual(self.ramp_up.get_height_at_x(50), 300)
        self.assertEqual(self.ramp_up.get_height_at_x(250), 300)
        
    def test_ramp_get_height_at_x_slope_down(self):
        """Test calcolo altezza rampa che scende"""
        # Inizio rampa (x=100) - alto
        self.assertEqual(self.ramp_down.get_height_at_x(100), 250)
        
        # Fine rampa (x=200) - basso
        self.assertEqual(self.ramp_down.get_height_at_x(200), 300)
        
        # Metà rampa (x=150)
        self.assertEqual(self.ramp_down.get_height_at_x(150), 275)
        
    def test_ramp_is_on_ramp(self):
        """Test collision detection con rampa"""
        # Su rampa salita
        self.assertTrue(self.ramp_up.is_on_ramp(150, 275, tolerance=5))
        
        # Fuori toleranza
        self.assertFalse(self.ramp_up.is_on_ramp(150, 260, tolerance=5))
        
        # Fuori dalla rampa orizzontalmente
        self.assertFalse(self.ramp_up.is_on_ramp(50, 275, tolerance=5))
        
    @patch('pygame.draw.polygon')
    def test_ramp_draw(self, mock_draw):
        """Test disegno rampa"""
        mock_screen = Mock()
        
        self.ramp_up.draw(mock_screen)
        
        # Verifica che draw.polygon sia stato chiamato
        self.assertTrue(mock_draw.called)


class TestPlatformFunctions(unittest.TestCase):
    """Test per le funzioni helper delle piattaforme"""
    
    def test_create_default_platforms(self):
        """Test creazione piattaforme predefinite"""
        platforms = create_default_platforms()
        
        self.assertIsInstance(platforms, list)
        self.assertTrue(len(platforms) > 0)
        
        # Verifica che tutti gli elementi siano Platform
        for platform in platforms:
            self.assertIsInstance(platform, Platform)
            
    def test_create_default_ramps(self):
        """Test creazione rampe predefinite"""
        ramps = create_default_ramps()
        
        self.assertIsInstance(ramps, list)
        self.assertTrue(len(ramps) > 0)
        
        # Verifica che tutti gli elementi siano Ramp
        for ramp in ramps:
            self.assertIsInstance(ramp, Ramp)
            
    @patch('pygame.Rect')
    def test_check_platform_collision_no_collision(self, mock_rect):
        """Test collision detection piattaforme - nessuna collisione"""
        mock_player_rect = Mock()
        platforms = [Platform(100, 200, 100, 15)]
        
        # Player non sta cadendo
        is_on_platform, platform_y = check_platform_collision(mock_player_rect, -5, platforms)
        self.assertFalse(is_on_platform)
        self.assertEqual(platform_y, 0)
        
    @patch('pygame.Rect')
    def test_check_platform_collision_with_collision(self, mock_rect):
        """Test collision detection piattaforme - con collisione"""
        # Mock del rect del player
        mock_player_rect = Mock()
        mock_player_rect.bottom = 205
        mock_player_rect.right = 150
        mock_player_rect.left = 125
        
        platforms = [Platform(100, 200, 100, 15)]
        
        # Player sta cadendo e vicino alla piattaforma
        is_on_platform, platform_y = check_platform_collision(mock_player_rect, 5, platforms)
        self.assertTrue(is_on_platform)
        self.assertEqual(platform_y, 200)
        
    @patch('pygame.Rect')
    def test_check_ramp_collision_no_collision(self, mock_rect):
        """Test collision detection rampe - nessuna collisione"""
        mock_player_rect = Mock()
        mock_player_rect.centerx = 50  # Fuori dalla rampa
        mock_player_rect.bottom = 275
        
        ramps = [Ramp(100, 300, 100, 50, slope_up=True)]
        
        is_on_ramp, ramp_y = check_ramp_collision(mock_player_rect, ramps)
        self.assertFalse(is_on_ramp)
        self.assertEqual(ramp_y, 0)
        
    @patch('pygame.Rect')  
    def test_check_ramp_collision_with_collision(self, mock_rect):
        """Test collision detection rampe - con collisione"""
        mock_player_rect = Mock()
        mock_player_rect.centerx = 150  # Metà rampa
        mock_player_rect.bottom = 275   # Altezza corretta
        
        ramps = [Ramp(100, 300, 100, 50, slope_up=True)]
        
        is_on_ramp, ramp_y = check_ramp_collision(mock_player_rect, ramps)
        self.assertTrue(is_on_ramp)
        self.assertEqual(ramp_y, 275)


if __name__ == '__main__':
    unittest.main() 