import sys
import os
import platform
import shutil
import subprocess
from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QColor, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
)

from scraper_module import ScraperRegistry, ScraperWorker
from documentation_list import DOCUMENTATION_SOURCES


class DocumentationScraperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Documentation Scraper")
        self.setGeometry(300, 300, 700, 200)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Documentation Scraper")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Documentation selection
        select_label = QLabel("Select Documentation to Scrape:")
        main_layout.addWidget(select_label)
        
        # Combo box and button layout
        hbox = QHBoxLayout()
        self.doc_combo = QComboBox()
        self.populate_combo_box()
        hbox.addWidget(self.doc_combo, 3)
        
        self.scrape_button = QPushButton("Start Scraping")
        self.scrape_button.clicked.connect(self.start_scraping)
        hbox.addWidget(self.scrape_button, 1)
        
        main_layout.addLayout(hbox)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setTextFormat(Qt.RichText)
        self.status_label.setOpenExternalLinks(False)
        self.status_label.linkActivated.connect(self.open_folder)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.status_label.setText(
            '<span style="color:#4CAF50;"><b>Pages scraped:</b></span> 0'
        )
        main_layout.addWidget(self.status_label)
        
        # Info label
        info_label = QLabel(
            "Note: Scraped documentation will be saved in the 'Scraped_Documentation' folder."
        )
        info_label.setStyleSheet("color: gray; font-size: 11px;")
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
        
        main_layout.addStretch()
        
        self.current_folder = ""
        self.current_doc_name = ""
        self.worker = None
        self.thread = None
        
        self.apply_stylesheet()
    
    def apply_stylesheet(self):
        """Apply a dark theme stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox:hover {
                border: 1px solid #777777;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #ffffff;
                selection-background-color: #0d47a1;
            }
            QPushButton {
                background-color: #0d47a1;
                color: #ffffff;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0a3d91;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #999999;
            }
        """)
    
    def populate_combo_box(self):
        """Populate combo box with documentation options"""
        doc_options = sorted(DOCUMENTATION_SOURCES.keys(), key=str.lower)
        model = QStandardItemModel()
        
        script_dir = Path(__file__).parent
        scraped_dir = script_dir / "Scraped_Documentation"
        
        for doc in doc_options:
            folder = DOCUMENTATION_SOURCES[doc]["folder"]
            folder_path = scraped_dir / folder
            item = QStandardItem(doc)
            
            # Mark already scraped docs in red
            if folder_path.exists():
                item.setForeground(QColor("#e75959"))
            
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            model.appendRow(item)
        
        self.doc_combo.setModel(model)
    
    def start_scraping(self):
        """Start the scraping process"""
        selected_doc = self.doc_combo.currentText()
        doc_info = DOCUMENTATION_SOURCES.get(selected_doc)
        
        if not doc_info or "URL" not in doc_info or "folder" not in doc_info:
            QMessageBox.critical(
                self,
                "Error",
                "Incomplete configuration for the selected documentation."
            )
            return
        
        url = doc_info["URL"]
        folder = doc_info["folder"]
        scraper_name = doc_info.get("scraper_class", "BaseScraper")
        scraper_class = ScraperRegistry.get_scraper(scraper_name)
        
        script_dir = Path(__file__).parent
        self.current_folder = script_dir / "Scraped_Documentation" / folder
        self.current_doc_name = selected_doc
        
        # Check if folder exists
        if self.current_folder.exists():
            msg_box = QMessageBox(
                QMessageBox.Warning,
                "Existing Folder Warning",
                f"Folder already exists for '{selected_doc}'",
                QMessageBox.Ok | QMessageBox.Cancel,
                self,
            )
            msg_box.setInformativeText(
                "Proceeding will delete its contents and start over."
            )
            msg_box.setDefaultButton(QMessageBox.Cancel)
            
            if msg_box.exec() == QMessageBox.Cancel:
                return

            try:
                shutil.rmtree(self.current_folder)
                self.current_folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to clear existing folder: {e}"
                )
                return
        else:
            self.current_folder.mkdir(parents=True, exist_ok=True)

        self.status_label.setText(
            f'<span style="color:#FF9800;"><b>Scraping '
            f'{self.current_doc_name}...</b></span> '
            f'<span style="color:#4CAF50;"><b>Pages scraped:</b></span> 0 '
            f'<span style="color:#2196F3;"><a href="open_folder" '
            f'style="color:#2196F3;">Open Folder</a></span>'
        )
        self.scrape_button.setEnabled(False)

        self.worker = ScraperWorker(url, str(self.current_folder), scraper_class)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.status_updated.connect(self.update_status)
        self.worker.scraping_finished.connect(self.scraping_finished)
        self.worker.scraping_finished.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def update_status(self, status: str):
        """Update the status label with current progress"""
        self.status_label.setText(
            f'<span style="color:#FF9800;"><b>Scraping '
            f'{self.current_doc_name}...</b></span> '
            f'<span style="color:#4CAF50;"><b>Pages scraped:</b></span> '
            f'{status} '
            f'<span style="color:#2196F3;"><a href="open_folder" '
            f'style="color:#2196F3;">Open Folder</a></span>'
        )

    def scraping_finished(self):
        """Handle scraping completion"""
        self.scrape_button.setEnabled(True)

        final_count = len([
            f for f in self.current_folder.iterdir()
            if f.suffix == ".html"
        ])
        
        self.status_label.setText(
            f'<span style="color:#4CAF50;"><b>Scraping '
            f'{self.current_doc_name} completed!</b></span> '
            f'<span style="color:#4CAF50;"><b>Pages scraped:</b></span> '
            f'{final_count} '
            f'<span style="color:#2196F3;"><a href="open_folder" '
            f'style="color:#2196F3;">Open Folder</a></span>'
        )

        self.populate_combo_box()
        idx = self.doc_combo.findText(self.current_doc_name)
        if idx >= 0:
            self.doc_combo.setCurrentIndex(idx)

        QMessageBox.information(
            self,
            "Scraping Complete",
            f"Successfully scraped {final_count} pages from '{self.current_doc_name}'.\n\n"
            f"Files saved to:\n{self.current_folder}"
        )

    def open_folder(self, link: str):
        """Open the scraped documentation folder"""
        if link == "open_folder" and self.current_folder:
            system = platform.system()
            folder_path = str(self.current_folder)

            try:
                if system == "Windows":
                    os.startfile(folder_path)
                elif system == "Darwin":  # macOS
                    subprocess.Popen(["open", folder_path])
                else:  # Linux / BSD
                    subprocess.Popen(["xdg-open", folder_path])
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Could not open folder: {e}"
                )

    def closeEvent(self, event):
        """Clean up when closing the application"""
        try:
            if self.thread and self.thread.isRunning():
                reply = QMessageBox.question(
                    self,
                    "Scraping in Progress",
                    "Scraping is still in progress. Are you sure you want to quit?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.No:
                    event.ignore()
                    return

                self.thread.quit()
                self.thread.wait(2000)
        except RuntimeError:
            # C++ object already deleted, nothing to clean up
            pass

        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Documentation Scraper")
    
    window = DocumentationScraperGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()