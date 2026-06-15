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


import json
import zipfile
from datetime import datetime

import numpy as np

from src import hampel_filter
from src.utils import CoordinatePoint
from .point_sounding import PointSounding


class SurveyData:
    EXPECTED_HEADERS = {'profile': 'pr', 'picket': 'pk',
                        'qx': 'x', 'qy': 'y', 'relief': 'z',
                        'ax': 'ax', 'ay': 'ay', 'bx': 'bx', 'by': 'by',
                        'current': 'i_a', 'observed': '1_du', 'weight': 'w_du',
                        'loop_area': 'loop_area', 'loop_height': 'loop_height',
                        'source_pts': 'src_pts', 'begin_time': 'begin_time', 'end_time': 'end_time'
                        }

    points: list[PointSounding]
    current_index: int

    def __init__(self):
        self.times_str = None
        self.observed_data_str = None
        self.points = []
        self.current_index = -1

    @staticmethod
    def __load_emp_project(_path):
        """
        Загружает файлы из проекта *.emp
        :param _path:
        :return:
        """
        try:
            with zipfile.ZipFile(_path, 'r') as zip_file:
                required_files = ('observed_data.txt', 'times.txt')
                for file in required_files:
                    if file not in zip_file.namelist():
                        raise FileNotFoundError(f'File {file} is not found in this project')

                # чтение файлов
                observed_data = zip_file.read('observed_data.txt').decode('utf-8')
                times = zip_file.read('times.txt').decode('utf-8')
                if 'models.txt' in zip_file.namelist():
                    models = zip_file.read('models.txt').decode('utf-8')
                else:
                    models = None
                if 'project_settings.txt' in zip_file.namelist():
                    project_settings = zip_file.read('project_settings.txt').decode('utf-8')
                else:
                    project_settings = None
            return observed_data, times, models, project_settings
        except zipfile.BadZipfile:
            raise ValueError('Incorrect file')
        except Exception as e:
            raise Exception(f'Error file: {str(e)}')

    def load_data(self, _path):
        try:
            self.observed_data_str, self.times_str, models, project_settings = SurveyData.__load_emp_project(_path)
            self.__load_observed_data(self.observed_data_str.splitlines())
            self.__load_times(self.times_str.splitlines())
            if models is not None:
                self.__load_models(models.splitlines())
            else:
                for p in self.points:
                    p.set_default_model()
                    p.set_begin_end_index_times(0, len(self.times_str.splitlines()) - 1)

            if project_settings is not None:
                self.__load_project_settings(project_settings)

        except Exception as e:
            print(f'Error {str(e)}')

    def __load_observed_data(self, observed_data):
        """
        Наблюденные кривые должны быть в вольт/ампер
        :param observed_data:
        :return:
        """
        self.points: list[PointSounding] = []
        try:
            expected_hdr = self.EXPECTED_HEADERS

            # читаем заголовки
            headers = observed_data[0].lower().split('\t')

            # Создаем словарь для быстрого доступа к индексам колонок
            header_ind = {header: idx for idx, header in enumerate(headers)}

            # заполняем заголовки 1_dU.1 - 1_dU.n отдельно
            du_headers = []
            for header in headers:
                if header.startswith(expected_hdr['observed']):
                    du_headers.append(header)

            # заголовки весов если есть
            w_headers = []
            for header in headers:
                if header.startswith(expected_hdr['weight']):
                    w_headers.append(header)

            # заголовки, которых сейчас может не быть (ver. 1.0.0.)
            has_coefficient_weight = len(du_headers) == len(w_headers)
            has_loop_area = expected_hdr['loop_area'] in headers
            has_loop_height = expected_hdr['loop_height'] in headers
            has_source_pts = expected_hdr['source_pts'] in headers
            has_begin_end_time = expected_hdr['begin_time'] in headers

            del observed_data[0]
            # Читаем данные
            for line in observed_data:

                line = line.strip()
                if not line:
                    continue

                line_data = line.split('\t')

                # Создаем экземпляр PointSounding
                ps = PointSounding()

                # Заполняем основные атрибуты
                ps.pr = int(line_data[header_ind[expected_hdr['profile']]])
                if '_C' in line_data[header_ind[expected_hdr['picket']]]:  # пропуск контрольных
                    continue
                ps.pk = int(line_data[header_ind[expected_hdr['picket']]])

                # Создаем координатные точки
                x = float(line_data[header_ind[expected_hdr['qx']]])
                y = float(line_data[header_ind[expected_hdr['qy']]])
                z = float(line_data[header_ind[expected_hdr['relief']]])
                ps.coordinate = CoordinatePoint(x, y, z)

                # Точка A (Ax, Ay)
                ax = float(line_data[header_ind[expected_hdr['ax']]])
                ay = float(line_data[header_ind[expected_hdr['ay']]])
                ps.point_a = CoordinatePoint(ax, ay)

                # Точка B (Bx, By)
                bx = float(line_data[header_ind[expected_hdr['bx']]])
                by = float(line_data[header_ind[expected_hdr['by']]])
                ps.point_b = CoordinatePoint(bx, by)

                # координаты сдвинутые на A
                ps.coordinate_rel = CoordinatePoint(x - ax, y - ay, z)
                ps.point_a_rel = CoordinatePoint(0.0, 0.0, 0.0)
                ps.point_b_rel = CoordinatePoint(bx - ax, by - ay, 0.0)

                # Ток
                ps.current_ab = float(line_data[header_ind[expected_hdr['current']]])

                # Загружаем observed_curve из всех найденных колонок 1_dU
                observed_curve = np.array(list(map(lambda h: line_data[header_ind[h]], du_headers)), dtype=np.float64)
                ps.observed_curve = np.squeeze(observed_curve)

                # Задание стандартной модели
                ps.set_default_model()

                # весовые коэффициенты
                if has_coefficient_weight:
                    weights = np.array(list(map(lambda h: line_data[header_ind[h]], w_headers)), dtype=np.float64)
                    ps.weights = np.squeeze(weights)
                else:
                    ps.weights = np.array([1.0] * len(observed_curve), dtype=np.float64)

                # площадь и высота датчика над поверхностью
                ps.loop_area = float(line_data[header_ind[expected_hdr['loop_area']]]) if has_loop_area else 2500.0
                ps.loop_height = float(line_data[header_ind[expected_hdr['loop_height']]]) if has_loop_height else 40.0
                # кол-во ГЭД
                ps.src_pts = int(line_data[header_ind[expected_hdr['source_pts']]]) if has_source_pts else 7
                # обрезка времен
                if has_begin_end_time:
                    ps.begin_time = int(line_data[header_ind[expected_hdr['begin_time']]])
                    ps.end_time = int(line_data[header_ind[expected_hdr['end_time']]])
                else:
                    ps.begin_time = 0
                    ps.end_time = len(observed_curve) - 1

                # Добавляем в список points
                self.points.append(ps)

            print(f'Загружено {len(self.points)} точек')
            return 1
        except FileNotFoundError:
            return 0
        except Exception as e:
            return e

    def __load_times(self, times):
        times = [t.strip() for t in times]
        times = np.array(times, dtype=np.float32)
        if self.points is None or len(self.points) == 0:
            return
        if len(times) == len(self.points[0].observed_curve):
            for point in self.points:
                point.times = times
            print(f'Времена загружены. Кол-во времен {len(times)}')
        else:
            print(f'Времена не загружены. Кол-во времен {len(times)}, а кол-во точек на кривой '
                  f'{len(self.points[0].observed_curve)}')

    def __load_project_settings(self, project_settings):
        data = json.loads(project_settings)

        vci = data.get('vci', False)
        use_robust = data.get('use_robust', False)
        ignore_negative_value = data.get('ignore_negative_value', False)
        alpha_coefficient = data.get('alpha_coefficient', 0.1)

        self.set_vci_flag(vci)
        self.set_use_robust_flag(use_robust)
        self.set_ignore_negative_value_flag(ignore_negative_value)
        self.set_alpha_coefficient(alpha_coefficient)

    def save_data(self, _path):
        """
        Сохранить данные в файл
        :param _path:
        :return:
        """
        if self.points is None or len(self.points) == 0:
            return

        # observed data
        eh = self.EXPECTED_HEADERS
        du_header = [eh['observed'] + f'.{i + 1}' for i in range(len(self.points[0].observed_curve))]
        w_header = [eh['weight'] + f'.{i + 1}' for i in range(len(self.points[0].weights))]
        header = [eh['profile'], eh['picket'], eh['qx'], eh['qy'], eh['relief'],
                  eh['ax'], eh['ay'], eh['bx'], eh['by'], eh['current'],
                  eh['loop_area'], eh['loop_height'], eh['source_pts'],
                  eh['begin_time'], eh['end_time']
                  ]
        header.extend(du_header)
        header.extend(w_header)
        observed_str = '\t'.join(header) + '\n'
        for point in self.points:
            observed_str += point.get_point_str_line() + '\n'

        # environment
        environment_str = '\t'.join(['pr', 'pk', 'n_layer',
                                     'rho', 'rho_min', 'rho_max', 'rho_fix',
                                     'h', 'h_min', 'h_max', 'h_fix']) + '\n'
        for point in self.points:
            s = point.get_str_model()
            environment_str += s + '\n'

        try:
            with zipfile.ZipFile(_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Добавляем файлы в архив
                zip_file.writestr('observed_data.txt', observed_str)
                zip_file.writestr('times.txt', self.times_str)
                zip_file.writestr('models.txt', environment_str)
                zip_file.writestr('project_settings.txt', self.create_json_project_settings())
                meta_info = f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nFile count: 3"
                zip_file.writestr('meta.info', meta_info)
            print(f"Создан .emp файл: {_path}")

        except Exception as e:
            print(f"Ошибка при создании .emp файла: {e}")

    def create_json_project_settings(self) -> str | None:
        if self.points is None or len(self.points) == 0:
            return None
        data = {
            'vci': self.points[0].vci,
            'use_robust': self.points[0].use_robust,
            'ignore_negative_value': self.points[0].ignore_negative_value,
            'alpha_coefficient': self.points[0].alpha_coefficient_tikhonov
        }
        json_string = json.dumps(data, indent=4)
        return json_string

    def __load_models(self, models):
        if self.points is None or len(self.points) == 0:
            return

        del models[0]  # Удалим заголовки

        counter = 0
        for index in range(len(self.points)):
            rho = []
            rho_min = []
            rho_max = []
            rho_fix = []
            h = []
            h_min = []
            h_max = []
            h_fix = []

            for i in range(counter, len(models)):
                line = models[i].strip().split('\t')
                pr = int(line[0])
                pk = int(line[1])
                if pr == self.points[index].pr and pk == self.points[index].pk:
                    rho.append(float(line[3]))
                    rho_min.append(float(line[4]))
                    rho_max.append(float(line[5]))
                    rho_fix.append(line[6] == 'True')
                    h_value = float(line[7])

                    if h_value != 0.0:
                        h.append(h_value)
                        h_min.append(float(line[8]))
                        h_max.append(float(line[9]))
                        h_fix.append(line[10] == 'True')
                    else:
                        counter = i - 1
                        break

            self.points[index].model_environment.rho_value = np.log(np.array(rho, dtype=np.float32))
            self.points[index].model_environment.rho_value_min = np.log(np.array(rho_min, dtype=np.float32))
            self.points[index].model_environment.rho_value_max = np.log(np.array(rho_max, dtype=np.float32))
            self.points[index].model_environment.rho_value_fix = np.array(rho_fix, dtype=np.bool)
            self.points[index].model_environment.thickness_value = np.array(h, dtype=np.float32)
            self.points[index].model_environment.thickness_value_min = np.array(h_min, dtype=np.float32)
            self.points[index].model_environment.thickness_value_max = np.array(h_max, dtype=np.float32)
            self.points[index].model_environment.thickness_value_fix = np.array(h_fix, dtype=np.bool)

    def set_begin_end_index_times_for_all(self, begin: int, end: int):
        if self.points is None:
            return
        for i in range(len(self.points)):
            self.points[i].set_begin_end_index_times(begin, end)

    def set_use_robust_flag(self, flag: bool):
        if self.points is None:
            return
        for i in range(len(self.points)):
            self.points[i].use_robust = flag

    def set_ignore_negative_value_flag(self, flag: bool):
        if self.points is None:
            return
        for i in range(len(self.points)):
            self.points[i].ignore_negative_value = flag

    def set_vci_flag(self, flag: bool):
        if self.points is None:
            return
        for i in range(len(self.points)):
            for j in range(len(self.points[i].model_environment.thickness_value_fix)):
                self.points[i].model_environment.thickness_value_fix[j] = flag
                self.points[i].vci = flag

    def set_alpha_coefficient(self, alpha_coefficient):
        for p in self.points:
            p.alpha_coefficient_tikhonov = alpha_coefficient

    def get_profile_list(self):
        profile_list = []
        for p in self.points:
            profile_list.append(p.pr)

        profile_set = set(profile_list)
        profile_list = list(profile_set)
        profile_list.sort()
        profile_list = [str(p) for p in profile_list]
        return profile_list

    def get_picket_list(self, profile: int) -> list[int]:
        pickets = []
        for p in self.points:
            if profile == p.pr:
                pickets.append(p.pk)
        pickets_set = set(pickets)
        pickets = list(pickets_set)
        pickets.sort()
        return pickets

    def get_picket_curves(self, profile: int, picket: int):
        for p in self.points:
            if profile == p.pr and picket == p.pk:
                return p.times, p.observed_curve, p.theory_curve
        return None

    def get_point(self, profile: int, picket: int) -> PointSounding | None:
        for p in self.points:
            if profile == p.pr and picket == p.pk:
                return p
        return None

    def get_index(self, profile: int, picket: int) -> int:
        for i, p in enumerate(self.points):
            if profile == p.pr and picket == p.pk:
                return i
        return -1

    def get_coordinates_list(self) -> list[tuple[float]] | None:
        if self.points is None or len(self.points) == 0:
            return None
        coordinates = [tuple([p.coordinate.x, p.coordinate.y, p.coordinate.z]) for p in self.points]
        return coordinates

    def get_ab_coordinate_list(self):
        if self.points is None or len(self.points) == 0:
            return None
        ab_coordinate = [tuple([p.point_a.get_tuple(), p.point_b.get_tuple()]) for p in self.points]
        ab = list(set(ab_coordinate))
        return ab

    def get_pr_pk_list(self):
        if self.points is None or len(self.points) == 0:
            return None
        res = [tuple([p.pr, p.pk]) for p in self.points]
        return res

    def select_current_index(self, profile: int, picket: int):
        for i, p in enumerate(self.points):
            if profile == p.pr and picket == p.pk:
                self.current_index = i
                break

    def current_point(self) -> PointSounding | None:
        if self.current_index == -1:
            return None
        return self.points[self.current_index]

    def set_height_fly(self, height: float):
        for p in self.points:
            p.loop_height = height

    def set_loop_area(self, area: float):
        for p in self.points:
            p.loop_area = area

    def get_data_for_cross_section(self, need_profile: int, _reversed: bool = False):
        """
        Подготовка и получение данных для построения разреза
        :param _reversed: развернутый профиль
        :param need_profile: нужный профиль
        :return:
        """
        points: list[PointSounding] = []
        for p in self.points:
            if need_profile == p.pr:
                points.append(p)
        if len(points) == 0:
            return None

        points.sort(reverse=_reversed)

        # дистанции
        x_start = points[0].coordinate.x
        y_start = points[0].coordinate.y
        distances = np.array(
            [np.sqrt((p.coordinate.x - x_start) ** 2 + (p.coordinate.y - y_start) ** 2) for p in points],
            dtype=np.float32)
        pickets = [p.pk for p in points]
        num_distances = len(distances)

        # считаем глубины
        max_num_layer = max([len(p.model_environment.thickness_value) for p in points])
        depths = [np.cumsum(p.model_environment.thickness_value) for p in points]
        depths = np.array([np.pad(d, (0, max_num_layer - len(d)), 'edge') for d in depths], dtype=np.float16)

        relief = np.array([p.coordinate.z for p in points])
        delta_relief = relief.max() - relief.min()
        max_depth = depths.max() + delta_relief

        depths_relative_by_every_meter = np.arange(1, int(max_depth))
        depths_relative_by_every_meter_2d = np.tile(depths_relative_by_every_meter, (num_distances, 1))

        # 2d массив для УЭС
        rho_by_every_meter_2d = np.zeros_like(depths_relative_by_every_meter_2d, dtype=np.float32)

        for i in range(len(depths_relative_by_every_meter_2d)):
            k = 0
            thickness: np.float16
            for ih, thickness in enumerate(points[i].model_environment.thickness_value):
                for j in range(int(thickness)):
                    rho_by_every_meter_2d[i, k] = points[i].model_environment.rho_value[ih]
                    k += 1

            # заполняем все остатки значениями фундамента
            while k < len(depths_relative_by_every_meter_2d[i]):
                rho_by_every_meter_2d[i, k] = points[i].model_environment.rho_value[-1]
                k += 1

        X, Y = np.meshgrid(distances, depths_relative_by_every_meter, indexing='ij')
        Z = relief[:, np.newaxis] - Y

        errors = np.array([p.error_value for p in points])

        return (X, Z, rho_by_every_meter_2d), (distances, errors, pickets)

    def smooth_model_both(self, need_profile: int, window_size=3, smooth_thickness=True, smooth_rho=False):
        if smooth_rho + smooth_thickness == 0:
            return
        points: list[PointSounding] = []
        for i, p in enumerate(self.points):
            if need_profile == p.pr:
                points.append(p)
        points.sort()

        # сглаживание по слоям rho
        if smooth_rho:
            n_layer = len(points[0].model_environment.rho_value)
            for n in range(n_layer):
                rho = np.zeros(len(points), dtype=np.float32)
                for i, p in enumerate(points):
                    rho[i] = p.model_environment.rho_value[n]
                rho = np.exp(rho)  # log(rho) -> rho
                rho_smooth = hampel_filter.mu_estimate_smooth(rho, window_size)
                rho_smooth = np.log(rho_smooth)  # rho -> log(rho)
                for i, p in enumerate(points):
                    p.model_environment.rho_value[n] = rho_smooth[i]
            # применяем изменения по точкам
            for i, p in enumerate(self.points):
                for ii, pp in enumerate(points):
                    if p.pr == pp.pr and p.pk == pp.pk:
                        self.points[i].model_environment.rho_value = pp.model_environment.rho_value
                        break

        # сглаживание по слоям thickness
        if smooth_thickness:
            n_layer = len(points[0].model_environment.thickness_value)
            for n in range(n_layer):
                thickness = np.zeros(len(points), dtype=np.float32)
                for i, p in enumerate(points):
                    thickness[i] = p.model_environment.thickness_value[n]
                thickness_smooth = hampel_filter.mu_estimate_smooth(thickness, window_size)
                for i, p in enumerate(points):
                    p.model_environment.thickness_value[n] = thickness_smooth[i]
            # применяем изменения по точкам
            for i, p in enumerate(self.points):
                for ii, pp in enumerate(points):
                    if p.pr == pp.pr and p.pk == pp.pk:
                        self.points[i].model_environment.thickness_value = pp.model_environment.thickness_value
                        break

    def get_cube_data_for_map(self, is_relative_depth: bool, excluding_profiles: list) -> np.ndarray | None:
        """
        Получить куб из данных x, y, z, rho
        :param is_relative_depth:
        :param excluding_profiles:
        :return:
        """
        if self.points is None or len(self.points) == 0:
            return None
        need_points = [p for p in self.points if p.pr not in excluding_profiles]
        if not need_points:
            return None

        blocks = []
        # сначала находим самую глубокую модель в точках
        max_depth = 0
        for p in need_points:
            boundaries = np.cumsum(p.model_environment.thickness_value)
            if max_depth < boundaries[-1]:
                max_depth = boundaries[-1]
        # теперь сбор данных
        for p in need_points:
            env = p.model_environment
            rho_lin = np.exp(env.rho_value)
            boundaries = np.cumsum(env.thickness_value)

            # глубины через 1 метр
            sample_depths = np.arange(0, max_depth + 1, 1.0)
            layer_idx = np.searchsorted(boundaries, sample_depths, side='right')
            layer_idx[layer_idx == len(rho_lin)] = len(rho_lin) - 1

            # сопротивления для всех глубин
            resistivity = rho_lin[layer_idx]

            # Z-координата
            if is_relative_depth:
                z_vals = sample_depths
            else:
                z_vals = int(p.coordinate.z) - sample_depths

            # Формируем блок данных для текущего зондирования
            n = len(sample_depths)
            block = np.empty((n, 4), dtype=np.float32)
            block[:, 0] = p.coordinate.x
            block[:, 1] = p.coordinate.y
            block[:, 2] = z_vals
            block[:, 3] = resistivity

            blocks.append(block)

        if not blocks:
            return None

        return np.vstack(blocks)

    def export_to_zond_tem_1d(self, _path_to_save: str, _profiles_for_export: list[int]):
        """
        Выгрузка в ZondTEM1D
        :param _path_to_save: путь куда сохранить файл
        :param _profiles_for_export: список экспортируемых профилей
        :return:
        """
        if self.points is None or len(self.points) == 0:
            return
        count = 0
        for i, p in enumerate(self.points):
            if p.pr in _profiles_for_export:
                count += 1
        with open(_path_to_save, 'w') as save_file:
            save_file.write('zondtem3.0\n')
            save_file.write(f'{count}\n')  # !number of sounging

            center_ax = (self.points[0].point_a.x + self.points[0].point_b.x) / 2
            center_ay = (self.points[0].point_a.y + self.points[0].point_b.y) / 2
            n_count = 0
            for i, p in enumerate(self.points):
                if p.pr not in _profiles_for_export:
                    continue
                """
                В качестве начала координат при описании геометрии источников и приемников 
                рекомендуется использовать центр источника.
                """

                x = p.coordinate.x - center_ax
                y = p.coordinate.y - center_ay
                ax = p.point_a.x - center_ax
                ay = p.point_a.y - center_ay
                bx = p.point_b.x - center_ax
                by = p.point_b.y - center_ay

                s = f'title: {p.pr}_{p.pk}'
                save_file.write(s + '\n')

                s = f'{x} {y} {p.coordinate.z}'
                save_file.write(s + '\n')

                """
                0 - вертикальный магнитный диполь (VMD), 1 – горизонтальный электрический диполь (HED), 
                2 - линия конечной длины (Line), 3 – петля (Loop), 4 - горизонтальный магнитный диполь (HMD).
                """
                s = 2
                save_file.write(str(s) + '\n')

                # координаты центра источника X Y Z.
                s = f'{0} {0} 0'
                save_file.write(s + '\n')

                # описание узлов источника. (!XY nodes of loop/line or center XY and dircos of dipoles)
                s = f'{ax} {ay} {bx} {by}'
                save_file.write(s + '\n')

                # количество приемников
                s = 1
                save_file.write(str(s) + '\n')

                """
                0 - электрическая антенна (горизонтальная составляющая), 
                1 - электрическая линия конечной длины , 
                2 – петля (вертикальная составляющая), 
                3 - магнитная антенна (вертикальная составляющая), 
                4 - магнитная антенна (горизонтальная составляющая).
                """
                s = 2
                save_file.write(str(s) + '\n')

                # координаты центра приемника X Y Z.
                # Важно ввести только третью координату – высоту приемника над поверхностью земли
                s = f'{x} {y} {p.loop_height}'
                # s = f'{x} {y} {0}'
                save_file.write(s + '\n')

                # описание узлов приемника
                # петля: 8 чисел, координаты узлов петли X1 Y1 X2 Y2 X3 Y3 X4 Y4.
                half_side = np.sqrt(abs(p.loop_area)) / 2
                s = (f'{x - half_side:.2f} {y - half_side:.2f} '
                     f'{x + half_side:.2f} {y - half_side:.2f} '
                     f'{x + half_side:.2f} {y + half_side:.2f} '
                     f'{x - half_side:.2f} {y + half_side:.2f}')
                save_file.write(s + '\n')

                # число временных режимов (SWEEP). Обычно 1.
                s = 1
                save_file.write(str(s) + '\n')

                """
                тип импульса. 0 – ступенька, 1 – прямоугольный импульс конечной длины, 2 – импульс произвольной формы
                """
                s = 1
                save_file.write(str(s) + '\n')

                """
                последовательность параметров временного режима.
                Для типов импульсов 0 и 1 последовательность параметров выглядит следующим
                образом (4 числа): длина импульса, длина паузы, продолжительность переднего
                фронта импульса, продолжительность заднего фронта импульса (все величины в
                секундах).
                """
                s = f'{0.01} {0.01} {0} {0}'
                save_file.write(s + '\n')

                # количество измерений (временных задержек) для данного приемника
                s = f'{len(p.times)}'
                save_file.write(s + '\n')

                """
                шапка, указывающая программе, какой тип данных, в каком столбце находится. 
                Обычно, строка выглядит следующим образом.
                # t(sec) sweep U(uV) weight
                """
                save_file.write('# t(sec) sweep U(uV) weight' + '\n')
                for j, (t, v) in enumerate(zip(p.times, p.observed_curve)):

                    #uv = v * 10e6 / p.loop_area  # вольты -> микровольты -> микровольты / площадь петли
                    # я не знаю почему
                    uv = v * 10e5
                    weight = 1 if p.begin_time <= j <= p.end_time else 0
                    s = f'{j + 1} {t} {1} {uv} {weight}'
                    save_file.write(s + '\n')

                n_count += 1
                save_file.flush()

        print(_path_to_save)

    @staticmethod
    def get_hankel_filter():
        return [
            'anderson_801_1982',
            #'gupt_61_1997',
            #'gupt_120_1997',
            #'gupt_47_1997',
            #'gupt_140_1997',
            'kong_61_2007b',
            'kong_121_2007',
            'kong_241_2007',
            'key_101_2009',
            'key_201_2009',
            'key_401_2009',
            'key_51_2012',
            'key_101_2012',
            'key_201_2012',
            'wer_201_2018',
            'wer_2001_2018'
        ]

    @staticmethod
    def get_fourier_filter():
        return [
            'key_81_2009',
            'key_241_2009',
            'key_601_2009',
            'key_101_2012',
            'key_201_2012',
            #'grayver_50_2021',
            'wer_201_2018',
            'wer_101_2020a',
            'wer_101_2020b'
        ]

    def set_srcpts(self, scrpts):
        if self.points is not None:
            for p in self.points:
                p.src_pts = scrpts

    def export_model_by_pr_to_text(self, _path_to_save: str, _profiles_for_export: list[int], _reversed=False):
        """
        Выгрузка в txt формате
        :param _path_to_save:
        :param _profiles_for_export:
        :param _reversed:
        :return:
        """
        if self.points is None or len(self.points) == 0:
            return

        need_points = [p for p in self.points if p.pr in _profiles_for_export]
        if not need_points:
            return

        # сначала находим самую глубокую модель в точках
        max_depth = 0
        for p in need_points:
            boundaries = np.cumsum(p.model_environment.thickness_value)
            if max_depth < boundaries[-1]:
                max_depth = boundaries[-1]

        s_all = ''
        header = '\t'.join(['PR', 'PK', 'X', 'Y', 'Z', 'DIST', 'H', 'H0', 'RHO', 'LOG_RHO'])

        # теперь отдельно по профилям
        for profile in _profiles_for_export:
            need_points = [p for p in self.points if p.pr == profile]
            need_points.sort(reverse=_reversed)

            # для дистанции
            x_start = need_points[0].coordinate.x
            y_start = need_points[0].coordinate.y

            path_for_profile = _path_to_save[0:-4] + '_' + str(profile) + '.dat'
            with open(path_for_profile, 'w') as save_file:
                save_file.write(header + '\n')
                # по точкам
                for p in need_points:
                    env = p.model_environment
                    rho_lin = np.exp(env.rho_value)
                    boundaries = np.cumsum(env.thickness_value)

                    # глубины через 1 метр
                    sample_depths = np.arange(0, max_depth + 1, 1.0)
                    layer_idx = np.searchsorted(boundaries, sample_depths, side='right')
                    layer_idx[layer_idx == len(rho_lin)] = len(rho_lin) - 1

                    # сопротивления для всех глубин
                    resistivity = rho_lin[layer_idx]
                    resistivity_log = np.log10(resistivity)

                    absolute_h = int(p.coordinate.z) - sample_depths

                    for h0, h, rho, log_rho in zip(sample_depths, absolute_h, resistivity, resistivity_log):
                        dist = np.sqrt((p.coordinate.x - x_start) ** 2 + (p.coordinate.y - y_start) ** 2)
                        # ['PR', 'PK', 'X', 'Y', 'Z', 'DIST', 'H', 'H0', 'RHO', 'LOG_RHO']
                        temp = f'{p.pr}\t{p.pk}\t{p.coordinate.x}\t{p.coordinate.y}\t{p.coordinate.z}\t{dist:.2f}\t{h}\t{h0}\t{rho}\t{log_rho}'
                        s_all += temp + '\n'
                        save_file.write(temp + '\n')
                save_file.flush()
                print(f'saved {path_for_profile}')

            # сохраняем рельеф для разрезов
            path_for_profile = _path_to_save[0:-4] + '_' + str(profile) + '_relief.txt'
            with open(path_for_profile, 'w') as save_file:
                save_file.write('\t'.join(['DIST', 'Z', 'PK', 'X', 'Y']) + '\n')
                for p in need_points:
                    dist = np.sqrt((p.coordinate.x - x_start) ** 2 + (p.coordinate.y - y_start) ** 2)
                    temp = f'{dist}\t{p.coordinate.z}\t{p.pk}\t{p.coordinate.x}\t{p.coordinate.y}'
                    save_file.write(temp + '\n')
                save_file.flush()

        with open(_path_to_save, 'w') as save_file:
            save_file.write(header + '\n')
            save_file.write(s_all)
            save_file.flush()
            print(f'saved {_path_to_save}')








