# InverseEmPy1D
# Copyright 2026 Bashkeev Aiur Saianovich by Siberian School of Geoscience (iPolytech)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QCheckBox, QDoubleSpinBox, QPushButton, QGroupBox,
                             QFormLayout)


class CrossSectionSettingsDialog(QDialog):
    """Диалоговое окно для ввода параметров с блокировкой полей по чекбоксам."""

    def __init__(self, parent=None, initial_values=None):
        """
        :param parent:
        :param initial_values:
        checkBoxAutoColorBar - initial_values[0]
        checkBoxAutoAltitude - initial_values[1]
        minValueColorBar - initial_values[2]
        maxValueColorBar - initial_values[3]
        minValueAltitude - initial_values[4]
        maxValueAltitude - initial_values[5]
        checkBoxReverseProfile - initial_values[6]
        checkBoxErrorView - initial_values[7]


        """
        super().__init__(parent)
        self.setWindowTitle('Cross section settings')
        self.setModal(True)

        # Создаём виджеты
        self.checkBoxAutoColorBar = QCheckBox('Auto colorbar')
        self.checkBoxAutoAltitude = QCheckBox('Auto altitude')
        self.checkBoxReverseProfile = QCheckBox('Reverse')
        self.checkBoxErrorView = QCheckBox('Error view')
        self.checkBoxPkLabelView = QCheckBox('PK label view')

        # Поля для ввода чисел (QDoubleSpinBox)
        self.minValueColorBar = QDoubleSpinBox()
        self.maxValueColorBar = QDoubleSpinBox()
        self.minValueAltitude = QDoubleSpinBox()
        self.maxValueAltitude = QDoubleSpinBox()

        # Установим диапазоны для спинбоксов (можно настроить по желанию)
        for spin in (self.minValueColorBar, self.maxValueColorBar):
            spin.setRange(1e-2, 1e6)
            spin.setDecimals(2)  # два знака после запятой

        for spin in (self.minValueAltitude, self.maxValueAltitude):
            spin.setRange(-10000, 10000)  # достаточно большой диапазон
            spin.setDecimals(2)  # два знака после запятой

        # Начальные значения
        self.checkBoxAutoColorBar.setChecked(initial_values[0])
        self.checkBoxAutoAltitude.setChecked(initial_values[1])
        self.minValueColorBar.setValue(initial_values[2])
        self.maxValueColorBar.setValue(initial_values[3])
        self.minValueAltitude.setValue(initial_values[4])
        self.maxValueAltitude.setValue(initial_values[5])
        self.checkBoxReverseProfile.setChecked(initial_values[6])
        self.checkBoxErrorView.setChecked(initial_values[7])
        self.checkBoxPkLabelView.setChecked(initial_values[8])

        # Кнопки
        self.buttonOk = QPushButton('Ok')
        self.buttonCancel = QPushButton('Cancel')

        # Настройка layout
        main_layout = QVBoxLayout(self)

        # Реверс профиля
        main_layout.addWidget(self.checkBoxReverseProfile)
        # Отображение графика ошибок
        main_layout.addWidget(self.checkBoxErrorView)
        # Отображение надписей пикетов
        main_layout.addWidget(self.checkBoxPkLabelView)

        # Группа для цветовой шкалы
        group_color = QGroupBox('Color bar')
        color_layout = QFormLayout(group_color)
        color_layout.addRow(self.checkBoxAutoColorBar, None)  # чекбокс на всю ширину
        color_layout.addRow('Min:', self.minValueColorBar)
        color_layout.addRow('Max:', self.maxValueColorBar)
        main_layout.addWidget(group_color)

        # Группа для высоты
        group_alt = QGroupBox('Altitude (m)')
        alt_layout = QFormLayout(group_alt)
        alt_layout.addRow(self.checkBoxAutoAltitude, None)
        alt_layout.addRow('Min:', self.minValueAltitude)
        alt_layout.addRow('Max:', self.maxValueAltitude)
        main_layout.addWidget(group_alt)

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.buttonOk)
        button_layout.addWidget(self.buttonCancel)
        main_layout.addLayout(button_layout)

        # Подключаем сигналы
        self.checkBoxAutoColorBar.toggled.connect(self._on_auto_color_toggled)
        self.checkBoxAutoAltitude.toggled.connect(self._on_auto_alt_toggled)
        self.buttonOk.clicked.connect(self.accept)
        self.buttonCancel.clicked.connect(self.reject)

        # Устанавливаем начальное состояние блокировки
        self._on_auto_color_toggled(self.checkBoxAutoColorBar.isChecked())
        self._on_auto_alt_toggled(self.checkBoxAutoAltitude.isChecked())

    def _on_auto_color_toggled(self, checked: bool):
        """Блокирует/разблокирует поля min/max цветовой шкалы."""
        self.minValueColorBar.setEnabled(not checked)
        self.maxValueColorBar.setEnabled(not checked)

    def _on_auto_alt_toggled(self, checked: bool):
        """Блокирует/разблокирует поля min/max высоты."""
        self.minValueAltitude.setEnabled(not checked)
        self.maxValueAltitude.setEnabled(not checked)

    def get_values(self):
        """Возвращает кортеж значений"""
        return (
            self.checkBoxAutoColorBar.isChecked(),
            self.checkBoxAutoAltitude.isChecked(),
            self.minValueColorBar.value(),
            self.maxValueColorBar.value(),
            self.minValueAltitude.value(),
            self.maxValueAltitude.value(),
            self.checkBoxReverseProfile.isChecked(),
            self.checkBoxErrorView.isChecked(),
            self.checkBoxPkLabelView.isChecked()
        )

    def accept(self):
        """Принимаем диалог, сохраняем значения."""
        super().accept()


