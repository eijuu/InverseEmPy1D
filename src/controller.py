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


import logging
import os
import time as tmr
from datetime import datetime
from multiprocessing import Pool

import numpy as np
from PyQt6.QtWidgets import QTableWidgetItem, QApplication, QInputDialog, QMessageBox, QErrorMessage
from scipy.optimize import minimize

import utils
from main_gui import MainGui
from models import SurveyData, ModelEnvironment, PointSounding


def inverse_problem_for_one_point(args: PointSounding | None, callback=None):
    """
    Inverse problem for one point.
    :param args:
    :param callback:
    :return:
    """
    if not args.vci:
        # подбираемые параметры
        p_0 = args.get_param_models()
        # границы подбираемых параметров
        bounds = args.get_param_borders()
        # eps
        # n = len(p_0) // 2 + 1
        # eps_rho_list = [abs(b2 - b1) * 1e-5 for b1, b2 in bounds[:n]]
        # eps_h_list = [abs(b2 - b1) * 1e-6 for b1, b2 in bounds[n:]]
        # eps_list = eps_rho_list + eps_h_list

    else:
        p_0 = args.get_param_rho()
        bounds = args.get_param_borders_rho()
        # eps
        # eps_list = [abs(b2 - b1) * 1e-5 for b1, b2 in bounds]

    eps_list = 1e-6
    method = args.inverse_method
    # Базовые параметры для всех методов
    common_options = {
        'maxiter': args.max_iterations,
        'ftol': 1e-7,
        'disp': False
    }
    # Специфические параметры для каждого метода
    method_options = {
        'L-BFGS-B': {
            'gtol': 1e-6,
            'eps': eps_list
        },
        'Nelder-Mead': {
            'adaptive': True
            # gtol и eps не поддерживаются
        },
        'SLSQP': {
            'eps': eps_list
            # gtol не поддерживается
        },
        'TNC': {
            'gtol': 1e-6,
            'eps': eps_list
        },
        'Powell': {
            # gtol и eps не поддерживаются
        }
    }
    # Формируем финальный набор параметров
    options = common_options.copy()
    if method in method_options:
        options.update(method_options[method])

    # Удаляем неподдерживаемые параметры для каждого метода
    if method == 'Nelder-Mead':
        options.pop('gtol', None)
        options.pop('eps', None)
        options.pop('ftol', None)
    elif method == 'SLSQP':
        options.pop('gtol', None)
    elif method == 'Powell':
        options.pop('gtol', None)
        options.pop('eps', None)

    if not args.vci:

        # noinspection PyTypeChecker
        result = minimize(
            fun=args.minimize_function,
            x0=p_0,
            method=method,
            bounds=bounds,
            callback=callback,
            options=options
        )
        args.set_model_value(result.x)
    else:

        param_not_inverse = tuple(args.get_param_thickness())
        # noinspection PyTypeChecker
        result = minimize(
            fun=args.minimize_function_vci,
            x0=p_0,
            args=(param_not_inverse,),
            method=method,
            bounds=bounds,
            callback=callback,
            options=options
        )
        args.set_model_value(np.r_[result.x, param_not_inverse])

    args.direct_problem_calculate()
    return args


def direct_problem_for_one_point(args: PointSounding | None):
    args.direct_problem_calculate()
    args.error_value_calculate()
    return args


def auto_fitting_srcpts_worker(args: PointSounding | None):
    args.auto_fitting_srcpts(17, 0.03)
    return args


