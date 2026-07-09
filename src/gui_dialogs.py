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


from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QDialogButtonBox, QLabel, QAbstractItemView, QDoubleSpinBox, QSpinBox
)
from PySide6.QtCore import Qt


class ProfileSelectionDialog(QDialog):

    def __init__(self, parent, title: str, profiles: list, all_checked: bool = True):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.selected_profile = []

        layout = QVBoxLayout(self)
        # лист чекбокс
        self.list_widget = QListWidget()
        for profile in profiles:
            item = QListWidgetItem(profile)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            if all_checked:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)

        # кнопки
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        # Собираем выбранные профили
        self.selected_profile = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                self.selected_profile.append(item.text())
        super().accept()


class FiltersSelectionDialogs(QDialog):
    def __init__(self, parent, title: str, h_filters: list, f_filters: list, selected_filters: tuple):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.selected_filters = ['', '']
        layout = QVBoxLayout(self)

        hankel_layout = QVBoxLayout()
        hankel_label = QLabel('Hankel Filters:')
        self.hankel_list = QListWidget()
        self.hankel_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.hankel_list.addItems(h_filters)
        ind_h = h_filters.index(selected_filters[0])
        self.hankel_list.setCurrentRow(ind_h)

        hankel_layout.addWidget(hankel_label)
        hankel_layout.addWidget(self.hankel_list)

        fourier_layout = QVBoxLayout()
        fourier_label = QLabel('Fourier Filters:')
        self.fourier_list = QListWidget()
        self.fourier_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.fourier_list.addItems(f_filters)
        ind_f = f_filters.index(selected_filters[1])
        self.fourier_list.setCurrentRow(ind_f)

        fourier_layout.addWidget(fourier_label)
        fourier_layout.addWidget(self.fourier_list)

        columns_layout = QHBoxLayout()
        columns_layout.addLayout(hankel_layout)
        columns_layout.addLayout(fourier_layout)
        layout.addLayout(columns_layout)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        self.selected_filters = ['', '']
        h = self.hankel_list.currentItem().text()
        f = self.fourier_list.currentItem().text()
        self.selected_filters = [h, f]

        super().accept()


class InputDoubleDialog(QDialog):

    double_value: float

    def __init__(self, parent, title: str, default_value: float = 0.010):
        super().__init__(parent)
        # self.alpha_coefficient = default_value

        self.setWindowTitle(title)

        layout = QVBoxLayout(self)
        # input double
        self.double_input = QDoubleSpinBox()
        self.double_input.setMinimum(0.0)
        self.double_input.setMaximum(1.0)
        self.double_input.setSingleStep(0.001)
        self.double_input.setValue(default_value)
        self.double_input.setDecimals(3)
        self.double_input.setKeyboardTracking(True)

        layout.addWidget(self.double_input)

        # кнопки
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        # Собираем выбранные профили
        self.double_value = self.double_input.value()
        super().accept()


class InputIntegerDialog(QDialog):

    integer_value: int

    def __init__(self, parent, title: str, default_value: int = 0):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        self.integer_input = QSpinBox()
        self.integer_input.setRange(1, 100)
        self.integer_input.setSingleStep(1)
        self.integer_input.setValue(default_value)
        self.integer_input.setKeyboardTracking(True)
        layout.addWidget(self.integer_input)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def accept(self):
        self.integer_value = self.integer_input.value()
        super().accept()




