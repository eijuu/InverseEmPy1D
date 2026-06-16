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


import empymod
import numpy as np

from src import hampel_filter, utils
from src.utils import CoordinatePoint
from .model_environment import ModelEnvironment


class PointSounding:
    """
    Класс для точки зондирования БПЛА-МПП
    """
    point_b_rel: CoordinatePoint
    point_a_rel: CoordinatePoint
    coordinate_rel: CoordinatePoint
    end_time: int
    begin_time: int
    alpha_coefficient_tikhonov: float
    error_value: float
    pr: int
    pk: int
    coordinate: CoordinatePoint
    point_a: CoordinatePoint
    point_b: CoordinatePoint
    current_ab: float
    loop_area: float
    loop_height: float
    times: np.ndarray
    observed_curve: np.ndarray
    theory_curve: np.ndarray
    weights: np.ndarray
    model_environment: ModelEnvironment
    use_robust: bool
    ignore_negative_value: bool
    vci: bool

    hankel_func_arg: str
    fourier_func_arg: str

    max_iterations: int
    inverse_method: str

    src_pts: int
    turn_off: float

    def __init__(self):

        self.pr = 0
        self.pk = 0
        self.coordinate = CoordinatePoint()
        self.point_a = CoordinatePoint()
        self.point_b = CoordinatePoint()

        self.coordinate_rel = CoordinatePoint()
        self.point_a_rel = CoordinatePoint()
        self.point_b_rel = CoordinatePoint()

        self.current_ab = 0.0
        self.times = np.array([])
        self.observed_curve = np.array([])
        self.theory_curve = np.array([])
        self.weights = np.array([])
        self.error_value = 0.0
        self.model_environment = ModelEnvironment()

        self.alpha_coefficient_tikhonov = 0.1
        self.begin_time = 0
        self.end_time = 0
        self.loop_area = 0
        self.loop_height = 0
        self.use_robust = False
        self.ignore_negative_value = False
        self.vci = False
        self.src_pts = 7
        self.turn_off = 0.01  # ms

        self.hankel_func_arg = 'key_101_2009'
        self.fourier_func_arg = 'key_81_2009'

    def set_default_model(self):
        self.model_environment = ModelEnvironment()

    def insert_layer(self, index: int):
        self.model_environment.insert_layer(index)

    def delete_layer(self, index: int):
        self.model_environment.delete_layer(index)

    def create_vci_model(self, first_layer_h, progressive_coefficient, n_layers):
        h_layers = np.zeros(n_layers, dtype=np.float32)
        h_layers[0] = first_layer_h
        for i in range(1, n_layers):
            h_layers[i] = h_layers[i - 1] * progressive_coefficient

        self.model_environment.thickness_value = h_layers
        self.model_environment.thickness_value_max = h_layers + 0.75 * h_layers
        self.model_environment.thickness_value_min = h_layers - 0.75 * h_layers
        self.model_environment.thickness_value_fix = np.array([True] * n_layers)

        rho_layers = np.array([1000.0] * (n_layers + 1))
        self.model_environment.rho_value = np.log(rho_layers)
        self.model_environment.rho_value_max = np.log(rho_layers * 10)
        self.model_environment.rho_value_min = np.log(rho_layers / 100)
        self.model_environment.rho_value_fix = np.array([False] * (n_layers + 1))

    def direct_problem_calculate(self):
        self.direct_problem_wrapper(
            np.r_[self.model_environment.rho_value, self.model_environment.thickness_value])
        # self.error_value_calculate()

    def direct_problem_wrapper(self, params):
        n = len(params) // 2 + 1
        rho = params[:n]
        h = params[n:]
        depths = np.cumsum(h)
        self._direct_problem(rho, depths)

    def _direct_problem(self, _rho, _depth):
        _rho = np.exp(_rho)

        nodes = np.array([-10 - self.turn_off, -10, 0, self.turn_off]) * 1e-3
        amplitudes = np.array([0.0, 1.0, 1.0, 0.0])

        waveform = {'nodes': nodes, 'amplitudes': amplitudes, 'signal': -1}
        em = empymod.model.bipole(
            src=[self.point_a_rel.x, self.point_b_rel.x, self.point_a_rel.y, self.point_b_rel.y,
                 self.point_a_rel.z, self.point_b_rel.z],
            rec=[self.coordinate_rel.x, self.coordinate_rel.y, -self.loop_height, 0, 90],
            depth=np.r_[0, _depth],
            res=np.r_[2e14, _rho],
            freqtime=self.times,
            signal=waveform,  # Waveform
            mrec="b",  # Receiver: dB/dt
            strength=1,
            srcpts=self.src_pts,
            ftarg={'dlf': self.fourier_func_arg},
            htarg={'dlf': self.hankel_func_arg, 'pts_per_dec': -1},
            bandpass={'func': PointSounding.bandpass},
            verb=0
        )

        em = np.squeeze(em)
        em *= -self.loop_area
        self.theory_curve = np.array(em)

    def minimize_function(self, params):
        """
        Минимизация функции
        :param params: [rho_1, rho_2...rho_n, h_1, h_2...h_n-1]
        :return: значение невязки
        """
        self.direct_problem_wrapper(params)
        self.error_value_calculate()
        return self.error_value

    def minimize_function_vci(self, params, args):
        """
        минимизация функции vci
        :param params: [rho_1, rho_2...rho_n]
        :param args: (h_1, h_2...h_n-1)
        :return:
        """
        depths = np.cumsum(args)
        self._direct_problem(params, depths)
        self.error_value_calculate()
        delta_sum = 0.0
        for i in range(1, len(params)):
            delta_sum += (params[i] - params[i - 1]) ** 2

        r = self.error_value**2
        b = self.alpha_coefficient_tikhonov * delta_sum
        # print(f'{r:.5f}, {b:.5f}')
        self.error_value = np.sqrt(r + b)

        return self.error_value

    def error_value_calculate(self):
        thr = np.copy(self.theory_curve[self.begin_time: self.end_time + 1])
        obs = np.copy(self.observed_curve[self.begin_time: self.end_time + 1])

        # маска для точек равные 0
        mask_not_0 = obs != 0.0
        thr = thr[mask_not_0]
        obs = obs[mask_not_0]

        if self.ignore_negative_value:
            # игнорим все значения ниже 0
            mask_above_0 = obs > 0.0
            thr = thr[mask_above_0]
            obs = obs[mask_above_0]

        if len(obs) == 0:
            self.error_value = 999.0
            return

        relative_residuals = ((thr - obs) / obs) ** 2
        if self.use_robust:
            relative_residuals_filtered = hampel_filter.mu_estimate_smooth_cutted(relative_residuals, 5)
            error = np.sum(relative_residuals_filtered)
            self.error_value = np.sqrt(error / len(relative_residuals_filtered))
        else:
            error = np.sum(relative_residuals)
            self.error_value = np.sqrt(error / len(relative_residuals))

    def get_param_models(self):
        return np.r_[self.model_environment.rho_value, self.model_environment.thickness_value]

    def get_param_rho(self):
        return self.model_environment.rho_value

    def get_param_thickness(self):
        return self.model_environment.thickness_value

    def get_param_borders(self):
        return self.get_param_borders_rho() + self.get_param_borders_thickness()

    def get_param_borders_rho(self):
        rho_borders = []
        for m in zip(self.model_environment.rho_value_min, self.model_environment.rho_value_max):
            rho_borders.append(m)
        return rho_borders

    def get_param_borders_thickness(self):
        thickness_borders = []
        for m in zip(self.model_environment.thickness_value_min, self.model_environment.thickness_value_max):
            thickness_borders.append(m)
        return thickness_borders

    def set_model_value(self, params):
        n = len(params) // 2 + 1
        self.model_environment.rho_value = params[:n]
        self.model_environment.thickness_value = params[n:]

    def set_model_borders_value(self, rho_list_min, rho_list_max, h_list_min, h_list_max):
        self.model_environment.rho_value_min = rho_list_min
        self.model_environment.rho_value_max = rho_list_max
        self.model_environment.thickness_value_min = h_list_min
        self.model_environment.thickness_value_max = h_list_max

    def get_str_model(self):
        n_layers = len(
            self.model_environment.thickness_value)  # Используем количество слоев по h, т.к их на 1 меньше, чем rho
        s = ''
        for i in range(n_layers):
            s += str(self.pr) + '\t'
            s += str(self.pk) + '\t'
            s += str(i + 1) + '\t'
            s += f'{np.exp(self.model_environment.rho_value[i]):.2f}' + '\t'
            s += f'{np.exp(self.model_environment.rho_value_min[i]):.2f}' + '\t'
            s += f'{np.exp(self.model_environment.rho_value_max[i]):.2f}' + '\t'
            s += str(self.model_environment.rho_value_fix[i]) + '\t'
            s += f'{self.model_environment.thickness_value[i]:.2f}' + '\t'
            s += f'{self.model_environment.thickness_value_min[i]:.2f}' + '\t'
            s += f'{self.model_environment.thickness_value_max[i]:.2f}' + '\t'
            s += str(self.model_environment.thickness_value_fix[i]) + '\n'

        # для последних слоев
        s += str(self.pr) + '\t'
        s += str(self.pk) + '\t'
        s += str(n_layers + 1) + '\t'
        s += f'{np.exp(self.model_environment.rho_value[-1]):.2f}' + '\t'
        s += f'{np.exp(self.model_environment.rho_value_min[-1]):.2f}' + '\t'
        s += f'{np.exp(self.model_environment.rho_value_max[-1]):.2f}' + '\t'
        s += str(self.model_environment.rho_value_fix[-1]) + '\t'
        s += str(0) + '\t'
        s += str(0) + '\t'
        s += str(0) + '\t'
        s += str(0)
        return s

    def set_begin_end_index_times(self, begin: int, end: int):
        self.begin_time = begin
        self.end_time = end

    def set_begin_index_times(self, begin: int):
        if 0 <= begin < len(self.times) and begin < self.end_time:
            self.begin_time = begin

    def set_end_index_times(self, end: int):
        if 1 <= end < len(self.times) and end > self.begin_time:
            self.end_time = end

    def auto_fitting_srcpts(self, default_value=11, err=0.05):
        max_srcpts = 50
        self.src_pts = max_srcpts
        self.direct_problem_calculate()
        p0 = np.copy(self.theory_curve)
        for pts in range(3, max_srcpts):
            self.src_pts = pts
            self.direct_problem_calculate()
            p1 = np.copy(self.theory_curve)
            if utils.rmsre(p0, p1) < err:
                print(f'Pr {self.pr}, Pk {self.pk} auto fitting srcpts: {self.src_pts}')
                break
        else:
            self.src_pts = default_value
            print(f'Pr {self.pr}, Pk {self.pk} auto fitting srcpts not completed. Default srcpts {default_value}')

    def __lt__(self, other):
        r1 = self.pr * 10000 + self.pk
        r2 = other.pr * 10000 + other.pk
        return r1 < r2

    @staticmethod
    def bandpass(inp, p_dict):
        cut_off_freq = 1e6
        h = (1 + 1j * p_dict['freq'] / cut_off_freq) ** -1
        h *= (1 + 1j * p_dict['freq'] / 3e5) ** -1
        p_dict['EM'] *= h[:, None]

    def get_point_str_line(self):
        """
        Вернуть строку с данными для сохранения в файл
        :return:
        """
        data = [self.pr, self.pk, self.coordinate.x, self.coordinate.y, self.coordinate.z,
                self.point_a.x, self.point_a.y, self.point_b.x, self.point_b.y, self.current_ab,
                self.loop_area, self.loop_height, self.src_pts, self.begin_time, self.end_time]
        data.extend(self.observed_curve)
        data.extend(self.weights)
        s = [str(_) for _ in data]
        return '\t'.join(s)
