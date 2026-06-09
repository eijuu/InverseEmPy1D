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


import numpy as np


def __mad(uwn):
    m = np.median(uwn)
    uw = uwn - m
    return np.median(uw) * 1.483


def __delta_psi_function(x, c1=1.2, c2=3.5, c3=8):
    abs_x = abs(x)
    if abs_x < c1:
        return 1
    elif c1 <= abs_x < c2:
        return 0
    elif c2 <= abs_x < c3:
        return c1 / (c2 - c3)
    else:
        return 0


def __psi_function(x, c1=1.2, c2=3.5, c3=8):
    abs_x = abs(x)
    if abs_x < c1:
        return x
    elif c1 <= abs_x < c2:
        return np.sign(x) * c1
    elif c2 <= abs_x < c3:
        return np.sign(x) * c1 * (c3 - abs_x) / (c3 - c2)
    else:
        return 0


def __mu_estimate(uwn, _concll):
    m = np.median(uwn)
    sigma = __mad(uwn)
    a = _concll * 2
    if sigma < 1e-10:
        a = 0
    while abs(a) > _concll:
        new_uwn = (np.array(uwn) - m) / sigma
        upp = 0
        dawn = 0
        for u in new_uwn:
            upp += __psi_function(u)
            dawn += __delta_psi_function(u)
        if dawn > 1E-10:
            a = sigma * upp / dawn
        else:
            a = 0
        m += a
    return m


def mu_estimate_smooth(sm, size_win, _concll=1e-7):
    md2 = int((size_win - 1) / 2)
    um = np.zeros_like(sm)
    for i in range(md2, len(sm) - md2):
        fant = sm[i - md2: i + md2 + 1]
        um[i] = __mu_estimate(fant, _concll)
    for i in range(md2):
        um[i] = sm[i]
    for i in range(len(sm) - md2, len(sm)):
        um[i] = sm[i]
    return um


def mu_estimate_smooth_cutted(sm, size_win, _concll=1e-7):
    md2 = int((size_win - 1) / 2)
    valid_len = len(sm) - md2 * 2
    um = np.zeros(valid_len)
    for i in range(md2, len(sm) - md2):
        fant = sm[i - md2: i + md2 + 1]
        um[i - md2] = __mu_estimate(fant, _concll)
    return um


