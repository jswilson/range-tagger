import math

from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QFileDialog, QGraphicsView, QGraphicsScene, QMessageBox)
from PyQt5.QtCore import (QFile, Qt)
from PyQt5.QtGui import (QPixmap, QImage)

from ...registry import Registry
from .video_handler import VideoHandler
from .video_handler import CouldNotOpenVideoException
from .Button import Button
from .Controls import Controls

class VideoArea(QFrame):
    def __init__(self, store):
        QFrame.__init__(self)
        self.store = store
        self.video_handler = None
        self.playback_handler = PlaybackHandler(self.store, self.video_handler)

        self.store.video_filename_changed.connect(self._video_filename_changed)
        self.store.video_frame_number_changed.connect(self._video_frame_number_changed)

        self._init_ui()

        self._video_filename_changed(self.store.video_filename)
        self._video_frame_number_changed(self.store.video_current_frame)

    def _video_filename_changed(self, filename):
        if not filename:
            return

        self._show_video_area_and_load_video(filename)

    def _show_video_area_and_load_video(self, filename):
        try:
            self.video_handler = VideoHandler(filename)
            self.playback_handler.set_video_handler(self.video_handler)
        except CouldNotOpenVideoException:
            self.error_message = QMessageBox(QMessageBox.Critical, "Video Open Error", "Could not open video file; has it been renamed or moved?")
            self.error_message.show()
            return

        self.store.set_video_loaded(True)

        self.graphics_view.setVisible(True)
        self.controls.setVisible(True)
        self.button.setVisible(False)
        self.store.set_total_frames(self.video_handler.get_total_frames())
        self.store.set_video_frame(0)

    def _video_frame_number_changed(self, frame_number):
        if frame_number is None or self.video_handler is None:
            return

        frame = self.video_handler.get_frame(frame_number)
        self.graphics_scene.addItem(frame)
        self.graphics_view.fitInView(self.graphics_view.sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.graphics_view.fitInView(self.graphics_view.sceneRect(), Qt.KeepAspectRatio)

    def _handle_open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self,
            Registry.OPEN_VIDEO_DIALOG_TITLE,
            '.',
            Registry.OPEN_VIDEO_DIALOG_FILE_TYPES
        )

        if not filename:
            return

        self.store.set_video_filename(filename)

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.controls = Controls(self.store,
            self.playback_handler._on_pause,
            self.playback_handler._on_next_frame,
            self.playback_handler._on_prev_frame,
            self.playback_handler._on_seek,
            self.playback_handler._on_frames_to_jump_change,
            self.playback_handler._on_jump_back,
            self.playback_handler._on_jump_forward
        )

        self.controls.setVisible(False)
        self.button = Button()
        self.layout.addWidget(self.button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.button.clicked.connect(self._handle_open_file)

        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_scene.setBackgroundBrush(Qt.black);
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setVisible(False)

        self.layout.addWidget(self.graphics_view)
        self.layout.addWidget(self.controls)
        self.layout.setContentsMargins(0,0,0,0)
        self._init_style()

    def _init_style(self):
        file = QFile(Registry.VIDEO_AREA_QSS);
        file.open(QFile.ReadOnly);
        styleSheet = file.readAll().data();
        self.setStyleSheet(styleSheet.decode("utf-8"));


class PlaybackHandler:
    def __init__(self, store, video_handler):
        self.store = store
        self.video_handler = video_handler

    def set_video_handler(self, video_handler):
        self.video_handler = video_handler

    def _on_jump_back(self):
        self.store.set_video_frame(self.store.video_current_frame - self.store.frames_to_jump)

    def _on_jump_forward(self):
        self.store.set_video_frame(self.store.video_current_frame + self.store.frames_to_jump)

    def _on_frames_to_jump_change(self, frames):
        self.store.set_frames_to_jump(frames)

    def _on_next_frame(self):
        self.store.set_video_frame(self.store.video_current_frame + 1)

    def _on_prev_frame(self):
        self.store.set_video_frame(self.store.video_current_frame - 1)

    def _on_pause(self):
        self.timer.cancel()

    def _on_seek(self, value):
        percentage = value / 16384.0
        frame_number = math.floor(percentage * (self.video_handler.get_total_frames() - 1))
        self.store.set_video_frame(frame_number)
