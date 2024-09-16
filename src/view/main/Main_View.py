import os
import numpy as np
import wave
import sounddevice as sd
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QTimer, Signal, QUrl, Slot
from PySide6.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QInputDialog, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from util.Theme_Util import ThemeUtil
from common.const.Global_Const import Global_Const
from Module import Module
from view.layout.Toolbar_View import Toolbar_View
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class RecordingItem(QWidget):
    delete_requested = Signal(str)

    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)  # Create QAudioOutput object
        self.player.setAudioOutput(self.audio_output)  # Set audio output for the player
        self.audio_output.setVolume(1.0)  # Set volume (0.0 to 1.0 scale)

        # Set the media source for playback
        file_url = QUrl.fromLocalFile(os.path.join("src", "asset", "output", filename))
        self.player.setSource(file_url)

        self.is_playing = False
        self.init_ui()

        # Connect QMediaPlayer's positionChanged signal to update the playback time
        self.player.positionChanged.connect(self.update_playback_time)
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)

        details_layout = QVBoxLayout()

        # Strip the .wav extension from the filename
        name_without_extension = os.path.splitext(self.filename)[0]

        name = QLabel(name_without_extension)
        name.setStyleSheet("font-size: 16px; font-weight: bold; color: #fff; padding: 5px; background-color: #333; border-radius: 8px;")
        name.setWordWrap(True)
        name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        name.setMinimumHeight(30)
        details_layout.addWidget(name)

        self.duration = QLabel(" Duration: 00:00 / 00:00")
        self.duration.setStyleSheet("font-size: 14px; color: #ccc;")
        self.duration.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.duration.setMinimumHeight(30)
        details_layout.addWidget(self.duration)

        layout.addLayout(details_layout)
        layout.addStretch()

        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(QIcon('src/asset/image/play'))  # Change to a play icon
        self.play_pause_button.setStyleSheet(""" 
    QPushButton {
        background-color: transparent;
        border: none;
        color: #fff;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
    }
    """)

        self.play_pause_button.setFixedSize(24, 24)
        self.play_pause_button.clicked.connect(self.toggle_playback)
        layout.addWidget(self.play_pause_button)

        self.reset_button = QPushButton()
        self.reset_button.setIcon(QIcon('src/asset/image/restart'))  # Add a reset icon
        self.reset_button.setStyleSheet(""" 
    QPushButton {
        background-color: transparent;
        border: none;
        color: #3498db;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: rgba(52, 152, 219, 0.2);
        border-radius: 12px;
    }
    """)

        self.reset_button.setFixedSize(24, 24)
        self.reset_button.clicked.connect(self.reset_playback)
        layout.addWidget(self.reset_button)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon('src/asset/image/delete'))
        delete_button.setStyleSheet(""" 
    QPushButton {
        background-color: transparent;
        border: none;
        color: #ff6b6b;
        padding: 5px;
    }
    QPushButton:hover {
        color: #ff4444;
        background-color: rgba(255, 107, 107, 0.2);
        border-radius: 12px;
    }
    """)

        delete_button.setFixedSize(24, 24)
        delete_button.clicked.connect(self.delete_confirmation)
        layout.addWidget(delete_button)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
            
    @Slot()
    def toggle_playback(self):
        """Toggle playback state between play and pause."""
        if self.player.mediaStatus() == QMediaPlayer.NoMedia:
            print("No media loaded")
            return

        # Handle play and pause toggle based on media player state
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_pause_button.setIcon(QIcon('src/asset/image/play'))  # Change to a play icon
        else:
            self.player.play()
            self.play_pause_button.setIcon(QIcon('src/asset/image/pause'))  # Change to a pause icon

    @Slot()
    def reset_playback(self):
        """Reset the playback position to the beginning and stop playback."""
        self.player.setPosition(0)
        self.player.pause()  # Ensure the player is paused
        self.play_pause_button.setIcon(QIcon('src/asset/image/play'))  # Ensure the icon shows play
        self.is_playing = False

    @Slot()
    def delete_confirmation(self):
        """Show a confirmation dialog before deleting the recording."""
        reply = QMessageBox.question(self, 'Delete Recording', f"Are you sure you want to delete {self.filename}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Emit signal to request deletion
            self.delete_requested.emit(self.filename)

    @Slot(int)
    def update_playback_time(self, position):
        """Update the playback time label with the current position."""
        duration = self.player.duration()
        if duration < 0:  # Handle invalid duration
            duration = 0
        position_text = self.format_time(position)
        duration_text = self.format_time(duration)
        self.duration.setText(f" Duration: {position_text} / {duration_text}")

    def format_time(self, milliseconds):
        """Format milliseconds into MM:SS format."""
        seconds = milliseconds / 1000
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02}:{seconds:02}"

