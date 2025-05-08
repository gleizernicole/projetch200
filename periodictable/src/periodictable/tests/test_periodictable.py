import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Force PyQt5 to work in headless environments (like CI or no display)
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Set up path so we can import the main app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we can import your modules
from periodictable.utils import PeriodicTableApp
from periodictable.elements_data import elements, positions, colors, production_methods

class TestPeriodicTableApp(unittest.TestCase):
    """Test case for the PeriodicTableApp class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the QApplication once for all tests"""
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        """Set up the test fixture before each test"""
        self.periodic_table = PeriodicTableApp()
    
    def tearDown(self):
        """Clean up after each test"""
        self.periodic_table.close()
    
    # UI Initialization Tests
    def test_window_title(self):
        """Test that the window title is set correctly"""
        self.assertEqual(self.periodic_table.windowTitle(), "Interactive Periodic Table + Quiz 🎲")
    
    def test_score_display_initialization(self):
        """Test that the score display is initialized to zero"""
        self.assertEqual(self.periodic_table.score_display.text(), "Score: 0")
    
    def test_quiz_button_initialization(self):
        """Test that the quiz button is initialized with correct text"""
        self.assertEqual(self.periodic_table.quiz_btn.text(), "🎲 Start Quiz")
    
    def test_element_grid_initialization(self):
        """Test that the element grid is populated with all elements"""
        # Count the number of buttons in the grid
        button_count = 0
        for i in range(self.periodic_table.element_grid.count()):
            widget = self.periodic_table.element_grid.itemAt(i).widget()
            if widget and widget.text() in elements:
                button_count += 1
        
        # We expect one button per element in positions dictionary
        self.assertEqual(button_count, len(positions))
    
    # Timer Tests
    def test_timer_initialization(self):
        """Test that the timer is initialized correctly"""
        self.assertEqual(self.periodic_table.time_remaining, 30)
        self.assertEqual(self.periodic_table.timer_display.text(), "Time remaining: 30s")
        self.assertEqual(self.periodic_table.quiz_timer.interval(), 1000)  # 1 second interval
    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_timer_update(self, mock_warning):
        """Test that the timer updates correctly"""
        self.periodic_table.time_remaining = 2
        self.periodic_table.timer_display.setText("Time remaining: 2s")
        self.periodic_table.update_timer()
        
        # Check that time was reduced by 1
        self.assertEqual(self.periodic_table.time_remaining, 1)
        self.assertEqual(self.periodic_table.timer_display.text(), "Time remaining: 1s")
        
        # Check timeout handling
        self.periodic_table.update_timer()
        self.assertEqual(self.periodic_table.time_remaining, 0)
        # Verify that a timeout message was shown
        mock_warning.assert_called_once()
    
    # Quiz Functionality Tests
    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    def test_quiz_initialization(self, mock_get_item):
        """Test quiz initialization with different quiz types"""
        # Test multiple choice quiz
        mock_get_item.return_value = ("Multiple Choice", True)
        
        # Mock question dialog to prevent it from showing
        with patch.object(self.periodic_table, 'ask_question', return_value=None):
            self.periodic_table.start_quiz()
            
            self.assertEqual(self.periodic_table.quiz_type, "Multiple Choice")
            self.assertEqual(self.periodic_table.score, 0)
            self.assertEqual(self.periodic_table.question_count, 0)
            self.assertTrue(self.periodic_table.quiz_active)
            
        # Test free response quiz
        mock_get_item.return_value = ("Free Response", True)
        
        with patch.object(self.periodic_table, 'ask_question', return_value=None):
            self.periodic_table.start_quiz()
            
            self.assertEqual(self.periodic_table.quiz_type, "Free Response")
            self.assertTrue(self.periodic_table.quiz_active)
            
        # Test quiz cancellation
        mock_get_item.return_value = ("", False)
        
        original_quiz_active = self.periodic_table.quiz_active
        self.periodic_table.start_quiz()
        self.assertEqual(self.periodic_table.quiz_active, original_quiz_active)  # Should not change
    
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_quiz_completion(self, mock_info):
        """Test quiz completion handling"""
        self.periodic_table.quiz_active = True
        self.periodic_table.question_count = 10
        self.periodic_table.score = 7
        
        self.periodic_table.ask_question()
        
        # Check that the quiz completion message was shown
        mock_info.assert_called_once()
        args = mock_info.call_args[0]
        self.assertIn("Final Score: 7/10", args[1])
        self.assertFalse(self.periodic_table.quiz_active)
    
    def test_normalize_text(self):
        """Test the text normalization function"""
        # Test basic normalization
        self.assertEqual(self.periodic_table.normalize_text("Helium"), "helium")
        
        # Test spaces
        self.assertEqual(self.periodic_table.normalize_text("Carbon Dioxide"), "carbondioxide")
        
        # Test accents
        self.assertEqual(self.periodic_table.normalize_text("Néon"), "neon")
        
        # Test mixed case
        self.assertEqual(self.periodic_table.normalize_text("aLuMiNiUm"), "aluminium")
    
    # Answer Checking Tests
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_check_answer_correct(self, mock_warning, mock_info):
        """Test checking correct answers"""
        self.periodic_table.current_answer = "Hydrogen"
        self.periodic_table.score = 5
        
        # Check exact match
        self.periodic_table.check_answer("Hydrogen")
        self.assertEqual(self.periodic_table.score, 6)
        mock_info.assert_called_once()
        mock_warning.assert_not_called()
        
        # Reset mocks
        mock_info.reset_mock()
        mock_warning.reset_mock()
        
        # Check case insensitive match
        self.periodic_table.check_answer("hydrogen")
        self.assertEqual(self.periodic_table.score, 7)
        mock_info.assert_called_once()
        mock_warning.assert_not_called()
        
        # Reset mocks
        mock_info.reset_mock()
        mock_warning.reset_mock()
        
        # Check with spaces
        self.periodic_table.current_answer = "Carbon Dioxide"
        self.periodic_table.check_answer("carbondioxide")
        self.assertEqual(self.periodic_table.score, 8)
        mock_info.assert_called_once()
        mock_warning.assert_not_called()
    
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_check_answer_incorrect(self, mock_warning, mock_info):
        """Test checking incorrect answers"""
        self.periodic_table.current_answer = "Hydrogen"
        self.periodic_table.score = 5
        
        # Check incorrect answer
        self.periodic_table.check_answer("Helium")
        self.assertEqual(self.periodic_table.score, 5)  # Score should not change
        mock_warning.assert_called_once()
        mock_info.assert_not_called()
        
        # Reset mocks
        mock_info.reset_mock()
        mock_warning.reset_mock()
        
        # Check empty answer
        self.periodic_table.check_answer("")
        self.assertEqual(self.periodic_table.score, 5)  # Score should not change
        mock_warning.assert_called_once()
        mock_info.assert_not_called()
    
    # Element Information Tests
    @patch('PyQt5.QtWidgets.QDialog.exec_')
    def test_show_element_info(self, mock_exec):
        """Test showing element information dialog"""
        # Test with an existing element
        symbol = "H"
        with patch('os.path.exists', return_value=True), \
             patch('PyQt5.QtGui.QPixmap.scaled', return_value=MagicMock()):
            self.periodic_table.show_element_info(symbol)
            mock_exec.assert_called_once()
        
        # Reset mock
        mock_exec.reset_mock()
        
        # Test with missing image
        with patch('os.path.exists', return_value=False):
            self.periodic_table.show_element_info(symbol)
            mock_exec.assert_called_once()
    
    def test_get_production_content(self):
        """Test generating production methods content"""
        # Test with element that has production methods
        symbol = "O"  # Assuming oxygen has production methods
        
        # Mock the element data with production methods
        mock_element = {
            "production": {
                "industrial": ["Fractional distillation of liquid air", "Electrolysis of water"],
                "laboratory": {
                    "reaction": "2H2O2 → 2H2O + O2",
                    "conditions": "Heat with catalyst"
                }
            }
        }
        
        with patch.dict(elements, {symbol: mock_element}):
            content = self.periodic_table.get_production_content(symbol)
            self.assertIn("Industrial:", content)
            self.assertIn("Fractional distillation", content)
            self.assertIn("Laboratory:", content)
            self.assertIn("2H2O2 → 2H2O + O2", content)
        
        # Test with element without production methods
        symbol = "Xx"  # Fictional element
        with patch.dict(elements, {symbol: {}}):
            content = self.periodic_table.get_production_content(symbol)
            self.assertIn("No production methods", content)
    
    # Multiple Choice Answer Tests
    def test_mc_answer_selected(self):
        """Test multiple choice answer selection"""
        mock_dialog = MagicMock()
        answer = "Helium"
        
        self.periodic_table.mc_answer_selected(answer, mock_dialog)
        self.assertEqual(self.periodic_table.user_answer, answer)
        mock_dialog.accept.assert_called_once()
    
    # Quiz Timeout Tests
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_handle_timeout(self, mock_warning):
        """Test handling quiz timeout"""
        self.periodic_table.current_answer = "Carbon"
        self.periodic_table.question_count = 3
        self.periodic_table.current_dialog = MagicMock()
        
        # Mock ask_question to prevent showing dialog
        with patch.object(self.periodic_table, 'ask_question', return_value=None):
            self.periodic_table.handle_timeout()
            
            # Check that warning was shown
            mock_warning.assert_called_once()
            args = mock_warning.call_args[0]
            self.assertIn("Carbon", args[1])  # Current answer should be in message
            
            # Check that question count was incremented
            self.assertEqual(self.periodic_table.question_count, 4)
            
            # Check that dialog was closed
            self.periodic_table.current_dialog.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