class MainController:
    copied_model_environment: ModelEnvironment | None
    current_row_in_table: int
    MAX_PROCESS_LIMIT: int

    def __init__(self, version):
        self.model = SurveyData()
        self.view = MainGui()
        self.view.setWindowTitle(f'InverseEmPy1D [{version}]')
        self._connect_signals()

        self.current_row_in_table = -1
        self.copied_model_environment = None
        self.INVERSE_METHOD = 'L-BFGS-B'
        self.MAX_ITERATIONS = 30
        self.MAX_PROCESS_LIMIT = 30

        self.path_to_file = ''
        self.vci_check = False

        with open('filters', 'r') as f:
            filt = [line.strip() for line in f]
        self.dlf_filters = filt
        self.view.lblHtArg.setText(f'Hankel: {self.dlf_filters[0]}')
        self.view.lblFtArg.setText(f'Fourier: {self.dlf_filters[1]}')

        logging.basicConfig(level=logging.INFO, filename='log.log', format='%(asctime)s %(levelname)s %(message)s',
                            encoding='utf-8', filemode='w')

    def _connect_signals(self):
        # кнопки

        # Загрузка, сохранение
        self.view.btnLoad.clicked.connect(self.load_data)
        self.view.btnSaveData.clicked.connect(self.save_data)

        # Прямые задачи
        self.view.btnDirectProblem.clicked.connect(self.direct_problem_calculate)
        self.view.btnDirectProblemMulti.clicked.connect(self.direct_problem_calculate_multi)
        self.view.btnDirectProblemAll.clicked.connect(self.direct_problem_calculate_all)

        # фильтры
        self.view.brnSelectFilters.clicked.connect(self.select_filters)

        self.view.btnInverseProblem.clicked.connect(lambda: self.inverse_problem_calculate_united('current'))
        self.view.btnInverseProblemMulti.clicked.connect(lambda: self.inverse_problem_calculate_united('selected'))
        self.view.btnInverseProblemAll.clicked.connect(lambda: self.inverse_problem_calculate_united('all'))

        # Настройка срезов времен
        self.view.btnBeginTimeApply.clicked.connect(self.set_begin_index_time_for_selected)
        self.view.btnEndTimeApply.clicked.connect(self.set_end_index_time_for_selected)

        # Отрисовка разреза
        self.view.btnPlotCrossSection.clicked.connect(self.cross_section_plot)

        # Сглаживание разреза
        self.view.btnSmoothModelThickness.clicked.connect(self.smooth_model_thickness)
        self.view.btnSmoothModelRho.clicked.connect(self.smooth_model_rho)
        self.view.btnSmoothModelBoth.clicked.connect(self.smooth_model_both)

        # настройки разреза
        self.view.btnCrossSectionSettings.clicked.connect(self.cross_section_settings)

        # Кнопки редактирования моделей
        self.view.btnAddLayer.clicked.connect(self.add_layer)
        self.view.btnDeleteLayer.clicked.connect(self.delete_layer)
        self.view.btnCopyModel.clicked.connect(self.copy_model)
        self.view.btnCopyModelBorders.clicked.connect(self.copy_model_borders)
        self.view.btnPasteModel.clicked.connect(self.paste_model)
        self.view.btnPasteModelForAll.clicked.connect(self.paste_model_to_all)
        self.view.btnCreateVCILayers.clicked.connect(self.create_vci_model)

        # Выбор профиля и пикета
        self.view.comboBoxSelectProfile.activated.connect(self.change_current_profile)
        self.view.tablePickets.itemSelectionChanged.connect(self.picket_table_clicked)

        # выбор метода инверсии
        self.view.comboBoxSelectInverseMethods.activated.connect(self.select_inverse_method)

        # текстовые поля
        self.view.btnLoopAreaApply.clicked.connect(self.set_loop_area)
        self.view.btnLoopHeightApply.clicked.connect(self.set_loop_height)

        # изменение модели
        self.view.tableModel.cellClicked.connect(self.change_model_layer_controller)
        self.view.tableModelBorders.cellClicked.connect(self.change_model_layer_border_controller)

        # чекбоксы
        self.view.checkBoxUseRobustError.clicked.connect(self.set_use_robust_value)
        self.view.checkBoxIgnoreInvertedValue.clicked.connect(self.set_ignore_negative_value)
        self.view.checkBoxVCI.clicked.connect(self.set_vci_value)
        self.view.checkBoxTablePicketsAdvanceColumnView.clicked.connect(self.checkbox_table_picket_advance_column_view_check)

        self.view.check_box_curves_plot_log_y.clicked.connect(self.checkbox_curves_plot_log_y_check)

        # карта
        self.view.tab_widget.currentChanged.connect(self.tab_widget_page_change)
        self.view.btnDrawMap.clicked.connect(self.map_plot)
        self.view.btnExcludingProfiles.clicked.connect(self.excluding_profiles_for_map_plot)
        self.view.btnMapSectionSettings.clicked.connect(self.map_section_settings)
        self.view.btnPrepareData.clicked.connect(self.prepare_data_for_map_section)
        self.view.verticalSliderMap.valueChanged.connect(self.on_map_vertical_slider_moved)

        # menu
        # export
        self.view.actionExport_to_ZondTEM1D.triggered.connect(self.export_to_zond_tem_1d)
        self.view.actionExport_results_to_text_dat.triggered.connect(self.export_model_by_pr_to_text)
        self.view.actionExport_results_by_horizontal_slice_to_text_dat.triggered.connect(self.export_current_view_map_to_text)

        self.view.actionVCI_alpha.triggered.connect(self.alpha_vci_value_dialog)
        self.view.actionSrcpts.triggered.connect(self.srcpts_value_dialog)
        self.view.actionAuto_fitting_srcpts.triggered.connect(self.auto_fitting_srcpts_process)

        self.view.actionTurn_off_0_01_ms.triggered.connect(self.turn_off_dialog)

        self.view.actionColorMap.triggered.connect(self.colormap_dialog)

    def load_data(self):
        """
        Загрузка наблюденных данных
        :return:
        """
        prev_path = self.path_to_file
        self.path_to_file = self.view.open_file_dialog('Select file with data', '*.emp')
        if self.path_to_file:
            try:
                self.view.fill_path_label(self.path_to_file)
                self.model.load_data(self.path_to_file)

                self.view.fill_combo_box_select_profile(self.model.get_profile_list())
                self.change_current_profile()

                self.view.edLoopArea.setText(str(self.model.points[0].loop_area))
                self.view.edLoopHeight.setText(str(self.model.points[0].loop_height))
                self.view.checkBoxVCI.setChecked(self.model.points[0].vci)

                self.view.checkBoxUseRobustError.setChecked(self.model.points[0].use_robust)
                self.view.checkBoxIgnoreInvertedValue.setChecked(self.model.points[0].ignore_negative_value)
                self.view.spinBoxBeginTime.setValue(0)
                self.view.spinBoxEndTime.setValue(len(self.model.points[0].times) - 1)
                self.view.spinBoxEndTime.setMaximum(len(self.model.points[0].times) - 1)
                self.view.spinBoxMaxIteration.setValue(self.MAX_ITERATIONS)

                self.view.fill_vci_alpha_coefficient_menu(self.model.points[0].alpha_coefficient_tikhonov)

                self.view.fill_srcpts_menu(self.model.points[0].src_pts)

            except Exception as e:
                self.view.show_error(f'Load error: {str(e)}')
        else:
            self.path_to_file = prev_path

    def save_data(self):
        self.path_to_file = self.view.save_file_dialog('Select filename for save', '*.emp')
        if self.path_to_file:
            try:
                self.model.save_data(self.path_to_file)
                self.view.fill_path_label(self.path_to_file)
                self.view.show_information('Project saved')

            except Exception as e:
                self.view.show_error(f'Save error: {str(e)}')

    def change_current_profile(self):
        # текущий профиль из комбобокса
        current_profile = int(self.view.get_selected_profile())
        # получение списка пикетов из текущего профиля
        pickets_list = self.model.get_picket_list(current_profile)
        # заполнение
        dict_list_data = []
        for pk in pickets_list:
            p = self.model.get_point(current_profile, pk)
            dict_list_data.append({
                'pk': p.pk,
                'error': p.error_value * 100,
                'area': p.loop_area,
                'height': p.loop_height,
                'src_pts': p.src_pts,
                'begin_time': p.begin_time,
                'end_time': p.end_time
            })
        # заполняем таблицу пикетов
        self.view.fill_table_pickets(dict_list_data)
        # отрисуем разрез текущего профиля
        self.cross_section_plot()
        # карта
        self.map_plot()

    def update_table_picket(self):
        pr = int(self.view.comboBoxSelectProfile.currentText())
        selected_indexes = self.view.tablePickets.selectionModel().selectedRows()
        for index in selected_indexes:
            row = index.row()
            pk = int(self.view.tablePickets.item(row, 0).text())
            point = self.model.get_point(pr, pk)

            self.view.tablePickets.item(row, 1).setText(f'{point.error_value * 100:.2f}')
            self.view.tablePickets.item(row, 3).setText(f'{point.loop_area:.2f}')
            self.view.tablePickets.item(row, 4).setText(f'{point.loop_height:.2f}')
            self.view.tablePickets.item(row, 5).setText(f'{point.src_pts:d}')
            self.view.tablePickets.item(row, 6).setText(f'{point.begin_time:d}')
            self.view.tablePickets.item(row, 7).setText(f'{point.end_time:d}')

    def picket_table_clicked(self):
        row = self.view.tablePickets.currentRow()
        if row < 0:
            print('нет данных в таблице')
            return

        pk = self.view.tablePickets.item(row, 0)
        if pk is None:
            print('нет данных ячейке')
            return
        self.change_current_picket()

    def curves_plot(self):
        if self.model.current_index == -1:
            return
        if self.view.tab_widget.currentIndex() != 0:
            return
        self.view.curves_plot(self.model.current_point().times,
                              self.model.current_point().observed_curve,
                              self.model.current_point().theory_curve,
                              self.model.current_point().begin_time,
                              self.model.current_point().end_time,
                              self.model.current_point().error_value * 100)

    def change_current_picket(self):
        self.current_row_in_table = self.view.tablePickets.currentRow()
        pk = self.view.tablePickets.item(self.current_row_in_table, 0)
        curr_pk = int(pk.text())
        curr_pr = int(self.view.comboBoxSelectProfile.currentText())

        self.model.select_current_index(curr_pr, curr_pk)
        if self.model.current_index == -1:
            print('Нет такого профиля и пикета')
            return

        # Рисунок
        self.curves_plot()

        # модель
        self.fill_table_model_environment()
        # текущее значение begin end
        self.view.spinBoxBeginTime.setValue(self.model.current_point().begin_time)
        self.view.spinBoxEndTime.setValue(self.model.current_point().end_time)

        self.view.edLoopHeight.setText(f'{self.model.current_point().loop_height}')
        self.view.edLoopArea.setText(f'{self.model.current_point().loop_area}')

        # src pts
        self.view.fill_srcpts_menu(self.model.current_point().src_pts)

    def fill_table_model_environment(self):
        self.view.fill_table_model_environment(self.model.current_point().model_environment.rho_value,
                                               self.model.current_point().model_environment.rho_value_min,
                                               self.model.current_point().model_environment.rho_value_max,
                                               self.model.current_point().model_environment.rho_value_fix,
                                               self.model.current_point().model_environment.thickness_value,
                                               self.model.current_point().model_environment.thickness_value_min,
                                               self.model.current_point().model_environment.thickness_value_max,
                                               self.model.current_point().model_environment.thickness_value_fix)

    def fill_table_model_environment_only_value(self):
        self.view.fill_table_model_only_value(self.model.current_point().model_environment.rho_value,
                                              self.model.current_point().model_environment.thickness_value)

    def set_loop_area(self):
        if self.model.current_index == -1:
            return
        pr = int(self.view.comboBoxSelectProfile.currentText())
        selected_indexes = self.view.tablePickets.selectionModel().selectedRows()
        if not selected_indexes:
            return
        area = self.view.edLoopArea.text()
        area_float = utils.try_str_to_float(area)
        if area_float is None:
            return
        self.view.enable_gui_element(False)  # lock gui

        for row in selected_indexes:
            pk = int(self.view.tablePickets.item(row.row(), 0).text())
            point_index = self.model.get_index(pr, pk)
            self.model.points[point_index].loop_area = area

        self.change_current_picket()
        self.update_table_picket()
        self.view.enable_gui_element(True)  # unlock gui

    def set_loop_height(self):
        if self.model.current_index == -1:
            return
        pr = int(self.view.comboBoxSelectProfile.currentText())
        selected_indexes = self.view.tablePickets.selectionModel().selectedRows()
        if not selected_indexes:
            return
        height = self.view.edLoopHeight.text()
        height_float = utils.try_str_to_float(height)
        if height_float is None:
            return
        self.view.enable_gui_element(False)  # lock gui

        for row in selected_indexes:
            pk = int(self.view.tablePickets.item(row.row(), 0).text())
            point_index = self.model.get_index(pr, pk)
            self.model.points[point_index].loop_height = height_float

        self.change_current_picket()
        self.update_table_picket()
        self.view.enable_gui_element(True)  # unlock gui

    def set_begin_end_for_all(self):
        """
        Изменение диапазона времен для всех точек
        :return:
        """
        if self.view.show_question_yes_no('Are yo sure?', 'Apply for all?'):
            self.view.enable_gui_element(False)  # lock gui
            begin = self.view.spinBoxBeginTime.value()
            end = self.view.spinBoxEndTime.value()
            self.model.set_begin_end_index_times_for_all(begin, end)
            self.view.enable_gui_element(True)  # unlock gui

    def set_begin_index_time_for_selected(self):
        """
        Изменение диапазона времен для выбранных точек
        :return:
        """
        if self.model.current_index == -1:
            return
        pr = int(self.view.comboBoxSelectProfile.currentText())
        selected_indexes = self.view.tablePickets.selectionModel().selectedRows()
        if not selected_indexes:
            return
        begin = self.view.spinBoxBeginTime.value()
        self.view.enable_gui_element(False)  # lock gui

        for row in selected_indexes:
            pk = int(self.view.tablePickets.item(row.row(), 0).text())
            point_index = self.model.get_index(pr, pk)
            self.model.points[point_index].set_begin_index_times(begin)

        self.change_current_picket()
        self.update_table_picket()
        self.view.enable_gui_element(True)  # unlock gui

    def set_end_index_time_for_selected(self):
        """
        Изменение диапазона времен для выбранных точек
        :return:
        """

        if self.model.current_index == -1:
            return
        pr = int(self.view.comboBoxSelectProfile.currentText())
        selected_indexes = self.view.tablePickets.selectionModel().selectedRows()
        if not selected_indexes:
            return
        end = self.view.spinBoxEndTime.value()
        self.view.enable_gui_element(False)  # lock gui

        for row in selected_indexes:
            pk = int(self.view.tablePickets.item(row.row(), 0).text())
            point_index = self.model.get_index(pr, pk)
            self.model.points[point_index].set_end_index_times(end)

        self.change_current_picket()
        self.update_table_picket()
        self.view.enable_gui_element(True)  # unlock gui

    def set_turn_off(self, value):
        for p in self.model.points:
            p.turn_off = value

    def set_use_robust_value(self):
        """
        Установка использования робастной оценки для расчета ошибки
        :return:
        """
        flag = self.view.checkBoxUseRobustError.isChecked()
        self.model.set_use_robust_flag(flag)

    def set_ignore_negative_value(self):
        """
        Установка игнорировать негативные значения кривой
        :return:
        """
        flag = self.view.checkBoxIgnoreInvertedValue.isChecked()
        self.model.set_ignore_negative_value_flag(flag)

    def set_vci_value(self):
        flag = self.view.checkBoxVCI.isChecked()
        self.vci_check = flag
        self.model.set_vci_flag(flag)
        if self.current_row_in_table != -1:
            self.fill_table_model_environment()

    def direct_problem_calculate(self):
        """
        Расчет прямой задачи для одной точки с обновлением графики и таблицы
        :return:
        """
        if self.model.current_index == -1:
            return

        self.model.current_point().direct_problem_calculate()
        self.model.current_point().error_value_calculate()
        self.view.tablePickets.setItem(self.current_row_in_table, 1,
                                       QTableWidgetItem(f'{self.model.current_point().error_value * 100:.2f}'))

        self.curves_plot()

        a = np.array(self.model.current_point().theory_curve)
        np.savetxt('theoretical_curve.txt', a)

    def direct_problem_calculate_multi(self):
        self.view.enable_gui_element(False)  # lock gui

        selected_indexes = self.view.tablePickets.selectedIndexes()
        selected_rows = list(set(index.row() for index in selected_indexes))

        self.view.progress_bar_initial_settings(0, len(selected_rows) - 1)

        pr = int(self.view.comboBoxSelectProfile.currentText())
        selected_pk = [-1] * len(selected_rows)
        for i, row in enumerate(selected_rows):
            picket = self.view.tablePickets.item(row, 0)
            selected_pk[i] = int(picket.text())

        selected_points = [None] * len(selected_pk)
        for i, pk in enumerate(selected_pk):
            selected_points[i] = self.model.get_point(pr, pk)

        num_processes = min(os.cpu_count() - 1, len(selected_points), self.MAX_ITERATIONS)
        print(f"Запуск {num_processes} процессов для обработки {len(selected_points)} точек")

        with Pool(processes=num_processes) as pool:
            for i, res in enumerate(pool.imap_unordered(direct_problem_for_one_point, selected_points)):
                self.view.progress_bar_iteration()
                for row in selected_rows:
                    picket = self.view.tablePickets.item(row, 0)
                    if int(picket.text()) == res.pk:
                        self.view.tablePickets.item(row, 1).setText(f'{res.error_value * 100:.2f}')

                ind = self.model.get_index(res.pr, res.pk)
                self.model.points[ind] = res
                QApplication.processEvents()
        self.view.progressBar.setValue(0)

        self.view.enable_gui_element(True)  # unlock
        QApplication.processEvents()

    def direct_problem_calculate_all(self):
        """
        Рассчитать прямую задачу для всех точек
        :return:
        """
        if self.model.points is None or len(self.model.points) == 0:
            self.view.show_error('No points')
            return
        self.view.enable_gui_element(False)

        num_processes = min(os.cpu_count() - 1, len(self.model.points), self.MAX_PROCESS_LIMIT)
        self.view.progress_bar_initial_settings(0, len(self.model.points) - 1)
        print(f"Запуск {num_processes} процессов для обработки {len(self.model.points)} точек")

        time_start = tmr.time()
        with Pool(processes=num_processes) as pool:
            for i, res in enumerate(pool.imap_unordered(direct_problem_for_one_point, self.model.points)):
                self.view.progress_bar_iteration()
                ind = self.model.get_index(res.pr, res.pk)
                self.model.points[ind] = res
                QApplication.processEvents()

        time_end = tmr.time()
        delta_time = time_end - time_start

        print(f'Прямая задача для всех точек завершена за {delta_time:.2f} sec')

        self.view.progressBar.setValue(0)
        self.change_current_profile()
        self.view.enable_gui_element(True)  # lock gui
        QApplication.processEvents()

    def inverse_problem_calculate_united(self, scope='current'):
        """
        Инверсия
        :param scope:'current' - текущая точка, 'selected' - выделенные, 'all' - все точки
        :return:
        """
        # Определим список точек
        if scope == 'current':
            if self.model.current_index == -1:
                return
            points_to_process = [self.model.current_point()]
            use_callback = True

        elif scope == 'selected':
            selected_indexes = self.view.tablePickets.selectedIndexes()
            selected_rows = list(set(index.row() for index in selected_indexes))
            if not selected_rows:
                return
            pr = int(self.view.comboBoxSelectProfile.currentText())
            points_to_process = []
            for row in selected_rows:
                picket = int(self.view.tablePickets.item(row, 0).text())
                point = self.model.get_point(pr, picket)
                points_to_process.append(point)
            use_callback = False

        elif scope == 'all':
            if not self.model.points:
                return
            # если все, то можно выбрать какие именно профиля
            selected = self.view.show_select_profiles(self.model.get_profile_list())
            selected = list(map(int, selected))
            if len(selected) == 0:
                return
            points_to_process = []
            for pr in selected:
                pk_list = self.model.get_picket_list(pr)
                for pk in pk_list:
                    points_to_process.append(self.model.get_point(pr, pk))
            use_callback = False

        else:
            raise ValueError('Неверный scope. Используйте \'current\', \'selected\' или \'all\'.')

        # выбор инверсии (на всякий случай)
        self.select_inverse_method()

        # Подготовка UI
        self.view.enable_gui_element(False)
        self.view.progress_bar_initial_settings(0, len(points_to_process) - 1)
        self.view.btnInverseProblem.setText('Inversion...')

        # Если обрабатывается одна точка с callback
        if len(points_to_process) == 1 and use_callback:
            self.view.progress_bar_initial_settings(0, self.MAX_ITERATIONS)  # в прогресс баре макс кол-во это кол-во итераций
            self.view.tablePickets.item(self.current_row_in_table, 2).setText('Inverse...')

            QApplication.processEvents()

        # Запуск инверсии
        time_start = tmr.time()
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        print('Current Time =', current_time)
        logging.info(f'Current Time = {current_time}')

        if len(points_to_process) == 1 and use_callback:
            # для одной точки
            def callback(params):
                # print('Iter')
                self.view.tablePickets.item(self.current_row_in_table, 1).setText(
                    f'{self.model.current_point().error_value * 100:.2f}')
                self.curves_plot()

                self.model.current_point().set_model_value(params)
                self.fill_table_model_environment_only_value()
                self.view.progress_bar_iteration()
                QApplication.processEvents()

            result = inverse_problem_for_one_point(self.model.current_point(), callback=callback)
            # Обновляем модель и интерфейс после завершения
            self.model.current_point().set_model_value(result.get_param_models())
            self.fill_table_model_environment_only_value()
            self.direct_problem_calculate()
            self.view.tablePickets.item(self.current_row_in_table, 2).setText('Ready')
        else:
            # Многопроцессорная инверсия для нескольких точек
            num_processes = min(os.cpu_count() - 1, len(points_to_process), self.MAX_PROCESS_LIMIT)

            print(f'Запуск {num_processes} процессов для обработки {len(points_to_process)} точек')
            logging.info(f'Запуск {num_processes} процессов для обработки {len(points_to_process)} точек')

            with Pool(processes=num_processes) as pool:
                for i, res in enumerate(pool.imap_unordered(inverse_problem_for_one_point, points_to_process)):
                    print(f'Завершено {i + 1}/{len(points_to_process)} точек ({res.error_value * 100:.2f} %)')
                    logging.info(f'Завершено {i + 1}/{len(points_to_process)} точек ({res.error_value * 100:.2f} %)')
                    ind = self.model.get_index(res.pr, res.pk)
                    self.model.points[ind] = res

                    # Обновляем соответствующие строки в таблице
                    for row in range(self.view.tablePickets.rowCount()):
                        if (int(self.view.tablePickets.item(row, 0).text()) == res.pk and
                                int(self.view.comboBoxSelectProfile.currentText()) == res.pr):
                            self.view.tablePickets.item(row, 1).setText(f'{res.error_value * 100:.2f}')
                            self.view.tablePickets.item(row, 2).setText('Ready')
                            break
                    self.view.progress_bar_iteration()
                    QApplication.processEvents()

        # Завершение
        time_end = tmr.time()
        delta_time = time_end - time_start
        hours = int(delta_time / 3600)
        minutes = int((delta_time - int(hours * 3600)) / 60)
        sec = delta_time - hours * 3600 - minutes * 60
        print(f'Обработка всех точек завершена за {hours} ч {minutes} мин {sec:.2f} секунд! ({delta_time:.2f} sec)')
        logging.info(f'Обработка всех точек завершена за {hours} ч {minutes} мин {sec:.2f} секунд! ({delta_time:.2f} sec)')
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        print('Current Time =', current_time)
        logging.info(f'Current Time = {current_time}')
        self.view.progressBar.setValue(0)
        self.view.btnInverseProblem.setText('Inverse problem')
        self.view.enable_gui_element(True)
        QApplication.processEvents()
        if self.path_to_file != '' and len(points_to_process) > 1:
            self.model.save_data(self.path_to_file)

    def cross_section_plot(self):
        """
        Отрисовка разреза
        :return:
        """
        pr = int(self.view.comboBoxSelectProfile.currentText())
        if self.view.tab_widget.currentIndex() != 0:
            return

        result = self.model.get_data_for_cross_section(pr, self.view.cross_section_reversed)
        if result is None:
            return
        (X, Z, rho_by_every_meter_2d), (distances, errors, pickets) = result
        rho_by_every_meter_2d = np.exp(rho_by_every_meter_2d)  # log(rho) -> rho

        self.view.cross_section_plot((X, Z, rho_by_every_meter_2d), (distances, errors, pickets))

    def map_plot(self):
        """
        отрисовка карты
        :return:
        """
        if self.model.points is None or len(self.model.points) == 0:
            return
        if self.view.tab_widget.currentIndex() != 1:
            return
        need_points = [p for p in self.model.points if p.pr not in self.view.map_section_excluding_profiles]
        ab = self.model.get_ab_coordinate_list()
        self.view.map_plot(need_points, ab, int(self.view.get_selected_profile()))

    def prepare_data_for_map_section(self):
        self.view.cube_data = self.model.get_cube_data_for_map(self.view.map_section_is_relative_depths, self.view.map_section_excluding_profiles)
        vmin = int(self.view.cube_data[:, 2].min())
        vmax = int(self.view.cube_data[:, 2].max())
        self.view.verticalSliderMap.blockSignals(True)
        self.view.verticalSliderMap.setRange(vmin, vmax)
        if self.view.map_section_is_relative_depths:
            self.view.verticalSliderMap.setValue(vmin)
            self.view.lblCurrentDepth.setText(f'{vmin}')
        else:
            self.view.verticalSliderMap.setValue(vmax)
            self.view.lblCurrentDepth.setText(f'{vmax}')
        self.view.verticalSliderMap.blockSignals(False)

    def excluding_profiles_for_map_plot(self):
        selected = self.view.show_select_profiles(self.model.get_profile_list(), 'Excluding profiles', False)
        selected = list(map(int, selected))
        self.view.map_section_excluding_profiles = selected

    def change_model_layer_controller(self):
        """
        Изменение значений в слоях модели
        :return:
        """
        if self.view.tableModel.rowCount() == 0:
            return
        rho_list, h_list = self.view.get_model_into_table()
        self.model.points[self.model.current_index].set_model_value(np.r_[rho_list, h_list])

    def change_model_layer_border_controller(self):
        """
        Изменение границ в слоях модели
        :return:
        """
        if self.view.tableModelBorders.rowCount() == 0:
            return
        rho_list_min, rho_list_max, h_list_min, h_list_max = self.view.get_model_borders_into_table()
        self.model.points[self.model.current_index].set_model_borders_value(
            rho_list_min, rho_list_max, h_list_min, h_list_max)

    def create_vci_model(self):
        """
        создать модель с увеличивающимся шагом h
        :return:
        """
        if self.model.current_index == -1:
            return
        first_layer_h, ok_pressed = QInputDialog.getDouble(None, 'Thickness, m', 'Input first layer h', value=3.0,
                                                           min=0.1, max=100.0, step=1)
        if not ok_pressed:
            return

        progressive_coefficient, ok_pressed = QInputDialog.getDouble(None, 'Progression coefficient', 'Input k:',
                                                                     value=1.2, min=1, max=3, step=0.1)
        if not ok_pressed:
            return

        n_layers, ok_pressed = QInputDialog.getInt(None, 'Layers number', 'Input layers number', value=7,
                                                   min=3, max=20, step=1)
        if not ok_pressed:
            return

        self.model.current_point().create_vci_model(first_layer_h, progressive_coefficient, n_layers)
        self.fill_table_model_environment()

    def add_layer(self):
        """
        Добавить слой перед выбранным слоем
        :return:
        """
        if self.model.current_index == -1:
            return
        index = self.view.tableModel.currentRow()
        self.model.current_point().insert_layer(index)
        self.fill_table_model_environment()

    def delete_layer(self):
        """
        Удалить выбранный слой
        :return:
        """
        if self.model.current_index == -1:
            return
        index = self.view.tableModel.currentRow()
        self.model.current_point().delete_layer(index)
        self.fill_table_model_environment()

    def copy_model(self):
        """
        Скопировать модель в память
        :return:
        """
        if self.model.current_index == -1:
            return
        self.copied_model_environment = ModelEnvironment.copy_model(self.model.current_point().model_environment)

    def copy_model_borders(self):
        """
        Скопировать в память только границы модели
        :return:
        """
        if self.model.current_index == -1:
            return
        self.copied_model_environment = ModelEnvironment.copy_only_borders(self.model.current_point().model_environment)

    def paste_model(self):
        """
        Вставить модели в выбранные пикеты
        :return:
        """
        if self.copied_model_environment is None:
            return

        self.view.enable_gui_element(False)  # lock gui
        selected_indexes = self.view.tablePickets.selectedIndexes()
        selected_rows = list(set(index.row() for index in selected_indexes))

        pr = int(self.view.comboBoxSelectProfile.currentText())
        selected_pk = [-1] * len(selected_rows)
        for i, row in enumerate(selected_rows):
            picket = self.view.tablePickets.item(row, 0)
            selected_pk[i] = int(picket.text())

        selected_index_in_list = [-1] * len(selected_pk)
        for i, pk in enumerate(selected_pk):
            selected_index_in_list[i] = self.model.get_index(pr, pk)

        for i in selected_index_in_list:
            self.model.points[i].model_environment.paste_model(self.copied_model_environment)

        self.fill_table_model_environment()
        self.view.enable_gui_element(True)  # unlock gui

    def paste_model_to_all(self):
        """
        Вставить скопированную модель на всю базу
        :return:
        """
        if self.copied_model_environment is None:
            return

        if self.view.show_question_yes_no('Are yo sure?', 'Paste to all?'):
            self.view.enable_gui_element(False)  # lock gui
            self.view.progress_bar_initial_settings(0, len(self.model.points))
            for i in range(len(self.model.points)):
                self.view.progress_bar_iteration()
                self.model.points[i].model_environment.paste_model(self.copied_model_environment)
            self.fill_table_model_environment()
            self.view.enable_gui_element(True)  # unlock gui
            self.view.progressBar.setValue(0)

    def smooth_model(self, smooth_thickness: bool, smooth_rho: bool):
        pr = int(self.view.comboBoxSelectProfile.currentText())
        pk_list = self.model.get_picket_list(pr)

        value, ok_pressed = QInputDialog.getInt(
            None,
            'Window size',
            'Input window size:',
            value=3,
            min=3,
            max=11,
            step=2
        )
        if ok_pressed and value < len(pk_list) and value % 2 == 1:

            self.view.enable_gui_element(False)  # lock gui
            self.model.smooth_model_both(pr, value, smooth_thickness=smooth_thickness, smooth_rho=smooth_rho)

            self.view.progressBar.setMinimum(0)
            self.view.progress_bar_initial_settings(0, len(pk_list) - 1)
            self.view.progressBar.setValue(0)

            for i in range(len(self.model.points)):
                if pr == self.model.points[i].pr:
                    self.model.points[i].direct_problem_calculate()
                    self.view.progress_bar_iteration()
                    QApplication.processEvents()

            self.view.progressBar.setValue(0)
            self.change_current_profile()
            self.view.enable_gui_element(True)  # unlock gui
            QApplication.processEvents()

    def smooth_model_thickness(self):
        self.smooth_model(smooth_thickness=True, smooth_rho=False)

    def smooth_model_rho(self):
        self.smooth_model(smooth_thickness=False, smooth_rho=True)

    def smooth_model_both(self):
        self.smooth_model(smooth_thickness=True, smooth_rho=True)

    def select_inverse_method(self):
        inverse_method = str(self.view.comboBoxSelectInverseMethods.currentText())
        self.MAX_ITERATIONS = int(self.view.spinBoxMaxIteration.value())
        for i in range(len(self.model.points)):
            if self.model.points[i] is not None:
                self.model.points[i].inverse_method = inverse_method
                self.model.points[i].max_iterations = self.MAX_ITERATIONS

    def export_to_zond_tem_1d(self):
        selected = self.view.show_select_profiles(self.model.get_profile_list())
        if selected:
            path_to_file = self.view.save_file_dialog('Select filename for save', '*.tdf')
            if path_to_file == '':
                return
            selected = list(map(int, selected))
            self.model.export_to_zond_tem_1d(path_to_file, selected)
            print(f'saved {path_to_file}')
            self.view.show_information('Export saved')

    def export_model_by_pr_to_text(self):
        selected = self.view.show_select_profiles(self.model.get_profile_list())
        if selected:
            path_to_file = self.view.save_file_dialog('Select filename for save', '*.dat')
            if path_to_file == '':
                return
            if path_to_file[-4:] != '.dat':
                path_to_file += '.dat'
            selected = list(map(int, selected))
            self.model.export_model_by_pr_to_text(path_to_file, selected, self.view.cross_section_reversed)
            self.view.show_information('Export saved')

    def export_current_view_map_to_text(self):
        if self.view.cube_data is None:
            return
        path_to_file = self.view.save_file_dialog('Select filename for save', '*.dat')
        if path_to_file == '':
            return
        if path_to_file[-4:] != '.dat':
            path_to_file += '.dat'

        z_value = self.view.verticalSliderMap.value()
        mask = self.view.cube_data[:, 2] == z_value
        slice_pts = self.view.cube_data[mask]
        if len(slice_pts) <= 10:
            print(f"Нет данных на глубине z = {z_value}")
            return
        xx = slice_pts[:, 0]
        yy = slice_pts[:, 1]
        rho = slice_pts[:, 3]
        path = path_to_file[0:-4] + f'_{z_value}.dat'
        with open(path, 'w') as f:
            f.write('X\tY\tRHO\tLOG_RHO\n')
            for x, y, z in zip(xx, yy, rho):
                f.write(f'{x}\t{y}\t{z}\t{np.log10(z)}\n')
            f.flush()

        path = path_to_file[0:-4] + '_points.dat'
        with open(path, 'w') as f:
            f.write('PR\tPK\tX\tY\tZ\n')
            need_points = [p for p in self.model.points if p.pr not in self.view.map_section_excluding_profiles]
            for p in need_points:
                temp = f'{p.pr}\t{p.pk}\t{p.coordinate.x}\t{p.coordinate.y}\t{p.coordinate.z}'
                f.write(temp + '\n')
            f.flush()
        print('saved points')
        self.view.show_information('Export saved')

    def cross_section_settings(self):
        res = self.view.cross_section_settings_view()
        if res:
            self.cross_section_plot()

    def map_section_settings(self):
        res = self.view.map_section_settings_view()
        if res:
            self.prepare_data_for_map_section()

    def select_filters(self):
        selected = self.view.show_select_filters(SurveyData.get_hankel_filter(), SurveyData.get_fourier_filter(), self.dlf_filters)
        if selected:
            self.dlf_filters = selected
            with open('filters', 'w', encoding='utf-8') as f:
                f.writelines(item + '\n' for item in self.dlf_filters)
            for p in self.model.points:
                p.hankel_func_arg = self.dlf_filters[0]
                p.fourier_func_arg = self.dlf_filters[1]

    def alpha_vci_value_dialog(self):
        if self.model.points is not None:
            val = self.model.points[0].alpha_coefficient_tikhonov
        else:
            val = 0.010
        value = self.view.show_alpha_coefficient_input(val)
        if value:
            self.model.set_alpha_coefficient(value)
            self.view.fill_vci_alpha_coefficient_menu(value)

    def srcpts_value_dialog(self):
        if self.model.points is not None:
            val = self.model.points[0].src_pts
        else:
            val = 7
        value = self.view.show_srcpts_input(val)
        if value:
            self.model.set_srcpts(value)
            self.view.fill_srcpts_menu(value)

    def auto_fitting_srcpts_process(self):
        if self.model.points is None:
            return
        default_value = 7
        reply = QMessageBox.question(self.view.centralwidget, 'Auto fitting srcpts',
                                     'Are you sure you want to automatically fit srcpts?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:

            selected_indexes = self.view.tablePickets.selectedIndexes()
            if len(selected_indexes) == 0:
                return
            selected_rows = list(set(index.row() for index in selected_indexes))

            self.view.progress_bar_initial_settings(0, len(selected_rows) - 1)

            pr = int(self.view.comboBoxSelectProfile.currentText())
            selected_pk = [-1] * len(selected_rows)
            for i, row in enumerate(selected_rows):
                picket = self.view.tablePickets.item(row, 0)
                selected_pk[i] = int(picket.text())

            selected_points = [None] * len(selected_pk)
            for i, pk in enumerate(selected_pk):
                selected_points[i] = self.model.get_point(pr, pk)

            # Многопроцессорная инверсия для нескольких точек
            num_processes = min(os.cpu_count() - 1, len(selected_points), self.MAX_PROCESS_LIMIT)
            print(f'Запуск {num_processes} процессов для обработки {len(selected_points)} точек')
            logging.info(f'Запуск {num_processes} процессов для обработки {len(selected_points)} точек')
            self.view.progress_bar_initial_settings(0, len(selected_points))

            with Pool(processes=num_processes) as pool:
                for i, res in enumerate(pool.imap_unordered(auto_fitting_srcpts_worker, selected_points)):
                    ind = self.model.get_index(res.pr, res.pk)
                    self.model.points[ind] = res
                    self.view.progress_bar_iteration()
            self.view.progressBar.setValue(0)
            print('Completed')

    def turn_off_dialog(self):
        if self.model.points is None:
            return
        current_value = self.model.current_point().turn_off
        value, ok_pressed = QInputDialog.getDouble(None, 'turn off', 'Input turn off value in ms:',
                                                   value=current_value, min=0.01, max=10,
                                                   decimals=2, step=0.01)
        if not ok_pressed:
            return
        self.set_turn_off(value)
        self.view.fill_turn_off_menu(value)
        print('Completed')

    def colormap_dialog(self):
        if self.model.points is None:
            return
        value, ok_pressed = QInputDialog.getText(None, 'Colormap', 'Input colormap name in cm:',
                                                 text=self.view.cross_section_color_palette)
        if not ok_pressed:
            return
        try:
            from matplotlib import cm
            cmap = cm.get_cmap(value)
            print(f'Палитра \'{value}\' существует')
            self.view.cross_section_color_palette = value
            self.cross_section_plot()
        except ValueError:
            QMessageBox.information(None, 'Info', f'{value} palette not found')


    def on_map_vertical_slider_moved(self):
        self.view.lblCurrentDepth.setText(f'{self.view.verticalSliderMap.value()}')
        self.map_plot()

    def tab_widget_page_change(self):
        if self.view.tab_widget.currentIndex() == 1:
            self.map_plot()
        elif self.view.tab_widget.currentIndex() == 2:
            self.pseudo_curves_plot()

    def pseudo_curves_plot(self):
        pr = int(self.view.comboBoxSelectProfile.currentText())
        if self.view.tab_widget.currentIndex() != 2:
            return
        if self.model.points is None or len(self.model.points) == 0:
            return
        need_point = [p for p in self.model.points if p.pr == pr]
        if not need_point or len(need_point) == 0:
            return

        self.view.pseudo_curvesPlot.ax.clear()

        need_point.sort(reverse=self.view.cross_section_reversed)
        x_start = need_point[0].coordinate.x
        y_start = need_point[0].coordinate.y
        distances = np.array(
            [np.sqrt((p.coordinate.x - x_start) ** 2 + (p.coordinate.y - y_start) ** 2) for p in need_point],
            dtype=np.float32)
        delta_dist = abs(np.mean(distances[1:]-distances[:-1]))
        for i, p in enumerate(need_point):
            obs = p.observed_curve[p.begin_time:p.end_time + 1]
            time = p.times[p.begin_time:p.end_time + 1]
            log_obs = np.log10(np.abs(obs*1000))
            log_time = np.log10(time * 1000)

            x = 10*delta_dist * log_obs + distances[i]

            #x = delta_dist * log_time + distances[i]
            self.view.pseudo_curvesPlot.ax.plot(x, log_time, 'b-')

        self.view.pseudo_curvesPlot.ax.grid()
        self.view.pseudo_curvesPlot.ax.invert_yaxis()
        self.view.pseudo_curvesPlot.ax.legend()
        self.view.pseudo_curvesPlot.ax.set_xlabel('Distance, m')
        self.view.pseudo_curvesPlot.ax.set_ylabel('Emf/I, mV/A')
        self.view.pseudo_curvesPlot.figure.tight_layout()
        self.view.pseudo_curvesPlot.canvas.draw_idle()

    def checkbox_table_picket_advance_column_view_check(self):
        self.view.table_picket_hidden_column()

    def checkbox_curves_plot_log_y_check(self):
        """
        Лог или симлог по оси Y на графиках
        :return:
        """
        self.view.curves_plot_log_y = self.view.check_box_curves_plot_log_y.isChecked()
        self.curves_plot()
