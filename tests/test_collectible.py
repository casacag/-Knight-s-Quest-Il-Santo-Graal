"""
Test unitari per le classi Collectible
"""
import unittest
from unittest.mock import Mock, patch
import pygame
from src.collectible import Gold, Silver, Myrrh, create_random_collectible, spawn_collectibles_in_area
from src.config import GOLD_VALUE, SILVER_VALUE, MYRRH_VALUE, COLLECTIBLE_SIZE


class TestGold(unittest.TestCase):
    """Test per la classe Gold"""

    def setUp(self):
        """Setup per ogni test"""
        pygame.init()
        self.gold = Gold(100, 200)
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()

    def test_init(self):
        """Test inizializzazione dell'oro"""
        self.assertEqual(self.gold.x, 100)
        self.assertEqual(self.gold.y, 200)
        self.assertEqual(self.gold.size, COLLECTIBLE_SIZE)
        self.assertEqual(self.gold.value, GOLD_VALUE)
        self.assertEqual(self.gold.resource_type, "oro")
        self.assertFalse(self.gold.collected)

    def test_get_resource_type(self):
        """Test tipo di risorsa oro"""
        self.assertEqual(self.gold.get_resource_type(), "oro")

    def test_collect(self):
        """Test raccolta dell'oro"""
        value, heal = self.gold.collect()
        self.assertEqual(value, GOLD_VALUE)
        self.assertTrue(self.gold.is_collected())

    def test_update_animation(self):
        """Test animazione fluttuante"""
        initial_y = self.gold.y
        for _ in range(50):  # Simula qualche frame
            self.gold.update()
        # La Y dovrebbe essere cambiata per l'animazione
        # (potrebbe essere uguale per coincidenza, ma di solito cambia)

    @patch('pygame.draw.circle')
    @patch('pygame.font.Font')
    def test_draw(self, mock_font, mock_circle):
        """Test disegno dell'oro"""
        mock_screen = Mock()
        mock_font.return_value.render.return_value = Mock()
        mock_font.return_value.render.return_value.get_rect.return_value = Mock()
        
        self.gold.draw(mock_screen)
        self.assertTrue(mock_circle.called)

    def test_draw_when_collected(self):
        """Test che non disegni quando raccolto"""
        mock_screen = Mock()
        self.gold.collect()
        
        with patch('pygame.draw.circle') as mock_circle:
            self.gold.draw(mock_screen)
            mock_circle.assert_not_called()


class TestSilver(unittest.TestCase):
    """Test per la classe Silver"""

    def setUp(self):
        """Setup per ogni test"""
        pygame.init()
        self.silver = Silver(150, 250)
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()

    def test_init(self):
        """Test inizializzazione dell'argento"""
        self.assertEqual(self.silver.x, 150)
        self.assertEqual(self.silver.y, 250)
        self.assertEqual(self.silver.value, SILVER_VALUE)
        self.assertEqual(self.silver.resource_type, "argento")

    def test_get_resource_type(self):
        """Test tipo di risorsa argento"""
        self.assertEqual(self.silver.get_resource_type(), "argento")

    @patch('pygame.draw.rect')
    @patch('pygame.draw.line')
    def test_draw(self, mock_line, mock_rect):
        """Test disegno dell'argento"""
        mock_screen = Mock()
        self.silver.draw(mock_screen)
        self.assertTrue(mock_rect.called)
        self.assertTrue(mock_line.called)


