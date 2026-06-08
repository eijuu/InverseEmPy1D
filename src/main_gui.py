# InverseEmPy1D
# Copyright (C) 2026 Bashkeev Aiur Saianovich by Siberian School of Geoscience (iPolytech)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os.path
import matplotlib
import numpy as np
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import *
from matplotlib import cm, ticker
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure
from matplotlib.ticker import LogLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
import utils
from gui import Ui_MainWindow
from gui_dialogs import *
from settings_dialog import CrossSectionSettingsDialog, MapSectionSettingsDialog
from scipy.interpolate import griddata

BLUE_COLOR = QColor(0, 255, 255)
YELLOW_COLOR = QColor(255, 255, 0)


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ax = None
        matplotlib.rcParams.update({'font.size': 10})
        matplotlib.rcParams.update({'font.family': 'Times New Roman'})

        self.figure = Figure()
        self.figure.subplots_adjust(hspace=0.0)
        self.canvas = FigureCanvasQTAgg(self.figure)
        vertical_layout = QVBoxLayout()

        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)


class MainGui(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.lblPath.setMaximumWidth(300)
        self.lblPath.setWordWrap(True)
        self.lblPath.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Таблица пикетов
        self.tablePickets.setColumnCount(3)
        self.tablePickets.setHorizontalHeaderLabels(['Pickets', 'Error, %', 'Status'])
        self.tablePickets.setColumnWidth(0, 75)
        self.tablePickets.setColumnWidth(1, 75)
        self.tablePickets.setColumnWidth(2, 90)
        self.tablePickets.setRowCount(0)

        # Таблица моделей
        self.tableModel.setColumnCount(3)
        self.tableModel.setHorizontalHeaderLabels(['ρ, Ohmm', 'h, m', 'z, m'])
        self.tableModel.setColumnWidth(0, 75)
        self.tableModel.setColumnWidth(1, 75)
        self.tableModel.setColumnWidth(2, 75)
        self.tableModel.setRowCount(0)

        # Таблица границ моделей
        self.tableModelBorders.setColumnCount(4)
        self.tableModelBorders.setHorizontalHeaderLabels(['ρ_min', 'ρ_max', 'h_min', 'h_max'])
        self.tableModelBorders.setColumnWidth(0, 75)
        self.tableModelBorders.setColumnWidth(1, 75)
        self.tableModelBorders.setColumnWidth(2, 75)
        self.tableModelBorders.setColumnWidth(3, 75)
        self.tableModelBorders.setRowCount(0)

        # Графика
        # Таб 1
        # разрез
        label_cross = QLabel()
        label_cross.setMaximumHeight(14)
        label_cross.setText('Cross-section')
        self.layoutGraphics.addWidget(label_cross)
        self.crossSectionPlot = MplWidget()
        self.crossSectionPlot.ax = self.crossSectionPlot.figure.add_subplot(111)
        self.crossSectionPlot.ax.set_xlabel('Pickets')
        self.crossSectionPlot.ax.set_ylabel('Depth, m')
        self.crossSectionPlot.figure.tight_layout()
        self.layoutGraphics.addWidget(NavigationToolbar(self.crossSectionPlot.canvas, self))
        self.layoutGraphics.addWidget(self.crossSectionPlot)
        self.layoutGraphics.setContentsMargins(0, 0, 0, 0)
        self.layoutGraphics.setSpacing(0)
        # диапазон значений для цвета
        self.cross_section_min_value_colorbar = 0
        self.cross_section_max_value_colorbar = 0
        self.cross_section_auto_value_color_bar = True
        # диапазон шкалы z
        self.cross_section_min_value_altitude = 0
        self.cross_section_max_value_altitude = 0
        self.cross_section_auto_value_altitude = True
        # развернутый профиль
        self.cross_section_reversed = False
        # Отображение графика ошибок
        self.cross_section_error_view = True
        # Отображение надписей пикетов
        self.cross_section_pk_label_view = True

        # кривые
        label_curve = QLabel()
        label_curve.setMaximumHeight(14)
        label_curve.setText('Curves')
        self.layoutGraphics.addWidget(label_curve)
        self.curvesPlot = MplWidget()
        self.curvesPlot.ax = self.curvesPlot.figure.add_subplot(111)
        self.curvesPlot.ax.set_xlabel('Times, ms')
        self.curvesPlot.ax.set_ylabel('Emf/I, mV/A')
        self.curvesPlot.figure.tight_layout()
        self.layoutGraphics.addWidget(NavigationToolbar(self.curvesPlot.canvas, self))
        self.layoutGraphics.addWidget(self.curvesPlot)

        # Таб 2
        # карта
        self.mapPlot = MplWidget()
        self.mapPlot.ax = self.mapPlot.figure.add_subplot(111)
        self.mapPlot.ax.set_xlabel('X')
        self.mapPlot.ax.set_ylabel('Y')
        self.mapPlot.figure.tight_layout()
        self.layoutMapGraphics.addWidget(NavigationToolbar(self.mapPlot.canvas, self))
        self.layoutMapGraphics.addWidget(self.mapPlot)
        self.layoutMapGraphics.setContentsMargins(0, 0, 0, 0)
        self.layoutMapGraphics.setSpacing(0)
        self.map_section_is_relative_depths = True
        self.map_section_is_view_pickets_label = True
        self.map_section_excluding_profiles = []
        self.cube_data: np.ndarray | None = None
        self.verticalSliderMap.setTickInterval(1)

        # Таб 3
        # псевдосекция
        self.pseudo_curvesPlot = MplWidget()
        self.pseudo_curvesPlot.ax = self.pseudo_curvesPlot.figure.add_subplot(111)
        self.pseudo_curvesPlot.ax.set_xlabel('Distance, m')
        self.pseudo_curvesPlot.ax.set_ylabel('Emf')
        self.pseudo_curvesPlot.figure.tight_layout()
        self.layoutPseudoSection.addWidget(NavigationToolbar(self.pseudo_curvesPlot.canvas, self))
        self.layoutPseudoSection.addWidget(self.pseudo_curvesPlot)

        self.tab_widget.setCurrentWidget(self.tab_widget.findChild(QWidget, 'tabProfile'))

        # MAX ITERATION
        self.spinBoxMaxIteration.setMinimum(1)
        self.spinBoxMaxIteration.setMaximum(500)

    def open_file_dialog(self, _title='Выберите файл', _filter='Все файлы (*)') -> str:
        file_path, _ = QFileDialog.getOpenFileName(self, _title, '', _filter)
        return file_path

    def save_file_dialog(self, _title='Выберите файл', _filter='Все файлы (*)') -> str:
        file_path, _ = QFileDialog.getSaveFileName(self, _title, '', _filter)
        return file_path

    def show_error(self, message):
        QMessageBox.critical(self, 'Ошибка', message)

    def show_information(self, message):
        QMessageBox.information(self, 'Information', message)

    def show_question_yes_no(self, title, question):
        ans = QMessageBox.question(self, title, question)
        if ans == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    def show_select_profiles(self, profiles, title='Select profiles', all_checked=True):
        dialog = ProfileSelectionDialog(self, title, profiles, all_checked)
        result = dialog.exec()
        if result == QMessageBox.DialogCode.Accepted:
            return dialog.selected_profile
        return []

    def show_alpha_coefficient_input(self, default_value: float = 0.010):
        dialog = InputDoubleDialog(self, 'Input alpha coefficient', default_value)
        result = dialog.exec()
        if result == QMessageBox.DialogCode.Accepted:
            return dialog.double_value
        return None

    def show_srcpts_input(self, default_value: int = 7):
        dialog = InputIntegerDialog(self, 'Input scrpts', default_value)
        result = dialog.exec()
        if result == QMessageBox.DialogCode.Accepted:
            return dialog.integer_value
        return None

    def show_select_filters(self, h_filters, f_filters, selected_filters):
        dialog = FiltersSelectionDialogs(self, 'Select filters', h_filters, f_filters, selected_filters)
        result = dialog.exec()
        if result == QMessageBox.DialogCode.Accepted:
            self.lblHtArg.setText(f'Hankel: {dialog.selected_filters[0]}')
            self.lblFtArg.setText(f'Fourier: {dialog.selected_filters[1]}')
            return dialog.selected_filters
        return []

    def fill_vci_alpha_coefficient_menu(self, value):
        self.actionVCI_alpha.setText(f'VCI alpha = {value:.3f}')

    def fill_srcpts_menu(self, value):
        self.actionSrcpts.setText(f'srcpts: {value}')

    def fill_turn_off_menu(self, value):
        self.actionTurn_off_0_01_ms.setText(f'turn off: {value} ms')

    def fill_path_label(self, _path):
        self.lblPath.setText(os.path.basename(_path))

    def fill_combo_box_select_profile(self, profile_list):
        self.comboBoxSelectProfile.clear()
        self.comboBoxSelectProfile.addItems(profile_list)

    def fill_table_pickets(self, pickets_list, error_list):
        self.tablePickets.clearContents()
        self.tablePickets.setRowCount(0)
        self.tablePickets.setRowCount(len(pickets_list))
        for i, (pk, err) in enumerate(zip(pickets_list, error_list)):
            self.tablePickets.setItem(i, 0, QTableWidgetItem(str(pk)))
            self.tablePickets.setItem(i, 1, QTableWidgetItem(f'{err:.2f}'))
            self.tablePickets.setItem(i, 2, QTableWidgetItem('Ready'))
        self.tablePickets.resizeColumnsToContents()

    def get_selected_profile(self):
        return self.comboBoxSelectProfile.currentText()

    def curves_plot(self, times, observed, theoretical, begin_time, end_time, err=0.0):
        if times is None or len(times) == 0:
            print('Нет времен')
            return

        times = times * 1000  # s -> ms

        self.curvesPlot.ax.clear()

        if observed is not None:
            t1, c1, t2, c2 = utils.separate_curve_pos_neg(times, observed)
            self.curvesPlot.ax.loglog(t1, c1 * 1000, 'b^', alpha=0.1)
            self.curvesPlot.ax.loglog(t2, abs(c2) * 1000, 'bv', alpha=0.1)
            if begin_time != end_time:
                t1, c1, t2, c2 = utils.separate_curve_pos_neg(times[begin_time: end_time + 1],
                                                              observed[begin_time: end_time + 1])
                self.curvesPlot.ax.loglog(t1, c1 * 1000, 'b^', label='Obs (+)')
                self.curvesPlot.ax.loglog(t2, abs(c2) * 1000, 'bv', label='Obs (-)')

        if theoretical is not None and len(theoretical) != 0:
            t1, c1, t2, c2 = utils.separate_curve_pos_neg(times, theoretical)
            self.curvesPlot.ax.loglog(t1, c1 * 1000, 'r^--', alpha=0.2)
            self.curvesPlot.ax.loglog(t2, abs(c2) * 1000, 'rv--', alpha=0.2)
            if begin_time != end_time:
                t1, c1, t2, c2 = utils.separate_curve_pos_neg(times[begin_time: end_time + 1],
                                                              theoretical[begin_time: end_time + 1])
                self.curvesPlot.ax.loglog(t1, c1 * 1000, 'r^--', label='Theor (+)')
                self.curvesPlot.ax.loglog(t2, abs(c2) * 1000, 'rv--', label='Theor (-)')

        self.curvesPlot.ax.set_title(f'RMSRE is {err:.2f}%')
        self.curvesPlot.ax.grid()
        self.curvesPlot.ax.legend()
        self.curvesPlot.ax.set_xlabel('Times, ms')
        self.curvesPlot.ax.set_ylabel('Emf/I, mV/A')
        self.curvesPlot.figure.tight_layout()
        self.curvesPlot.canvas.draw_idle()

    def cross_section_plot(self, data_for_mesh, data_for_errors):

        X, Z, rho_by_every_meter_2d = data_for_mesh
        distances, errors, pickets = data_for_errors
        errors = errors * 100

        for ax in self.crossSectionPlot.canvas.figure.axes:
            ax.set_xscale('linear')  # Чтобы не было warning non-linear
            ax.clear()
        self.crossSectionPlot.canvas.figure.clf()
        self.crossSectionPlot.ax = self.crossSectionPlot.figure.add_subplot(111)

        if self.cross_section_auto_value_color_bar:
            v_min = np.min(rho_by_every_meter_2d)
            v_max = np.max(rho_by_every_meter_2d)
        else:
            v_min = self.cross_section_min_value_colorbar
            v_max = self.cross_section_max_value_colorbar

        self.cross_section_min_value_colorbar, self.cross_section_max_value_colorbar = v_min, v_max

        cmap = cm.get_cmap('jet')

        mesh = self.crossSectionPlot.ax.pcolormesh(X, Z, rho_by_every_meter_2d,
                                                   norm=LogNorm(v_min, v_max, True), shading='nearest', cmap=cmap)

        cbar = self.crossSectionPlot.figure.colorbar(mesh, ax=self.crossSectionPlot.ax,
                                                     ticks=LogLocator(subs=range(10)),
                                                     format=ticker.LogFormatterMathtext(labelOnlyBase=False),
                                                     label='Удельное сопротивление (Ом·м)',
                                                     fraction=0.03, pad=0.05, extend='both')

        self.crossSectionPlot.ax.set_xlabel('Distances, m')
        self.crossSectionPlot.ax.set_ylabel('Alt, m')

        if self.cross_section_auto_value_altitude:
            basement_z = Z[:, -1]

            min_lim = basement_z.max()
            max_lim = Z.max()
            max_lim = max_lim + max_lim * 0.02
        else:
            min_lim = self.cross_section_min_value_altitude
            max_lim = self.cross_section_max_value_altitude

        self.cross_section_min_value_altitude, self.cross_section_max_value_altitude = min_lim, max_lim
        self.crossSectionPlot.ax.set_ylim(min_lim, max_lim)
        self.crossSectionPlot.ax.grid()

        # график ошибок
        if self.cross_section_error_view:
            ax2 = self.crossSectionPlot.ax.twinx()
            ax2.plot(distances, errors, 'ko--', linewidth=0.7, markersize=1, label='Error, %')
            ax2.set_ylabel('Error, %', color='k')
            ax2.set_ylim(0.0, max(errors) + 1)
            ax2.tick_params(axis='y', labelcolor='k')
            ax2.grid(False)

        # График с пикетами
        relief = Z[:, 0].copy()
        self.crossSectionPlot.ax.plot(distances, relief, 'ko-', linewidth=0.7, markersize=1)
        # отображение надписей
        if self.cross_section_pk_label_view:
            for i, (x, y, label) in enumerate(zip(distances, relief, pickets)):
                self.crossSectionPlot.ax.annotate(f'{label}', xy=(x, y + y * 0.005),
                                                  ha='center', va='bottom', rotation='vertical', fontsize=8)

        self.crossSectionPlot.figure.tight_layout()
        self.crossSectionPlot.canvas.draw_idle()

    def map_plot(self, points, ab, current_pr=None):

        for ax in self.mapPlot.canvas.figure.axes:
            #ax.set_xscale('linear')
            #ax.set_yscale('linear')   # Чтобы не было warning non-linear
            ax.clear()

        self.mapPlot.canvas.figure.clf()
        self.mapPlot.ax = self.mapPlot.figure.add_subplot(111)

        # отрисовка среза
        if self.cube_data is not None:
            z_value = self.verticalSliderMap.value()
            mask = self.cube_data[:, 2] == z_value
            slice_pts = self.cube_data[mask]
            if len(slice_pts) <= 10:
                print(f"Нет данных на глубине z = {z_value}")
                return
            xx = slice_pts[:, 0]
            yy = slice_pts[:, 1]
            rho = slice_pts[:, 3]
            # Интерполяция
            grid_res = 100
            xi = np.linspace(xx.min(), xx.max(), grid_res)
            yi = np.linspace(yy.min(), yy.max(), grid_res)
            Xi, Yi = np.meshgrid(xi, yi)

            log_rho = np.log10(rho)
            log_rho_grid = griddata((xx, yy), log_rho, (Xi, Yi), method='cubic')
            rho_grid = 10 ** log_rho_grid

            if self.cross_section_auto_value_color_bar:
                v_min = np.nanmin(rho_grid)
                v_max = np.nanmax(rho_grid)
            else:
                v_min = self.cross_section_min_value_colorbar
                v_max = self.cross_section_max_value_colorbar
            cmap = cm.get_cmap('jet')
            mesh = self.mapPlot.ax.pcolormesh(Xi, Yi, rho_grid,
                                              norm=LogNorm(vmin=v_min, vmax=v_max),
                                              shading='nearest', cmap=cmap)
            divider = make_axes_locatable(self.mapPlot.ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            cbar = self.mapPlot.figure.colorbar(mesh, cax=cax,
                                                ticks=LogLocator(subs=range(10)),
                                                format=ticker.LogFormatterMathtext(labelOnlyBase=False),
                                                label='Удельное сопротивление (Ом·м)',
                                                fraction=0.03, pad=0.05, extend='both')

            self.mapPlot.ax.set_title(f'Горизонтальный срез на {z_value} м')

        for coord in ab:
            a, b = coord
            ax, ay, az = a
            bx, by, bz = b
            self.mapPlot.ax.plot([ax, bx], [ay, by], 'ko-', linewidth=2, markersize=5)
            if self.map_section_is_view_pickets_label:
                self.mapPlot.ax.annotate('A', xy=(ax, ay), xytext=(0, 10), textcoords='offset points', ha='center',
                                         va='center', fontsize=12)
                self.mapPlot.ax.annotate('B', xy=(bx, by), xytext=(0, 10), textcoords='offset points', ha='center',
                                         va='center', fontsize=12)

        x = [p.coordinate.x for p in points]
        y = [p.coordinate.y for p in points]
        pr = [p.pr for p in points]
        pk = [p.pk for p in points]
        colors = [1 if p == current_pr else 0 for p in pr]

        self.mapPlot.ax.scatter(x, y, c=colors, cmap='plasma', s=15, edgecolors='k')
        if self.map_section_is_view_pickets_label:
            for i in [0, len(pr) - 1]:
                self.mapPlot.ax.annotate(f'Pr.{pr[i]}_Pk.{pk[i]}', xy=(x[i], y[i]), xytext=(0, 10),
                                         textcoords='offset points',
                                         ha='center', va='center', fontsize=8)
            for i in range(1, len(pk)):
                if pr[i] != pr[i - 1]:
                    self.mapPlot.ax.annotate(f'Pr.{pr[i]}_Pk.{pk[i]}', xy=(x[i], y[i]), xytext=(0, 10),
                                             textcoords='offset points', ha='center', va='center', fontsize=8)
                    self.mapPlot.ax.annotate(f'Pr.{pr[i - 1]}_Pk.{pk[i - 1]}', xy=(x[i - 1], y[i - 1]), xytext=(0, 10),
                                             textcoords='offset points', ha='center', va='center', fontsize=8)

        self.mapPlot.ax.grid()
        self.mapPlot.ax.set_aspect('equal')

        self.mapPlot.ax.set_xlabel('x, m')
        self.mapPlot.ax.set_ylabel('y, m')
        self.mapPlot.figure.tight_layout()

        self.mapPlot.figure.canvas.draw_idle()

    @staticmethod
    def set_color_table_item_by_fix(item, fix):
        color = QBrush(BLUE_COLOR if fix else YELLOW_COLOR)
        item.setBackground(color)

    def fill_table_model_only_value(self, rho, h):
        for i, r in enumerate(rho):
            self.tableModel.item(i, 0).setText(f'{np.exp(r):.2f}')
        for i, v in enumerate(h):
            self.tableModel.item(i, 1).setText(f'{v:.2f}')
        z = np.insert(np.cumsum(h), 0, 0.0)
        for i in range(len(z) - 1):
            self.tableModel.item(i, 2).setText(f'{z[i]:.2f}')

    def fill_table_model_environment(self, rho, rho_min, rho_max, rho_fix, h, h_min, h_max, h_fix):
        n_layer = len(rho)
        # значения и фиксы
        self.tableModel.clearContents()
        self.tableModel.setRowCount(n_layer)

        for i, (r, f) in enumerate(zip(rho, rho_fix)):
            q_item = QTableWidgetItem(f'{np.exp(r):.2f}')
            MainGui.set_color_table_item_by_fix(q_item, f)
            self.tableModel.setItem(i, 0, q_item)

        for i, (hv, f) in enumerate(zip(h, h_fix)):
            q_item = QTableWidgetItem(f'{hv:.2f}')
            MainGui.set_color_table_item_by_fix(q_item, f)
            self.tableModel.setItem(i, 1, q_item)

        z = np.insert(np.cumsum(h), 0, 0.0)
        for i in range(len(h)):
            q_item = QTableWidgetItem(f'{z[i]:.2f}')
            self.tableModel.setItem(i, 2, q_item)

        # границы
        self.tableModelBorders.clearContents()
        self.tableModelBorders.setRowCount(n_layer)
        for i, (mi, ma) in enumerate(zip(rho_min, rho_max)):
            q_item_min = QTableWidgetItem(f'{np.exp(mi):.2f}')
            q_item_max = QTableWidgetItem(f'{np.exp(ma):.2f}')
            self.tableModelBorders.setItem(i, 0, q_item_min)
            self.tableModelBorders.setItem(i, 1, q_item_max)

        for i, (mi, ma) in enumerate(zip(h_min, h_max)):
            q_item_min = QTableWidgetItem(f'{mi:.2f}')
            q_item_max = QTableWidgetItem(f'{ma:.2f}')
            self.tableModelBorders.setItem(i, 2, q_item_min)
            self.tableModelBorders.setItem(i, 3, q_item_max)

    def get_model_into_table(self):
        """Изменение модели слоев из таблицы"""
        rho_list = np.zeros(self.tableModel.rowCount())

        for i in range(self.tableModel.rowCount()):
            item = self.tableModel.item(i, 0)
            rho_list[i] = np.log(float(item.text()))

        h_list = np.zeros(self.tableModel.rowCount() - 1)
        for i in range(self.tableModel.rowCount() - 1):
            item = self.tableModel.item(i, 1)
            h_list[i] = float(item.text())
        return rho_list, h_list

    def get_model_borders_into_table(self):
        """Изменение модели границ слоев из таблицы"""
        rho_list_min = np.zeros(self.tableModelBorders.rowCount())
        rho_list_max = np.zeros(self.tableModelBorders.rowCount())
        for i in range(self.tableModelBorders.rowCount()):
            item_min = self.tableModelBorders.item(i, 0)
            item_max = self.tableModelBorders.item(i, 1)
            rho_list_min[i] = np.log(float(item_min.text()))
            rho_list_max[i] = np.log(float(item_max.text()))

        h_list_min = np.zeros(self.tableModelBorders.rowCount() - 1)
        h_list_max = np.zeros(self.tableModelBorders.rowCount() - 1)
        for i in range(self.tableModelBorders.rowCount() - 1):
            item_min = self.tableModelBorders.item(i, 2)
            item_max = self.tableModelBorders.item(i, 3)
            h_list_min[i] = float(item_min.text())
            h_list_max[i] = float(item_max.text())
        return rho_list_min, rho_list_max, h_list_min, h_list_max

    def progress_bar_initial_settings(self, begin: int, end: int):
        self.progressBar.setMinimum(begin)
        self.progressBar.setMaximum(end)
        self.progressBar.setValue(begin)

    def progress_bar_iteration(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

    def enable_gui_element(self, lock: bool):
        self.tablePickets.setEnabled(lock)
        self.tableModel.setEnabled(lock)
        self.tableModelBorders.setEnabled(lock)

        self.comboBoxSelectProfile.setEnabled(lock)
        self.edLoopArea.setEnabled(lock)
        self.edLoopHeight.setEnabled(lock)
        self.spinBoxEndTime.setEnabled(lock)
        self.spinBoxBeginTime.setEnabled(lock)
        self.checkBoxUseRobustError.setEnabled(lock)
        self.checkBoxIgnoreInvertedValue.setEnabled(lock)
        self.checkBoxVCI.setEnabled(lock)

        self.btnSetBeginEndForAll.setEnabled(lock)
        self.btnSetBeginEndForSelected.setEnabled(lock)

        self.comboBoxSelectInverseMethods.setEnabled(lock)

        self.btnLoad.setEnabled(lock)
        self.btnSaveData.setEnabled(lock)
        self.btnDirectProblem.setEnabled(lock)
        self.btnDirectProblemAll.setEnabled(lock)
        self.btnDirectProblemMulti.setEnabled(lock)
        self.btnInverseProblem.setEnabled(lock)
        self.btnInverseProblemAll.setEnabled(lock)
        self.btnInverseProblemMulti.setEnabled(lock)
        self.btnPlotCrossSection.setEnabled(lock)
        self.brnSelectFilters.setEnabled(lock)

        self.spinBoxMaxIteration.setEnabled(lock)

        self.btnSmoothModelBoth.setEnabled(lock)
        self.btnSmoothModelRho.setEnabled(lock)
        self.btnSmoothModelThickness.setEnabled(lock)

        self.btnCreateVCILayers.setEnabled(lock)
        self.btnAddLayer.setEnabled(lock)
        self.btnDeleteLayer.setEnabled(lock)
        self.btnCopyModel.setEnabled(lock)
        self.btnCopyModelBorders.setEnabled(lock)
        self.btnPasteModel.setEnabled(lock)
        self.btnPasteModelForAll.setEnabled(lock)
        QApplication.processEvents()

    def cross_section_settings_view(self) -> bool:
        """
        Вызов окна настроек разреза
        :return:
        """
        init_value = (self.cross_section_auto_value_color_bar, self.cross_section_auto_value_altitude,
                      self.cross_section_min_value_colorbar, self.cross_section_max_value_colorbar,
                      self.cross_section_min_value_altitude, self.cross_section_max_value_altitude,
                      self.cross_section_reversed, self.cross_section_error_view, self.cross_section_pk_label_view)
        dialog = CrossSectionSettingsDialog(self, init_value)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = dialog.get_values()
            self.cross_section_auto_value_color_bar = result[0]
            self.cross_section_auto_value_altitude = result[1]
            self.cross_section_min_value_colorbar = result[2]
            self.cross_section_max_value_colorbar = result[3]
            self.cross_section_min_value_altitude = result[4]
            self.cross_section_max_value_altitude = result[5]
            self.cross_section_reversed = result[6]
            self.cross_section_error_view = result[7]
            self.cross_section_pk_label_view = result[8]
            return True
        else:
            return False

    def map_section_settings_view(self) -> bool:
        """
        checkBoxAutoColorBar - initial_values[0]
        checkBoxRelativeDepths - initial_values[1]
        minValueColorBar - initial_values[2]
        maxValueColorBar - initial_values[3]
        checkBoxViewPicketsLabel - initial_values[4]
        :return:
        """
        init_value = (self.cross_section_auto_value_color_bar, self.map_section_is_relative_depths,
                      self.cross_section_min_value_colorbar, self.cross_section_max_value_colorbar,
                      self.map_section_is_view_pickets_label)
        dialog = MapSectionSettingsDialog(self, init_value)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = dialog.get_values()
            self.cross_section_auto_value_color_bar = result[0]
            self.map_section_is_relative_depths = result[1]
            self.cross_section_min_value_colorbar = result[2]
            self.cross_section_max_value_colorbar = result[3]
            self.map_section_is_view_pickets_label = result[4]
            return True
        else:
            return False
