"""
Класс реализующий UI для настроек симуляции
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from ui import Ui_Form
from quad_tree.configer import ConfigManager
from quad_tree import main_func

import sys


class ModalError(QtWidgets.QDialog):
    def __init__(self, parent=None, error_text="Ошибка!") -> None:
        """
        Класс окошка с ошибкой
        """
        super(ModalError, self).__init__(parent)

        # Создание элементов интерфейса
        super().__init__(parent)
        self.label = QtWidgets.QLabel(error_text)
        self.label.setWordWrap(True)
        self.button = QtWidgets.QPushButton("OK")
        self.button.clicked.connect(self.accept)

        # Расположение элементов интерфейса на форме
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Настройка размеров формы
        self.setWindowTitle("Ошибка!")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        # Делаем окно модальным
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def accept(self) -> None:
        """
        Метод закрытия окна
        """
        self.hide()


class SettingsWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self) -> None:
        """
        Класс для заполнения, выведения и валидации параметров симуляции
        """
        super(SettingsWindow, self).__init__()
        self.setupUi(self)
        self.runPushButton.clicked.connect(self.validate)
        self.confManager = ConfigManager()
        self.confManager.load_from_file()

        self.ballCountSpinBox.setValue(
            self.confManager.config.getint('DEFAULT', 'BALLS_COUNT')
        )
        self.radiusFromSpinBox.setValue(
            self.confManager.config.getint('DEFAULT', 'BALL_MIN_RADIUS')
        )
        self.radiusToSpinbox.setValue(
            self.confManager.config.getint('DEFAULT', 'BALL_MAX_RADIUS')
        )
        self.boundsWidthSpinBox.setValue(
            self.confManager.config.getint('DEFAULT', 'WIDTH')
        )
        self.boundsHeightSpinBox.setValue(
            self.confManager.config.getint('DEFAULT', 'HEIGHT')
        )
        self.velocityFromSpinBox.setValue(
            self.confManager.config.getint('DEFAULT', 'BALL_MIN_VELOCITY')
        )
        self.velocityToSpinBox.setValue(
            self.confManager.config.getint('DEFAULT', 'BALL_MAX_VELOCITY')
        )

        self.runPushButton.setFocus()

    def validate(self) -> None:
        """
        Метод валидации значений
        При прохождении валидации запускает метод запуска симуляции
        """
        error_text = 'Ошибка:\n'
        if self.boundsWidthSpinBox.value() < self.radiusToSpinbox.value():
            error_text += 'Окно не может быть уже чем радиус шара\n'
        if self.boundsHeightSpinBox.value() < self.radiusToSpinbox.value():
            error_text += 'Окно не может быть тоньше чем радиус шара\n'
        if self.radiusFromSpinBox.value() > self.radiusToSpinbox.value():
            error_text += 'Левая граница радиуса больше правой\n'
        if self.velocityFromSpinBox.value() > self.velocityToSpinBox.value():
            error_text += 'Левая граница скорости больше правой\n'

        if error_text != 'Ошибка:\n':
            error_show = ModalError(self, error_text)
            error_show.show()
            return

        self.confManager.update_from_dict(
            {
                'WIDTH': self.boundsWidthSpinBox.value(),
                'HEIGHT': self.boundsHeightSpinBox.value(),
                'BALLS_COUNT': self.ballCountSpinBox.value(),
                'BALL_MIN_RADIUS': self.radiusFromSpinBox.value(),
                'BALL_MAX_RADIUS': self.radiusToSpinbox.value(),
                'BALL_MIN_VELOCITY': self.velocityFromSpinBox.value(),
                'BALL_MAX_VELOCITY': self.velocityToSpinBox.value(),
            }
        )
        self.run()

    def run(self) -> None:
        """
        Метод запуска симуляции, сохраняет конфиги в файл
        """
        self.confManager.set_consts()
        self.confManager.save_to_file()
        self.hide()
        main_func.run()



