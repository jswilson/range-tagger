import sys
from PyQt5.QtWidgets import QApplication
from src.VRTWindow import VRTWindow

app = QApplication([])
widget = VRTWindow()
widget.resize(1166, 870)
widget.show()
sys.exit(app.exec_())
