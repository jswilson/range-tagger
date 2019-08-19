from PyQt5.QtWidgets import (QPushButton)

class PressableLabel(QPushButton):

    def __init__(self, text, disabled=False, clicked_cb=None):
        QPushButton.__init__(self, text)
        self.text = text
        self.disabled = disabled
        self.clicked_cb = clicked_cb
        self.clicked.connect(self._on_clicked)

        self._set_button_parameters()

    def _on_clicked(self):
        self.clicked_cb(self.text)

    def _set_button_parameters(self):
        self.setFlat(True)
        width = self.fontMetrics().boundingRect(str(self.text)).width() + 10
        self.setMaximumWidth(width)
        self.setDisabled(self.disabled)
