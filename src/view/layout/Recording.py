import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QUrl, Slot
from PySide6.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class RecordingItem(QWidget):
    delete_requested = Signal(str)

    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(1.0)

        file_url = QUrl.fromLocalFile(os.path.join("src", "asset", "output", filename))
        self.player.setSource(file_url)

        self.is_playing = False
        self.init_ui()
        self.player.positionChanged.connect(self.update_playback_time)

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)

        details_layout = QVBoxLayout()

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
        self.play_pause_button.setIcon(QIcon('src/asset/image/play'))
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
        self.reset_button.setIcon(QIcon('src/asset/image/restart'))
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
        if self.player.mediaStatus() == QMediaPlayer.NoMedia:
            return

        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_pause_button.setIcon(QIcon('src/asset/image/play'))
        else:
            self.player.play()
            self.play_pause_button.setIcon(QIcon('src/asset/image/pause'))

    @Slot()
    def reset_playback(self):
        self.player.setPosition(0)
        self.player.pause()
        self.play_pause_button.setIcon(QIcon('src/asset/image/play'))
        self.is_playing = False

    @Slot()
    def delete_confirmation(self):
        reply = QMessageBox.question(self, 'Delete Recording', f"Are you sure you want to delete {self.filename}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_requested.emit(self.filename)

    @Slot(int)
    def update_playback_time(self, position):
        duration = self.player.duration()
        if duration < 0:
            duration = 0
        position_text = self.format_time(position)
        duration_text = self.format_time(duration)
        self.duration.setText(f" Duration: {position_text} / {duration_text}")

    def format_time(self, milliseconds):
        seconds = milliseconds / 1000
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02}:{seconds:02}"

    def get_filename(self):
        return self.filename


def sort_recording_items(recording_items):
    return sorted(recording_items, key=lambda item: os.path.splitext(item.get_filename())[0])
