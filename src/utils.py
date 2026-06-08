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


import math
import numpy as np


class CoordinatePoint:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def get_tuple(self) -> tuple:
        return self.x, self.y, self.z

    def __str__(self):
        return f'{self.x}, {self.y}, {self.z}'


def separate_curve_pos_neg(_times, _curve):
    positive_mask = _curve > 0
    negative_mask = _curve < 0
    times_for_positive = _times[positive_mask]
    observed_curve_positive = _curve[positive_mask]

    times_for_negative = _times[negative_mask]
    observed_curve_negative = _curve[negative_mask]
    return times_for_positive, observed_curve_positive, times_for_negative, observed_curve_negative


def try_str_to_float(value) -> float | None:
    try:
        res = float(value)
        return res
    except (ValueError, TypeError):
        return None


def rmsre(o, t):
    if len(o) == len(t):
        error = np.sum(((t - o) / o) ** 2)
        return np.sqrt(error / len(o))
    else:
        return 123456789


def array_to_string_array(arr) -> list:
    return [str(_) for _ in arr]


def translate_and_turn_coordinate(a: CoordinatePoint, b: CoordinatePoint, m: CoordinatePoint) -> tuple[CoordinatePoint, CoordinatePoint, CoordinatePoint]:
    """
    Преобразует координаты точек A, B, M в новую систему:
    - начало координат переносится в точку A
    - ось X направляется вдоль вектора AB
    Возвращает (A', B', M') в новой системе.
    """
    # Вычисляем вектор AB
    dx = b.x - a.x
    dy = b.y - a.y

    # Длина отрезка AB
    L = math.sqrt(dx*dx + dy*dy)

    # Защита от совпадения точек A и B
    if L == 0.0:
        raise ValueError("Точки A и B совпадают – направление оси X определить невозможно")

    # Координаты точки M относительно A
    mx = m.x - a.x
    my = m.y - a.y

    # Проекции на новую ось X (поворот)
    mx_prime = (mx * dx + my * dy) / L
    my_prime = (-mx * dy + my * dx) / L

    # Создаём новые точки
    a_prime = CoordinatePoint(0.0, 0.0, a.z)
    b_prime = CoordinatePoint(L, 0.0, b.z)
    m_prime = CoordinatePoint(mx_prime, my_prime, m.z)

    return a_prime, b_prime, m_prime


