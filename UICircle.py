from PyQt5.QtWidgets import QWidget, QLabel


class UICircle(QWidget):
    def __init__(self, parent=None, style=None):
        super(UICircle, self).__init__(parent)

        if style is None:
            style = "border: 3px solid blue; border-radius: 10px;"

        self.circle = QLabel(self)
        self.circle.resize(20, 20)
        self.circle.setStyleSheet(style)