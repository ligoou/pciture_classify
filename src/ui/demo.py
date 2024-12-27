import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class FolderPathSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Folder Path Selector')
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        title_label = QLabel("Folder Path Selector")
        title_label.setFont(QFont("Arial", 24))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        folder_path_layout = QHBoxLayout()
        self.folder_path_label = QLabel("No folder selected")
        self.folder_path_label.setFont(QFont("Arial", 14))
        folder_path_layout.addWidget(self.folder_path_label)

        select_button = QPushButton("Select Folder")
        select_button.clicked.connect(self.selectFolder)
        select_button.setFont(QFont("Arial", 14))
        select_button.setStyleSheet("background-color: #4CAF50; color: #ffffff;")
        folder_path_layout.addWidget(select_button)

        layout.addLayout(folder_path_layout)

        self.setLayout(layout)

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderPath:
            self.folder_path_label.setText(folderPath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderPathSelector()
    ex.show()
    sys.exit(app.exec_())
