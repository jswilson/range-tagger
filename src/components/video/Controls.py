from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QBoxLayout, QSlider, QPushButton, QSizePolicy, QLabel)
from PyQt5.QtCore import (Qt, QFile)
from PyQt5.QtWidgets import QStyle
from PyQt5.QtGui import QIntValidator

from ...registry import Registry
from .FrameLineEdit import FrameLineEdit
from ...util import format_frames_to_hms
class Controls(QFrame):
    def __init__(self, store, pause_cb, next_cb, prev_cb, seek_cb, frames_to_jump_cb, jump_back_cb, jump_forward_cb):
        QFrame.__init__(self)
        self.store = store
        self.pause_cb = pause_cb
        self.next_cb = next_cb
        self.prev_cb = prev_cb
        self.seek_cb = seek_cb
        self.frames_to_jump_cb = frames_to_jump_cb
        self.jump_back_cb = jump_back_cb
        self.jump_forward_cb = jump_forward_cb
        self._paused = True

        self.store.video_frame_number_changed.connect(self._video_frame_number_changed)

        self._init_ui()

    def _video_frame_number_changed(self, frame_number):
        self.slider.blockSignals(True)

        self._update_slider(frame_number)
        self._update_times(frame_number)
        self._update_frames(frame_number)

        self.slider.blockSignals(False)

    def _jump_back_clicked(self):
        self.jump_back_cb()

    def _jump_forward_clicked(self):
        self.jump_forward_cb()

    def _on_frames_to_jump_change(self, text):
        try:
            int(text)
        except ValueError:
            return

        self.frames_to_jump_cb(int(text))

    def _next_clicked(self):
        self.next_cb()

    def _prev_clicked(self):
        self.prev_cb()

    def _slider_changed(self):
        self.seek_cb(self.slider.value())

    def _update_slider(self, frame_number):
        self.slider.setValue(float(frame_number) / self.store.video_total_frames * 16384)

    def _update_times(self, frame_number):
        self.time_start_label.setText(format_frames_to_hms(frame_number))
        self.time_end_label.setText(format_frames_to_hms(self.store.video_total_frames))

    def _update_frames(self, frame_number):
        self.frame_start_label.setText(str(frame_number))
        self.frame_end_label.setText(str(self.store.video_total_frames-1))

    def _init_ui(self):
        self.layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.left_controls_layout = QVBoxLayout()
        self.left_controls_layout.setContentsMargins(0,0,0,0)

        self.play_controls_frame = QFrame()
        self.play_controls_layout = QHBoxLayout()
        self.play_controls_layout.setContentsMargins(0,0,0,0)
        self.play_controls_frame.setLayout(self.play_controls_layout)

        self.custom_controls_layout = QHBoxLayout()
        self.custom_controls_frame = QFrame()
        self.custom_controls_layout.setContentsMargins(0,0,0,0)
        self.custom_controls_frame.setLayout(self.custom_controls_layout)
        self.left_controls_layout.addWidget(self.play_controls_frame)
        self.left_controls_layout.addWidget(self.custom_controls_frame)
        self.custom_controls_layout.setAlignment(Qt.AlignCenter)

        self.right_slider_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(16384)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(1)
        self.right_slider_layout.setContentsMargins(0,0,0,0)
        self.label_layout = QHBoxLayout()
        self.time_start_label = QLabel("")
        self.time_end_label = QLabel("")
        self.label_layout.addWidget(self.time_start_label)
        self.label_layout.addWidget(self.time_end_label)
        self.label_layout.setContentsMargins(0,0,0,0)
        self.time_start_label.setContentsMargins(0,0,0,0)
        self.time_start_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.time_end_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.time_end_label.setContentsMargins(0,0,0,0)
        self.right_slider_layout.addWidget(self.slider)
        self.right_slider_layout.addLayout(self.label_layout)

        self.frame_label_layout = QHBoxLayout()
        self.frame_start_label = QLabel("")
        self.frame_end_label = QLabel("")
        self.frame_start_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.frame_end_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.frame_label_layout.addWidget(self.frame_start_label)
        self.frame_label_layout.addWidget(self.frame_end_label)
        self.right_slider_layout.addLayout(self.frame_label_layout)

        self.prev = QPushButton()
        self.prev.setMaximumWidth(75)
        self.prev.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))

        self.next = QPushButton()
        self.next.setMaximumWidth(75)
        self.next.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))

        self.custom_back = QPushButton()
        self.custom_back.setMaximumWidth(75)
        self.custom_back.setContentsMargins(0,0,0,0)
        self.custom_back.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))

        self.custom_frames = FrameLineEdit()
        self.custom_frames.setMaximumWidth(50)
        self.custom_frames.setMinimumWidth(50)
        self.custom_frames.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.custom_frames.setContentsMargins(0,0,0,0)
        self.custom_frames.setText(str(self.store.frames_to_jump))
        self.custom_frames.setAlignment(Qt.AlignCenter)
        self.custom_frames.setValidator(QIntValidator(0, 999, self))
        self.custom_frames.textChanged.connect(self._on_frames_to_jump_change)
        self.custom_frames.focusOutEvent
        self.custom_frames_container = QFrame()
        self.custom_frames_container_layout = QVBoxLayout()
        self.custom_frames_container_layout.addWidget(self.custom_frames)
        self.custom_frames_container_layout.setContentsMargins(0,0,0,0)
        self.custom_frames_container.setLayout(self.custom_frames_container_layout)

        self.custom_fwd = QPushButton()
        self.custom_fwd.setMaximumWidth(75)
        self.custom_fwd.setContentsMargins(0,0,0,0)
        self.custom_fwd.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))

        self.custom_controls_layout.addStretch()
        self.custom_controls_layout.addWidget(self.custom_back)
        self.custom_controls_layout.addWidget(self.custom_frames_container)
        self.custom_controls_layout.addWidget(self.custom_fwd)
        self.custom_controls_layout.addStretch()

        self.play_controls_layout.addStretch()
        self.play_controls_layout.addWidget(self.prev)
        self.play_controls_layout.addWidget(self.next)
        self.play_controls_layout.addStretch()
        self.layout.addLayout(self.left_controls_layout, 1)
        self.layout.addLayout(self.right_slider_layout, 4)

        self.setLayout(self.layout)

        self.next.clicked.connect(self._next_clicked)
        self.prev.clicked.connect(self._prev_clicked)
        self.slider.valueChanged.connect(self._slider_changed)
        self.custom_back.clicked.connect(self._jump_back_clicked)
        self.custom_fwd.clicked.connect(self._jump_forward_clicked)

        self._init_style()

    def _init_style(self):
        file = QFile(Registry.CONTROLS_QSS);
        file.open(QFile.ReadOnly);
        styleSheet = file.readAll().data();
        self.setStyleSheet(styleSheet.decode("utf-8"));