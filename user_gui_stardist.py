# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 12:26:11 2024

@author: meher
"""

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QSlider, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

class CellViewer(QMainWindow):
    def __init__(self, npy_file):
        super().__init__()

        # Load the 3D numpy array
        self.volume = np.load(npy_file)
        self.current_slice = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Stardist GUI')

        main_layout = QVBoxLayout()
        self.image_label = QLabel(self)
        main_layout.addWidget(self.image_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.volume.shape[0] - 1)
        self.slider.valueChanged.connect(self.update_slice)
        main_layout.addWidget(self.slider)

        options_layout = QHBoxLayout()
        self.option_a = QRadioButton("Option A")
        self.option_b = QRadioButton("Option B")
        self.option_c = QRadioButton("Option C")
        options_layout.addWidget(self.option_a)
        options_layout.addWidget(self.option_b)
        options_layout.addWidget(self.option_c)
        main_layout.addLayout(options_layout)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_cell)
        main_layout.addWidget(self.next_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.update_slice(0)

    def update_slice(self, value):
        self.current_slice = value
        self.display_slice()

    def display_slice(self):
        slice_image = self.volume[self.current_slice, :, :]

        # Determine the appropriate QImage format based on the dtype of the slice
        if slice_image.dtype == np.uint8:
            qimage_format = QImage.Format_Grayscale8
        elif slice_image.dtype == np.uint16:
            slice_image = slice_image.astype(np.uint8)  # Just for display; keeps original data intact
            qimage_format = QImage.Format_Grayscale8
        else:
            # Scale float or other types to 8-bit just for display
            slice_image = (255 * (slice_image - slice_image.min()) / (slice_image.max() - slice_image.min())).astype(np.uint8)
            qimage_format = QImage.Format_Grayscale8

        height, width = slice_image.shape
        qimage = QImage(slice_image.data, width, height, width, qimage_format)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def next_cell(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    npy_file = 'C:/Users/meher/stardist/segmentation_result.npy'  # Replace with the actual path to your .npy file
    viewer = CellViewer(npy_file)
    viewer.show()
    sys.exit(app.exec_())


#npy_file = 'C:/Users/meher/stardist/segmentation_result100.npy'  