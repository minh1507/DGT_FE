import os
import numpy as np
import wave
import sounddevice as sd
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtWidgets import QListWidgetItem, QMenu, QInputDialog, QSizePolicy
from util.Theme_Util import ThemeUtil
from common.const.Global_Const import Global_Const
from Module import Module
from view.layout.Toolbar_View import Toolbar_View
from ..layout.Recording import RecordingItem

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
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.record_button = QtWidgets.QPushButton("Record")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 10px;
                border: 2px solid #c0392b;
            }
            QPushButton:hover {
                background-color: #c0392b;
                border-color: #e74c3c;
            }
        """)
        self.record_button.clicked.connect(self.record_audio)
        button_layout.addWidget(self.record_button)
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: #ccc;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 10px;
                border: 2px solid #444;
            }
            QPushButton:hover {
                background-color: #444;
                border-color: #555;
            }
            QPushButton:disabled {
                background-color: #777;
                color: #999;
                border-color: #666;
            }
        """)
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_recording)
        button_layout.addWidget(self.stop_button)
        home_layout.addLayout(button_layout)
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
        self.recordings_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        home_layout.addStretch()
        home_layout.addWidget(self.recordings_list)
        self.recordings_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.recordings_list.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
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
        pass

    def delete_recording(self, filename):
        for i in range(self.recordings_list.count()):
            item_widget = self.recordings_list.itemWidget(self.recordings_list.item(i))
            if item_widget and item_widget.filename == filename:
                item_widget.player.stop()
                item_widget.player.setSource(QUrl())
        file_path = os.path.join("src", "asset", "output", filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.recordings.remove(filename)
                self.refresh_recordings_list()
                QtWidgets.QMessageBox.information(self, "Deleted", f"{filename} has been deleted.")
        except PermissionError:
            QtWidgets.QMessageBox.warning(self, "Error", f"Cannot delete {filename}. The file is being used by another process.")

    def switch_to_home(self):
        self.refresh_recordings_list()
        self.stacked_widget.setCurrentWidget(self.home_view)

    def record_audio(self):
        if not self.is_recording:
            self.is_recording = True
            self.frames = []
            self.record_seconds = 0
            self.status_label.setText("Status: Recording...")
            self.record_button.setDisabled(True)
            self.stop_button.setDisabled(False)
            self.duration_timer.start(1000)
            self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=48000, blocksize=2048)
            self.stream.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.status_label.setText("Status: Not Recording")
            self.record_button.setDisabled(False)
            self.stop_button.setDisabled(True)
            self.duration_timer.stop()
            self.stream.stop()
            self.stream.close()
            filename = self.prompt_for_filename()
            if filename:
                file_path = os.path.join("src", "asset", "output", filename)
                self.save_wav(file_path)
                self.recordings.append(filename)
                self.refresh_recordings_list()
                QtWidgets.QMessageBox.information(self, "Saved", f"Recording has been saved as {filename}.")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, flush=True)
        filtered_data = self.apply_filters(indata.copy())
        self.frames.append(filtered_data)

    def apply_filters(self, audio_data):
        return self.apply_nlms_filter(audio_data)

    def apply_nlms_filter(self, audio_data):
        mu = 0.1
        filter_length = 64
        epsilon = 1e-6
        filter_weights = np.zeros(filter_length)
        buffer = np.zeros(filter_length)
        output_data = np.zeros_like(audio_data)
        for i in range(filter_length, len(audio_data)):
            buffer[1:] = buffer[:-1]
            buffer[0] = audio_data[i]
            output = np.dot(filter_weights, buffer)
            output_data[i] = output
            error = audio_data[i] - output
            norm_factor = np.dot(buffer, buffer) + epsilon
            filter_weights += mu * error * buffer / norm_factor
        return output_data

    def save_wav(self, filename):
        output_dir = os.path.dirname(filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        try:
            audio_data = np.concatenate(self.frames)
            audio_data = audio_data / np.max(np.abs(audio_data)) * 32767
            audio_data = audio_data.astype(np.int16)
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(48000)
                wf.writeframes(audio_data.tobytes())
        except IOError as e:
            QtWidgets.QMessageBox.warning(self, "File Error", f"Failed to save recording: {e}")

    def prompt_for_filename(self):
        filename, ok = QInputDialog.getText(self, 'Enter Filename', 'Enter the name for the new recording (without extension):')
        if ok and filename:
            if not filename.endswith('.wav'):
                filename += '.wav'
            return filename
        return None

    def update_timer(self):
        self.record_seconds += 1
        minutes, seconds = divmod(self.record_seconds, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def load_recordings(self):
        output_dir = os.path.join("src", "asset", "output")
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                if filename.endswith(".wav"):
                    self.recordings.append(filename)
        self.refresh_recordings_list()

    def refresh_recordings_list(self):
        self.recordings_list.clear()
        for filename in self.recordings:
            item = QListWidgetItem()
            widget = RecordingItem(filename, parent=self)
            widget.delete_requested.connect(self.delete_recording)
            item.setSizeHint(widget.sizeHint())
            self.recordings_list.addItem(item)
            self.recordings_list.setItemWidget(item, widget)
        self.recordings_list.setFixedHeight(400)
