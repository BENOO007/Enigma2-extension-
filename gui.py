"""
Enigma2 Extension - PyQt5 GUI
Main graphical user interface for the application
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QLabel, 
                             QListWidget, QListWidgetItem, QTabs, QTabWidget,
                             QGridLayout, QMessageBox, QProgressBar, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap
import requests
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SearchThread(QThread):
    """Worker thread for searching content"""
    search_finished = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, query, search_type):
        super().__init__()
        self.query = query
        self.search_type = search_type
    
    def run(self):
        try:
            # TODO: Implement actual search logic
            results = []
            self.search_finished.emit(results)
        except Exception as e:
            logger.error(f"Search error: {e}")
            self.error_occurred.emit(str(e))


class MovieTab(QWidget):
    """Tab for searching movies"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.search_thread = None
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search Movies:")
        search_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter movie name...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_movies)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_result_selected)
        layout.addWidget(QLabel("Search Results:"))
        layout.addWidget(self.results_list)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.play_button = QPushButton("▶ Play")
        self.play_button.clicked.connect(self.play_selected)
        self.favorite_button = QPushButton("♥ Add to Favorites")
        self.favorite_button.clicked.connect(self.add_to_favorites)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.favorite_button)
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def search_movies(self):
        """Search for movies"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Input Error", "Please enter a movie name!")
            return
        
        logger.info(f"Searching for movies: {query}")
        self.progress_bar.setVisible(True)
        
        self.search_thread = SearchThread(query, "movie")
        self.search_thread.search_finished.connect(self.display_results)
        self.search_thread.error_occurred.connect(self.handle_search_error)
        self.search_thread.start()
    
    def display_results(self, results):
        """Display search results"""
        self.results_list.clear()
        if not results:
            QMessageBox.information(self, "No Results", "No movies found!")
        else:
            for result in results:
                item = QListWidgetItem(result.get("title", "Unknown"))
                self.results_list.addItem(item)
        self.progress_bar.setVisible(False)
    
    def handle_search_error(self, error):
        """Handle search errors"""
        QMessageBox.critical(self, "Search Error", f"Error: {error}")
        self.progress_bar.setVisible(False)
    
    def on_result_selected(self, item):
        """Handle result selection"""
        logger.info(f"Selected movie: {item.text()}")
    
    def play_selected(self):
        """Play selected movie"""
        current_item = self.results_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Selection Error", "Please select a movie!")
            return
        logger.info(f"Playing movie: {current_item.text()}")
        QMessageBox.information(self, "Playing", f"Playing: {current_item.text()}")
    
    def add_to_favorites(self):
        """Add selected movie to favorites"""
        current_item = self.results_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Selection Error", "Please select a movie!")
            return
        logger.info(f"Added to favorites: {current_item.text()}")
        QMessageBox.information(self, "Added", f"Added to favorites: {current_item.text()}")


class SeriesTab(QWidget):
    """Tab for searching series"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search Series:")
        search_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter series name...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_series)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)
        
        # Results list
        self.results_list = QListWidget()
        layout.addWidget(QLabel("Search Results:"))
        layout.addWidget(self.results_list)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.play_button = QPushButton("▶ Play")
        self.favorite_button = QPushButton("♥ Add to Favorites")
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.favorite_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def search_series(self):
        """Search for series"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Input Error", "Please enter a series name!")
            return
        logger.info(f"Searching for series: {query}")


class FavoritesTab(QWidget):
    """Tab for viewing favorites"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        title = QLabel("My Favorites")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Favorites list
        self.favorites_list = QListWidget()
        layout.addWidget(self.favorites_list)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.play_button = QPushButton("▶ Play")
        self.remove_button = QPushButton("✕ Remove")
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.remove_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)


class SettingsTab(QWidget):
    """Tab for settings"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout()
        
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Enigma2 Connection Settings
        connection_layout = QGridLayout()
        
        connection_layout.addWidget(QLabel("Enigma2 Host:"), 0, 0)
        self.host_input = QLineEdit()
        self.host_input.setText("192.168.1.100")
        connection_layout.addWidget(self.host_input, 0, 1)
        
        connection_layout.addWidget(QLabel("Port:"), 1, 0)
        self.port_input = QLineEdit()
        self.port_input.setText("8001")
        connection_layout.addWidget(self.port_input, 1, 1)
        
        connection_layout.addWidget(QLabel("Theme:"), 2, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        connection_layout.addWidget(self.theme_combo, 2, 1)
        
        layout.addLayout(connection_layout)
        
        # Save settings button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def save_settings(self):
        """Save settings"""
        logger.info("Settings saved")
        QMessageBox.information(self, "Success", "Settings saved successfully!")


class Enigma2ExtensionGUI(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enigma2 Extension - Movie & Series Library")
        self.setGeometry(100, 100, 900, 600)
        self.init_ui()
        logger.info("GUI initialized")
    
    def init_ui(self):
        """Initialize main UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel("🎬 Enigma2 Extension - Movie & Series Library")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        self.movie_tab = MovieTab()
        self.series_tab = SeriesTab()
        self.favorites_tab = FavoritesTab()
        self.settings_tab = SettingsTab()
        
        self.tabs.addTab(self.movie_tab, "🎬 Movies")
        self.tabs.addTab(self.series_tab, "📺 Series")
        self.tabs.addTab(self.favorites_tab, "♥ Favorites")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")
        
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
    
    def closeEvent(self, event):
        """Handle window close event"""
        logger.info("Application closed")
        event.accept()


def main():
    """Main entry point for GUI"""
    app = QApplication(sys.argv)
    window = Enigma2ExtensionGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()