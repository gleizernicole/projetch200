import sys
import os
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

# Force PyQt5 to work in headless environments (like CI or no display)
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer

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
        cls.app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    
    def setUp(self):
        """Set up the test fixture before each test"""
        # Use a mock timer to avoid actual time-based operations
        with patch('PyQt5.QtCore.QTimer', autospec=True) as mock_timer:
            self.mock_timer = mock_timer.return_value
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
    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_timer_update(self, mock_warning):
        """Test that the timer updates correctly"""
        # Prepare timer and quiz state
        self.periodic_table.quiz_active = True
        self.periodic_table.time_remaining = 2
        self.periodic_table.timer_display.setText("Time remaining: 2s")
        
        # Manually call update_timer method
        self.periodic_table.update_timer()
        
        # Check that time was reduced by 1
        self.assertEqual(self.periodic_table.time_remaining, 1)
        self.assertEqual(self.periodic_table.timer_display.text(), "Time remaining: 1s")
    
    # Quiz Functionality Tests
    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    def test_quiz_initialization(self, mock_get_item):
        """Test quiz initialization with different quiz types"""
        # Prepare mock for multiple choice
        mock_get_item.return_value = ("Multiple Choice", True)
        
        # Use mock to prevent actual dialog from showing
        with patch.object(self.periodic_table, 'ask_question', return_value=None):
            # Call start_quiz
            self.periodic_table.start_quiz()
            
            # Verify quiz state
            self.assertEqual(self.periodic_table.quiz_type, "Multiple Choice")
            self.assertEqual(self.periodic_table.score, 0)
            self.assertEqual(self.periodic_table.question_count, 0)
            self.assertTrue(self.periodic_table.quiz_active)
    
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
    
    # Mocked Answer Checking Tests
    def test_check_answer_correct(self):
        """Test checking correct answers"""
        # Manually set up test scenario
        self.periodic_table.current_answer = "Hydrogen"
        self.periodic_table.score = 5
        
        # Create mock for QMessageBox to prevent actual dialog
        with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info:
            # Check exact match
            self.periodic_table.check_answer("Hydrogen")
            self.assertEqual(self.periodic_table.score, 6)
            mock_info.assert_called_once()
        
        # Reset for case insensitive
        self.periodic_table.score = 5
        
        # Check case insensitive
        with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info:
            self.periodic_table.check_answer("hydrogen")
            self.assertEqual(self.periodic_table.score, 6)
            mock_info.assert_called_once()
    
    def test_check_answer_incorrect(self):
        """Test checking incorrect answers"""
        # Manually set up test scenario
        self.periodic_table.current_answer = "Hydrogen"
        self.periodic_table.score = 5
        
        # Use mock to prevent actual dialog
        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            # Check incorrect answer
            self.periodic_table.check_answer("Helium")
            self.assertEqual(self.periodic_table.score, 5)  # Score should not change
            mock_warning.assert_called_once()
    
    # Element Information Tests
    def test_get_production_content(self):
        """Test generating production methods content"""
        # Create a temporary mock for production_methods
        mock_production = {
            "Test": {
                "industrial": ["Method 1", "Method 2"],
                "laboratory": {
                    "reaction": "Test Reaction",
                    "conditions": "Test Conditions"
                }
            }
        }
        
        # Patch the production_methods with our test data
        with patch.dict('periodictable.utils.production_methods', mock_production):
            content = self.periodic_table.get_production_content("Test")
            
            # Check that content includes expected information
            self.assertIn("Industrial:", content)
            self.assertIn("Method 1", content)
            self.assertIn("Laboratory:", content)
            self.assertIn("Test Reaction", content)
    
    def test_multiple_choice_answer_selection(self):
        """Test multiple choice answer selection"""
        # Create a mock dialog
        mock_dialog = MagicMock()
        
        # Simulate answer selection
        answer = "Helium"
        self.periodic_table.mc_answer_selected(answer, mock_dialog)
        
        # Check that the user answer was set correctly
        self.assertEqual(self.periodic_table.user_answer, answer)
        
        # Verify dialog was accepted
        mock_dialog.accept.assert_called_once()
    
    # Timeout Handling Test
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_handle_timeout(self, mock_warning):
        """Test handling quiz timeout"""
        # Set up test scenario with proper quiz state
        self.periodic_table.quiz_active = True
        self.periodic_table.current_answer = "Carbon"
        self.periodic_table.question_count = 3
        
        # Create a mock current dialog
        self.periodic_table.current_dialog = MagicMock()
        
        # Prevent actual question asking
        with patch.object(self.periodic_table, 'ask_question', return_value=None):
            # Call handle timeout
            self.periodic_table.handle_timeout()
            
            # Verify warning was shown
            mock_warning.assert_called_once()
            
            # Check that question count was incremented
            self.assertEqual(self.periodic_table.question_count, 4)
            
            # Verify dialog was closed
            self.periodic_table.current_dialog.close.assert_called_once()
    
    # Additional test for handling quiz timeout with timer at zero
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_update_timer_timeout(self, mock_warning):
        """Test timer update with timeout"""
        # Setup quiz state
        self.periodic_table.quiz_active = True
        self.periodic_table.time_remaining = 1
        self.periodic_table.current_answer = "Oxygen"
        self.periodic_table.current_dialog = MagicMock()
        
        # Mock the handle_timeout method to prevent it from executing
        with patch.object(self.periodic_table, 'handle_timeout') as mock_handle_timeout:
            # Call update_timer which should trigger timeout
            self.periodic_table.update_timer()
            
            # Verify time has reached 0
            self.assertEqual(self.periodic_table.time_remaining, 0)
            
            # Verify handle_timeout was called
            mock_handle_timeout.assert_called_once()

if __name__ == '__main__':
    unittest.main()