class MainView(QtWidgets.QWidget):
    def __init__(self, login_window):
        super().__init__()

        ThemeUtil.get(parent=self, name_file=Global_Const.Theme.CORE_THEME)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = Toolbar_View(login_window)
        layout.addWidget(toolbar.main())

        for i in Module.widgets:
            layout.addWidget(i())

        self.create_home_view()

        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.stacked_widget.addWidget(self.home_view)
        layout.addWidget(self.stacked_widget)

        self.is_recording = False
        self.fs = 44100
        self.frames = []
        self.duration_timer = QTimer(self)
        self.duration_timer.timeout.connect(self.update_timer)
        self.record_seconds = 0

        self.recordings = []

        self.load_recordings()

    def create_home_view(self):
        """Create the home view."""
        self.home_view = QtWidgets.QWidget()
        home_layout = QtWidgets.QVBoxLayout(self.home_view)
        home_layout.setAlignment(QtCore.Qt.AlignCenter)
        home_layout.setContentsMargins(20, 20, 20, 20)

        self.status_label = QtWidgets.QLabel("Status: Not Recording")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet(""" 
            font-size: 18px;
            color: #fff;
            background-color: #444;
            padding: 15px;
            border-radius: 10px;
        """)
        home_layout.addWidget(self.status_label)

        self.timer_label = QtWidgets.QLabel("00:00")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 32px; color: #fff; margin-bottom: 20px;")
        home_layout.addWidget(self.timer_label)

        button_layout = QtWidgets.QHBoxLayout()  # Change to QHBoxLayout for horizontal arrangement
        button_layout.setSpacing(20)
        button_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.record_button = QtWidgets.QPushButton("Record")
        self.record_button.setStyleSheet(""" 
    QPushButton {
        background-color: #e74c3c;
        color: white;
        font-size: 16px;  /* Smaller font size */
        padding: 10px 20px;  /* Adjust padding for a sleeker look */
        border-radius: 10px;  /* Smooth rounded corners */
        border: 2px solid #c0392b;  /* Add a border for a clean look */
    }
    QPushButton:hover {
        background-color: #c0392b;  /* Darker red on hover */
        border-color: #e74c3c;  /* Swap border colors on hover */
    }
    """)
        self.record_button.clicked.connect(self.record_audio)
        button_layout.addWidget(self.record_button)

        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setStyleSheet(""" 
    QPushButton {
        background-color: #555;
        color: #ccc;
        font-size: 16px;  /* Smaller font size */
        padding: 10px 20px;  /* Adjust padding */
        border-radius: 10px;  /* Smooth rounded corners */
        border: 2px solid #444;  /* Subtle border */
    }
    QPushButton:hover {
        background-color: #444;  /* Darker gray on hover */
        border-color: #555;  /* Swap border colors on hover */
    }
    QPushButton:disabled {
        background-color: #777;  /* Grayed-out when disabled */
        color: #999;
        border-color: #666;
    }
    """)
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_recording)
        button_layout.addWidget(self.stop_button)

        home_layout.addLayout(button_layout)  # Add buttons layout directly to the main layout

        self.recordings_list = QtWidgets.QListWidget()
        self.recordings_list.setStyleSheet(""" 
            QListWidget {
                background-color: #333;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 10px;
            }
        """)
        self.recordings_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Make sure it can expand

        home_layout.addStretch()

        home_layout.addWidget(self.recordings_list)

        self.recordings_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.recordings_list.customContextMenuRequested.connect(self.show_context_menu)


    def show_context_menu(self, pos):
        """Show context menu for recordings list."""
        item = self.recordings_list.itemAt(pos)
        if item:
            context_menu = QMenu(self)
            play_action = QAction("Play", self)
            delete_action = QAction("Delete", self)
            context_menu.addAction(play_action)
            context_menu.addAction(delete_action)

            play_action.triggered.connect(lambda: self.play_recording(item.text()))
            delete_action.triggered.connect(lambda: self.delete_recording(item.text()))

            context_menu.exec(self.recordings_list.viewport().mapToGlobal(pos))

    def play_recording(self, filename):
        """Play a selected recording."""
        # Currently handled in RecordingItem
        pass

    def delete_recording(self, filename):
        """Delete a selected recording."""
        # First, stop any playback associated with the file
        for i in range(self.recordings_list.count()):
            item_widget = self.recordings_list.itemWidget(self.recordings_list.item(i))
            if item_widget and item_widget.filename == filename:
                item_widget.player.stop()  # Stop the media player
                item_widget.player.setSource(QUrl())  # Clear the source to release the file

        file_path = os.path.join("src", "asset", "output", filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)  # Now, safely remove the file
                self.recordings.remove(filename)
                self.refresh_recordings_list()
                QtWidgets.QMessageBox.information(self, "Deleted", f"{filename} has been deleted.")
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, "Error", f"Cannot delete {filename}. The file is being used by another process.")

    def switch_to_home(self):
        """Switch to home view and refresh recordings list."""
        self.refresh_recordings_list()
        self.stacked_widget.setCurrentWidget(self.home_view)

    def record_audio(self):
        """Start recording audio."""
        if not self.is_recording:
            self.is_recording = True
            self.frames = []
            self.record_seconds = 0
            self.status_label.setText("Status: Recording...")
            self.record_button.setDisabled(True)
            self.stop_button.setDisabled(False)
            self.duration_timer.start(1000)

            self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs)
            self.stream.start()

    def stop_recording(self):
        """Stop the audio recording and save to a file."""
        if self.is_recording:
            self.is_recording = False
            self.status_label.setText("Status: Not Recording")
            self.record_button.setDisabled(False)
            self.stop_button.setDisabled(True)
            self.duration_timer.stop()

            self.stream.stop()
            self.stream.close()

            # Prompt the user for a filename
            filename = self.prompt_for_filename()
            if filename:
                file_path = os.path.join("src", "asset", "output", filename)

                # Save the recording to the specified file
                self.save_wav(file_path)
                
                # Add the new recording to the list
                self.recordings.append(filename)
                self.refresh_recordings_list()
                QtWidgets.QMessageBox.information(self, "Saved", f"Recording has been saved as {filename}.")

    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio recording."""
        if status:
            print(status, flush=True)
        self.frames.append(indata.copy())

    def save_wav(self, filename):
        """Save recorded audio to a WAV file."""
        output_dir = os.path.dirname(filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            # Concatenate frames into a single array
            audio_data = np.concatenate(self.frames)
            
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.fs)
                wf.writeframes(audio_data.tobytes())
        except IOError as e:
            QtWidgets.QMessageBox.warning(self, "File Error", f"Failed to save recording: {e}")

    def prompt_for_filename(self):
        """Prompt the user to input a filename for the new recording."""
        filename, ok = QInputDialog.getText(self, 'Enter Filename', 'Enter the name for the new recording (without extension):')
        if ok and filename:
            # Ensure filename ends with '.wav'
            if not filename.endswith('.wav'):
                filename += '.wav'
            return filename
        return None

    def update_timer(self):
        """Update the recording timer."""
        self.record_seconds += 1
        minutes, seconds = divmod(self.record_seconds, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def load_recordings(self):
        """Load the list of existing recordings from the directory."""
        output_dir = os.path.join("src", "asset", "output")
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                if filename.endswith(".wav"):
                    self.recordings.append(filename)
        self.refresh_recordings_list()

    def refresh_recordings_list(self):
        """Refresh the list of recordings."""
        self.recordings_list.clear()
        for filename in self.recordings:
            item = QListWidgetItem()
            widget = RecordingItem(filename, parent=self)
            widget.delete_requested.connect(self.delete_recording)  # Connect signal here
            item.setSizeHint(widget.sizeHint())
            self.recordings_list.addItem(item)
            self.recordings_list.setItemWidget(item, widget)

        # Set fixed height of QListWidget to 400
        self.recordings_list.setFixedHeight(400)

