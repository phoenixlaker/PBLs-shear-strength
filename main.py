# main.py
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QGridLayout, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from cal_test import final_out

class CalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Shear Strength Calculator')
        self.setFixedSize(1000, 1200)
        # background-color: #f0f2f5;
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
            }
            QLabel {
                font-family: 'Microsoft YaHei';
                font-size: 24px;
            }
            QLineEdit {
                font-family: 'Microsoft YaHei';
                font-size: 24px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background: white;
            }
            QPushButton {
                font-family: 'Microsoft YaHei';
                font-size: 24px;
                background-color: #4caf50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)

        self.labels = [
            'Specimen type (ST) \n ("PT":1,"SST":2)',
            'Interfacial condition (IC) \n ("Lubricated":1,"Natural bond":2)',
            'Number of rib holes (n)',
            'Thickness of perforated plate (t) (mm)',
            'Diameter of holes (D) (mm)',
            'Diameter of perforating rebars (d) (mm)',
            'Contact length (hp) (mm)',
            'Height of perforated plate (bp) (mm)',
            'Cylinder compressive strength of concrete (fc) (MPa)',
            'Ultimate strength of steel (fu) (MPa)',
            'Volume content of fibers (V_f) (%)',
            "Average length of fibers (L_f) (mm)",
            "Normalized diameter of fiber (fai_f) (mm)",
            "Concrete type (a) \n (UHPC:1,Normal:0)"
        ]

        # 提供一组默认值
        self.default_values = [
            1,   # ST
            1,   # IC
            1,      # n
            35,     # t
            70,     # D
            16,     # d
            355,    # hp
            300,    # bp
            48.99,  # fc
            577.5,  # fu
            0,      # V_f
            0,      # L_f
            0,      # fai_f
            0,      # a
        ]

        self.inputs = []
        grid = QGridLayout()
        grid.setSpacing(16)

        # 加标题
        self.title_label = QLabel('Shear Strength Prediction of PBLs')
        self.title_label.setFont(QFont('Microsoft YaHei', 30, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.title_label, 0, 0, 1, 2)

        # 输入框从第1行开始
        for i, label_text in enumerate(self.labels):
            label = QLabel(label_text)
            input_field = QLineEdit()
            input_field.setText(str(self.default_values[i]))
            grid.addWidget(label, i + 1, 0)
            grid.addWidget(input_field, i + 1, 1)
            self.inputs.append(input_field)

        # 计算按钮和结果输出再往后排
        self.calc_button = QPushButton('Calculate Shear Strength')
        self.result_label = QLabel('Ultimate Strength (Vu): ')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Microsoft YaHei', 24))

        grid.addWidget(self.calc_button, len(self.labels) + 1, 0, 1, 2)
        grid.addWidget(self.result_label, len(self.labels) + 2, 0, 1, 2)

        self.setLayout(grid)

class CalController:
    def __init__(self, window):
        self.window = window
        self.bindEvents()

    def bindEvents(self):
        self.window.calc_button.clicked.connect(self.calculate)

    def calculate(self):
        try:
            params = [float(input_field.text()) for input_field in self.window.inputs]
            if len(params) != 14:
                raise ValueError('Please fill all fields.')

            ST, IC, n, t, D, d, hp, bp, fc, fu, V_f, L_f, fai_f, a = params
            Vu = final_out(ST, IC, n, t, D, d, hp, bp, fc, fu, V_f, L_f, fai_f, a)
            Vu_value = Vu  # 取第一个结果

            self.window.result_label.setText(f'Shear Strength (Vu): {Vu_value:.2f} kN')
        except Exception as ex:
            QMessageBox.warning(self.window, 'Error', f'Calculation failed: {ex}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CalWindow()
    controller = CalController(win)
    win.show()
    sys.exit(app.exec_())