class MapSectionSettingsDialog(QDialog):
    def __init__(self, parent=None, initial_values=None):
        """
        :param parent:
        :param initial_values:
        checkBoxAutoColorBar - initial_values[0]
        checkBoxRelativeDepths - initial_values[1]
        minValueColorBar - initial_values[2]
        maxValueColorBar - initial_values[3]
        checkBoxViewPicketsLabel - initial_values[4]
        """
        super().__init__(parent)
        self.setWindowTitle('Map section settings')
        self.setModal(True)

        # Создаём виджеты
        self.checkBoxAutoColorBar = QCheckBox('Auto colorbar')
        self.checkBoxRelativeDepths = QCheckBox('Relative depths')
        self.checkBoxViewPicketsLabel = QCheckBox('View pickets label')

        # Поля для ввода чисел (QDoubleSpinBox)
        self.minValueColorBar = QDoubleSpinBox()
        self.maxValueColorBar = QDoubleSpinBox()

        # Установим диапазоны для спинбоксов (можно настроить по желанию)
        for spin in (self.minValueColorBar, self.maxValueColorBar):
            spin.setRange(1e-2, 1e6)
            spin.setDecimals(2)  # два знака после запятой

        # Начальные значения
        self.checkBoxAutoColorBar.setChecked(initial_values[0])
        self.checkBoxRelativeDepths.setChecked(initial_values[1])
        self.minValueColorBar.setValue(initial_values[2])
        self.maxValueColorBar.setValue(initial_values[3])
        self.checkBoxViewPicketsLabel.setChecked(initial_values[4])

        # Кнопки
        self.buttonOk = QPushButton('Ok')
        self.buttonCancel = QPushButton('Cancel')

        # Настройка layout
        main_layout = QVBoxLayout(self)

        # Группа для цветовой шкалы
        group_color = QGroupBox('Color bar')
        color_layout = QFormLayout(group_color)
        color_layout.addRow(self.checkBoxAutoColorBar, None)  # чекбокс на всю ширину
        color_layout.addRow('Min:', self.minValueColorBar)
        color_layout.addRow('Max:', self.maxValueColorBar)
        main_layout.addWidget(group_color)

        # относительные или абсолютные высоты
        main_layout.addWidget(self.checkBoxRelativeDepths)

        # включить / отключить надписи пикетов
        main_layout.addWidget(self.checkBoxViewPicketsLabel)

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.buttonOk)
        button_layout.addWidget(self.buttonCancel)
        main_layout.addLayout(button_layout)

        # Подключаем сигналы
        self.checkBoxAutoColorBar.toggled.connect(self._on_auto_color_toggled)
        self.buttonOk.clicked.connect(self.accept)
        self.buttonCancel.clicked.connect(self.reject)

        # Устанавливаем начальное состояние блокировки
        self._on_auto_color_toggled(self.checkBoxAutoColorBar.isChecked())

    def _on_auto_color_toggled(self, checked: bool):
        """Блокирует/разблокирует поля min/max цветовой шкалы."""
        self.minValueColorBar.setEnabled(not checked)
        self.maxValueColorBar.setEnabled(not checked)

    def get_values(self):
        """Возвращает кортеж значений"""
        return (
            self.checkBoxAutoColorBar.isChecked(),
            self.checkBoxRelativeDepths.isChecked(),
            self.minValueColorBar.value(),
            self.maxValueColorBar.value(),
            self.checkBoxViewPicketsLabel.isChecked()
        )

    def accept(self):
        """Принимаем диалог, сохраняем значения."""
        super().accept()
