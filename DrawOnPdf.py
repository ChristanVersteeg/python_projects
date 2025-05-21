import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class PDFEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Editor")
        self.setGeometry(100, 100, 800, 600)

        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(0, 0, 800, 600)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()

        self.loadButton = QPushButton("Load PDF", self)
        self.loadButton.clicked.connect(self.load_pdf)
        self.layout.addWidget(self.loadButton)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.doc = None
        self.current_page = None

    def load_pdf(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)", options=options)
        if fileName:
            self.doc = fitz.open(fileName)
            self.current_page = self.doc.load_page(0)
            pix = self.current_page.get_pixmap()
            qimage = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            self.image = QPixmap.fromImage(qimage)
            self.imageLabel.setPixmap(self.image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFEditor()
    window.show()
    sys.exit(app.exec_())

