import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QLineEdit, QComboBox, 
                             QProgressBar, QTextEdit, QFileDialog, QGroupBox, 
                             QGridLayout, QMessageBox, QTabWidget, QListWidget,
                             QCheckBox, QSplitter)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPalette, QColor

from converter import VideoConverter
from config import *
from utils import is_valid_video_file, get_output_filepath
from presets import get_preset_names, get_preset_settings, get_preset_description

class ConversionThread(QThread):
    progress_update = pyqtSignal(str)
    conversion_complete = pyqtSignal(bool, str)
    progress_percentage = pyqtSignal(int)
    
    def __init__(self, input_paths, output_dir, settings, batch_mode=False):
        super().__init__()
        self.input_paths = input_paths if isinstance(input_paths, list) else [input_paths]
        self.output_dir = output_dir
        self.settings = settings
        self.batch_mode = batch_mode
        
    def run(self):
        converter = VideoConverter()
        converter.progress_update.connect(self.progress_update.emit)
        
        if self.batch_mode and len(self.input_paths) > 1:
            # Batch conversion
            successful, failed = converter.convert_batch(
                self.input_paths, self.output_dir, self.settings,
                progress_callback=self.progress_percentage.emit
            )
            
            if failed:
                message = f"Batch conversion completed with {len(failed)} failures"
                self.conversion_complete.emit(False, message)
            else:
                self.conversion_complete.emit(True, f"All {successful} videos converted successfully!")
        else:
            # Single conversion
            input_path = self.input_paths[0]
            output_path = get_output_filepath(input_path, self.output_dir, self.settings['format'])
            
            success, message = converter.convert_video(
                input_path, output_path,
                self.settings.get('resolution'),
                self.settings.get('bitrate'),
                self.settings.get('codec')
            )
            self.conversion_complete.emit(success, message)

class VideoConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.conversion_thread = None
        
    def init_ui(self):
        self.setWindowTitle("Modern Video Converter")
        self.setGeometry(100, 100, 1000, 700)
        
        # Set modern dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3c3c3c;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QTextEdit, QListWidget {
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Single conversion tab
        self.single_tab = self.create_single_conversion_tab()
        self.tab_widget.addTab(self.single_tab, "Single Conversion")
        
        # Batch conversion tab
        self.batch_tab = self.create_batch_conversion_tab()
        self.tab_widget.addTab(self.batch_tab, "Batch Conversion")
        
        # Presets tab
        self.presets_tab = self.create_presets_tab()
        self.tab_widget.addTab(self.presets_tab, "Presets")
        
        main_layout.addWidget(self.tab_widget)
        
        # Progress and log section (shared)
        self.create_progress_section(main_layout)
        
    def create_single_conversion_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input section
        input_group = QGroupBox("Input Video")
        input_layout = QHBoxLayout(input_group)
        
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setPlaceholderText("Select input video file...")
        self.browse_input_btn = QPushButton("Browse")
        self.browse_input_btn.clicked.connect(self.browse_input_file)
        
        input_layout.addWidget(self.input_path_edit)
        input_layout.addWidget(self.browse_input_btn)
        
        # Output section
        output_group = QGroupBox("Output Settings")
        output_layout = QGridLayout(output_group)
        
        # Output directory
        output_layout.addWidget(QLabel("Output Directory:"), 0, 0)
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("Select output directory...")
        self.browse_output_btn = QPushButton("Browse")
        self.browse_output_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(self.output_dir_edit, 0, 1)
        output_layout.addWidget(self.browse_output_btn, 0, 2)
        
        # Format
        output_layout.addWidget(QLabel("Format:"), 1, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(SUPPORTED_OUTPUT_FORMATS)
        self.format_combo.setCurrentText(DEFAULT_OUTPUT_FORMAT)
        output_layout.addWidget(self.format_combo, 1, 1, 1, 2)
        
        # Resolution
        output_layout.addWidget(QLabel("Resolution:"), 2, 0)
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(list(RESOLUTION_PRESETS.keys()))
        output_layout.addWidget(self.resolution_combo, 2, 1, 1, 2)
        
        # Codec
        output_layout.addWidget(QLabel("Codec:"), 3, 0)
        self.codec_combo = QComboBox()
        self.codec_combo.addItems(list(CODEC_OPTIONS.keys()))
        output_layout.addWidget(self.codec_combo, 3, 1, 1, 2)
        
        # Bitrate
        output_layout.addWidget(QLabel("Bitrate:"), 4, 0)
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(list(BITRATE_PRESETS.keys()))
        self.bitrate_combo.setCurrentText('Medium (1000k)')
        output_layout.addWidget(self.bitrate_combo, 4, 1, 1, 2)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.convert_btn = QPushButton("Convert Video")
        self.convert_btn.clicked.connect(self.start_single_conversion)
        self.convert_btn.setStyleSheet("QPushButton { font-size: 16px; padding: 12px 24px; }")
        
        control_layout.addStretch()
        control_layout.addWidget(self.convert_btn)
        control_layout.addStretch()
        
        layout.addWidget(input_group)
        layout.addWidget(output_group)
        layout.addLayout(control_layout)
        layout.addStretch()
        
        # Set default output directory to user's home
        self.output_dir_edit.setText(os.path.expanduser("~"))
        
        return tab
    
    def create_batch_conversion_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # File list section
        files_group = QGroupBox("Video Files")
        files_layout = QVBoxLayout(files_group)
        
        file_controls = QHBoxLayout()
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.add_batch_files)
        self.remove_files_btn = QPushButton("Remove Selected")
        self.remove_files_btn.clicked.connect(self.remove_batch_files)
        self.clear_files_btn = QPushButton("Clear All")
        self.clear_files_btn.clicked.connect(self.clear_batch_files)
        
        file_controls.addWidget(self.add_files_btn)
        file_controls.addWidget(self.remove_files_btn)
        file_controls.addWidget(self.clear_files_btn)
        file_controls.addStretch()
        
        self.batch_file_list = QListWidget()
        
        files_layout.addLayout(file_controls)
        files_layout.addWidget(self.batch_file_list)
        
        # Batch settings (reuse single conversion settings)
        batch_settings_group = QGroupBox("Batch Settings")
        batch_settings_layout = QGridLayout(batch_settings_group)
        
        # Output directory for batch
        batch_settings_layout.addWidget(QLabel("Output Directory:"), 0, 0)
        self.batch_output_dir_edit = QLineEdit()
        self.batch_output_dir_edit.setText(os.path.expanduser("~"))
        self.batch_browse_output_btn = QPushButton("Browse")
        self.batch_browse_output_btn.clicked.connect(self.browse_batch_output_dir)
        batch_settings_layout.addWidget(self.batch_output_dir_edit, 0, 1)
        batch_settings_layout.addWidget(self.batch_browse_output_btn, 0, 2)
        
        # Batch control
        batch_control_layout = QHBoxLayout()
        self.batch_convert_btn = QPushButton("Convert All Files")
        self.batch_convert_btn.clicked.connect(self.start_batch_conversion)
        self.batch_convert_btn.setStyleSheet("QPushButton { font-size: 16px; padding: 12px 24px; }")
        
        batch_control_layout.addStretch()
        batch_control_layout.addWidget(self.batch_convert_btn)
        batch_control_layout.addStretch()
        
        layout.addWidget(files_group)
        layout.addWidget(batch_settings_group)
        layout.addLayout(batch_control_layout)
        
        return tab
    
    def create_presets_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Presets list
        presets_group = QGroupBox("Conversion Presets")
        presets_layout = QVBoxLayout(presets_group)
        
        self.presets_list = QListWidget()
        self.presets_list.addItems(get_preset_names())
        self.presets_list.currentItemChanged.connect(self.on_preset_selected)
        
        self.apply_preset_btn = QPushButton("Apply Preset to Single Conversion")
        self.apply_preset_btn.clicked.connect(self.apply_preset)
        
        presets_layout.addWidget(self.presets_list)
        presets_layout.addWidget(self.apply_preset_btn)
        
        # Preset details
        details_group = QGroupBox("Preset Details")
        details_layout = QVBoxLayout(details_group)
        
        self.preset_details = QTextEdit()
        self.preset_details.setReadOnly(True)
        self.preset_details.setMaximumHeight(200)
        
        details_layout.addWidget(self.preset_details)
        
        layout.addWidget(presets_group)
        layout.addWidget(details_group)
        
        return tab
    
    def create_progress_section(self, main_layout):
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Log area
        log_group = QGroupBox("Conversion Log")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(log_group)
        
    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input Video", "", 
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v)"
        )
        if file_path:
            self.input_path_edit.setText(file_path)
            
    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_edit.setText(dir_path)
            
    def start_conversion(self):
        input_path = self.input_path_edit.text().strip()
        output_dir = self.output_dir_edit.text().strip()
        
        # Validation
        if not input_path:
            QMessageBox.warning(self, "Warning", "Please select an input video file.")
            return
            
        if not output_dir:
            QMessageBox.warning(self, "Warning", "Please select an output directory.")
            return
            
        if not is_valid_video_file(input_path, SUPPORTED_INPUT_FORMATS):
            QMessageBox.warning(self, "Warning", "Invalid input video file.")
            return
            
        if not os.path.isdir(output_dir):
            QMessageBox.warning(self, "Warning", "Invalid output directory.")
            return
        
        # Get settings
        output_format = self.format_combo.currentText()
        resolution_key = self.resolution_combo.currentText()
        resolution = RESOLUTION_PRESETS[resolution_key]
        codec_key = self.codec_combo.currentText()
        codec = CODEC_OPTIONS[codec_key]
        bitrate_key = self.bitrate_combo.currentText()
        bitrate = BITRATE_PRESETS[bitrate_key]
        
        # Generate output path
        output_path = get_output_filepath(input_path, output_dir, output_format)
        
        # Start conversion in separate thread
        self.conversion_thread = ConversionThread(
            input_path, output_path, resolution, bitrate, codec
        )
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.conversion_complete.connect(self.conversion_finished)
        
        # Update UI
        self.convert_btn.setEnabled(False)
        self.convert_btn.setText("Converting...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.log_text.clear()
        
        self.conversion_thread.start()
        
    def update_progress(self, message):
        self.log_text.append(message)
        
    def conversion_finished(self, success, message):
        self.convert_btn.setEnabled(True)
        self.convert_btn.setText("Convert Video")
        self.progress_bar.setVisible(False)
        
        if success:
            self.log_text.append(f"✓ {message}")
            QMessageBox.information(self, "Success", "Video conversion completed successfully!")
        else:
            self.log_text.append(f"✗ {message}")
            QMessageBox.critical(self, "Error", f"Conversion failed: {message}")

def main():
    app = QApplication(sys.argv)
    window = VideoConverterGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


        
    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input Video", "", 
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v)"
        )
        if file_path:
            self.input_path_edit.setText(file_path)
            
    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def browse_batch_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Batch Output Directory")
        if dir_path:
            self.batch_output_dir_edit.setText(dir_path)
    
    def add_batch_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Video Files", "", 
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v)"
        )
        for file_path in file_paths:
            self.batch_file_list.addItem(file_path)
    
    def remove_batch_files(self):
        current_row = self.batch_file_list.currentRow()
        if current_row >= 0:
            self.batch_file_list.takeItem(current_row)
    
    def clear_batch_files(self):
        self.batch_file_list.clear()
    
    def on_preset_selected(self, current, previous):
        if current:
            preset_name = current.text()
            preset_settings = get_preset_settings(preset_name)
            description = get_preset_description(preset_name)
            
            if preset_settings:
                details = f"Preset: {preset_name}\n\n"
                details += f"Description: {description}\n\n"
                details += f"Format: {preset_settings['format']}\n"
                details += f"Codec: {preset_settings['codec']}\n"
                details += f"Resolution: {preset_settings['resolution'] or 'Original'}\n"
                details += f"Bitrate: {preset_settings['bitrate']}\n"
                
                self.preset_details.setText(details)
    
    def apply_preset(self):
        current_item = self.presets_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a preset first.")
            return
        
        preset_name = current_item.text()
        preset_settings = get_preset_settings(preset_name)
        
        if preset_settings:
            # Apply to single conversion tab
            self.format_combo.setCurrentText(preset_settings['format'])
            
            # Find and set resolution
            resolution = preset_settings['resolution']
            if resolution:
                for key, value in RESOLUTION_PRESETS.items():
                    if value == resolution:
                        self.resolution_combo.setCurrentText(key)
                        break
            else:
                self.resolution_combo.setCurrentText('Original')
            
            # Find and set codec
            codec = preset_settings['codec']
            for key, value in CODEC_OPTIONS.items():
                if value == codec:
                    self.codec_combo.setCurrentText(key)
                    break
            
            # Find and set bitrate
            bitrate = preset_settings['bitrate']
            for key, value in BITRATE_PRESETS.items():
                if value == bitrate:
                    self.bitrate_combo.setCurrentText(key)
                    break
            
            # Switch to single conversion tab
            self.tab_widget.setCurrentIndex(0)
            
            QMessageBox.information(self, "Success", f"Applied preset: {preset_name}")
            
    def start_single_conversion(self):
        input_path = self.input_path_edit.text().strip()
        output_dir = self.output_dir_edit.text().strip()
        
        # Validation
        if not input_path:
            QMessageBox.warning(self, "Warning", "Please select an input video file.")
            return
            
        if not output_dir:
            QMessageBox.warning(self, "Warning", "Please select an output directory.")
            return
            
        if not is_valid_video_file(input_path, SUPPORTED_INPUT_FORMATS):
            QMessageBox.warning(self, "Warning", "Invalid input video file.")
            return
            
        if not os.path.isdir(output_dir):
            QMessageBox.warning(self, "Warning", "Invalid output directory.")
            return
        
        # Get settings
        settings = self.get_conversion_settings()
        
        # Start conversion
        self.start_conversion([input_path], output_dir, settings, batch_mode=False)
    
    def start_batch_conversion(self):
        if self.batch_file_list.count() == 0:
            QMessageBox.warning(self, "Warning", "Please add video files to convert.")
            return
        
        output_dir = self.batch_output_dir_edit.text().strip()
        if not output_dir or not os.path.isdir(output_dir):
            QMessageBox.warning(self, "Warning", "Please select a valid output directory.")
            return
        
        # Get file list
        file_paths = []
        for i in range(self.batch_file_list.count()):
            file_paths.append(self.batch_file_list.item(i).text())
        
        # Get settings from single conversion tab
        settings = self.get_conversion_settings()
        
        # Start batch conversion
        self.start_conversion(file_paths, output_dir, settings, batch_mode=True)
    
    def get_conversion_settings(self):
        output_format = self.format_combo.currentText()
        resolution_key = self.resolution_combo.currentText()
        resolution = RESOLUTION_PRESETS[resolution_key]
        codec_key = self.codec_combo.currentText()
        codec = CODEC_OPTIONS[codec_key]
        bitrate_key = self.bitrate_combo.currentText()
        bitrate = BITRATE_PRESETS[bitrate_key]
        
        return {
            'format': output_format,
            'resolution': resolution,
            'codec': codec,
            'bitrate': bitrate
        }
    
    def start_conversion(self, input_paths, output_dir, settings, batch_mode=False):
        # Start conversion in separate thread
        self.conversion_thread = ConversionThread(
            input_paths, output_dir, settings, batch_mode
        )
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.conversion_complete.connect(self.conversion_finished)
        self.conversion_thread.progress_percentage.connect(self.update_progress_bar)
        
        # Update UI
        self.convert_btn.setEnabled(False)
        self.batch_convert_btn.setEnabled(False)
        self.convert_btn.setText("Converting...")
        self.batch_convert_btn.setText("Converting...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        self.conversion_thread.start()
        
    def update_progress(self, message):
        self.log_text.append(message)
        
    def update_progress_bar(self, percentage):
        self.progress_bar.setValue(percentage)
        
    def conversion_finished(self, success, message):
        self.convert_btn.setEnabled(True)
        self.batch_convert_btn.setEnabled(True)
        self.convert_btn.setText("Convert Video")
        self.batch_convert_btn.setText("Convert All Files")
        self.progress_bar.setVisible(False)
        
        if success:
            self.log_text.append(f"✓ {message}")
            QMessageBox.information(self, "Success", "Video conversion completed successfully!")
        else:
            self.log_text.append(f"✗ {message}")
            QMessageBox.critical(self, "Error", f"Conversion failed: {message}")

def main():
    app = QApplication(sys.argv)
    window = VideoConverterGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

