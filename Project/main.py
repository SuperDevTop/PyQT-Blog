from PyQt5.QtWidgets import QApplication
from design import Design

app = QApplication([])
window = Design()
window.show()
app.exec()