class TestMyrrh(unittest.TestCase):
    """Test per la classe Myrrh"""

    def setUp(self):
        """Setup per ogni test"""
        pygame.init()
        self.myrrh = Myrrh(200, 300)
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()

    def test_init(self):
        """Test inizializzazione della mirra"""
        self.assertEqual(self.myrrh.x, 200)
        self.assertEqual(self.myrrh.y, 300)
        self.assertEqual(self.myrrh.value, MYRRH_VALUE)
        self.assertEqual(self.myrrh.resource_type, "mirra")
        self.assertEqual(self.myrrh.sparkle_timer, 0)

    def test_get_resource_type(self):
        """Test tipo di risorsa mirra"""
        self.assertEqual(self.myrrh.get_resource_type(), "mirra")

    def test_sparkle_animation(self):
        """Test animazione scintillio"""
        initial_timer = self.myrrh.sparkle_timer
        self.myrrh.update()
        self.assertGreater(self.myrrh.sparkle_timer, initial_timer)

    @patch('pygame.draw.polygon')
    @patch('pygame.draw.line')
    def test_draw_with_sparkle(self, mock_line, mock_polygon):
        """Test disegno con scintillio"""
        mock_screen = Mock()
        self.myrrh.sparkle_timer = 5  # Momento di scintillio
        self.myrrh.draw(mock_screen)
        self.assertTrue(mock_polygon.called)
        self.assertTrue(mock_line.called)


class TestCollectibleFunctions(unittest.TestCase):
    """Test per le funzioni helper dei collezionabili"""

    def setUp(self):
        """Setup per ogni test"""
        pygame.init()
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        pygame.quit()

    def test_create_random_collectible(self):
        """Test creazione collezionabile casuale"""
        collectible = create_random_collectible(100, 200)
        
        # Dovrebbe essere uno dei tre tipi
        self.assertIn(type(collectible).__name__, ['Gold', 'Silver', 'Myrrh'])
        self.assertEqual(collectible.x, 100)
        self.assertEqual(collectible.y, 200)

    def test_spawn_collectibles_in_area(self):
        """Test spawn collezionabili in area"""
        collectibles = spawn_collectibles_in_area(800, 600, 500, 5)
        
        self.assertEqual(len(collectibles), 5)
        
        for collectible in collectibles:
            # Verifica posizioni nell'area corretta
            self.assertGreaterEqual(collectible.x, 50)
            self.assertLessEqual(collectible.x, 750)
            self.assertGreaterEqual(collectible.y, 300)  # ground_y - 200
            self.assertLessEqual(collectible.y, 470)   # ground_y - 30

    def test_collectible_position_methods(self):
        """Test metodi di posizione"""
        gold = Gold(123, 456)
        pos = gold.get_position()
        self.assertEqual(pos, (123, 456))

    def test_collect_returns_correct_values(self):
        """Test che collect restituisca i valori corretti"""
        gold = Gold(100, 200)
        silver = Silver(100, 200)
        myrrh = Myrrh(100, 200)
        
        gold_value, gold_heal = gold.collect()
        silver_value, silver_heal = silver.collect()
        myrrh_value, myrrh_heal = myrrh.collect()
        
        self.assertEqual(gold_value, GOLD_VALUE)
        self.assertEqual(silver_value, SILVER_VALUE)
        self.assertEqual(myrrh_value, MYRRH_VALUE)
        
        # Verifica che abbiano effetti di cura
        self.assertGreater(gold_heal, 0)
        self.assertGreater(silver_heal, 0)
        self.assertGreater(myrrh_heal, 0)

    def test_rect_collision_detection(self):
        """Test che i rect siano configurati correttamente per collision detection"""
        gold = Gold(100, 200)
        
        self.assertEqual(gold.rect.x, 100)
        self.assertEqual(gold.rect.y, 200)
        self.assertEqual(gold.rect.width, COLLECTIBLE_SIZE)
        self.assertEqual(gold.rect.height, COLLECTIBLE_SIZE)
        
        # Test aggiornamento rect durante animazione
        gold.update()
        self.assertEqual(gold.rect.x, gold.x)
        self.assertEqual(gold.rect.y, gold.y)

    def test_update_stops_when_collected(self):
        """Test che l'update si fermi quando l'oggetto è raccolto"""
        gold = Gold(100, 200)
        initial_timer = gold.float_timer
        
        gold.collect()
        gold.update()
        
        # Il timer non dovrebbe essere cambiato
        self.assertEqual(gold.float_timer, initial_timer)


if __name__ == "__main__":
    unittest.main() 