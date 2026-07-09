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

import copy

import numpy as np


class ModelEnvironment:
    """
    Класс для хранения 1D моделей
    """

    def __init__(self):

        self.rho_value = np.log(np.array((50.0, 100.0, 150.0), dtype=np.float32))
        self.rho_value_max = np.log(np.array((1000.0, 1000.0, 1000.0), dtype=np.float32))
        self.rho_value_min = np.log(np.array((10.0, 10.0, 10.0), dtype=np.float32))
        self.rho_value_fix = np.array((False, False, False), dtype=np.bool)

        self.thickness_value = np.array((105.0, 205.0), dtype=np.float32)
        self.thickness_value_max = np.array((200.0, 300.0), dtype=np.float32)
        self.thickness_value_min = np.array((10.0, 20.0), dtype=np.float32)
        self.thickness_value_fix = np.array((False, False), dtype=np.bool)

    def insert_layer(self, index: int):
        self.rho_value = np.insert(self.rho_value, index, np.log(100.0))
        self.rho_value_max = np.insert(self.rho_value_max, index, np.log(1000.0))
        self.rho_value_min = np.insert(self.rho_value_min, index, np.log(10.0))
        self.rho_value_fix = np.insert(self.rho_value_fix, index, False)
        if index >= len(self.thickness_value):
            self.thickness_value = np.append(self.thickness_value, 100.0)
            self.thickness_value_max = np.append(self.thickness_value_max, 200.0)
            self.thickness_value_min = np.append(self.thickness_value_min, 10.0)
            self.thickness_value_fix = np.append(self.thickness_value_fix, False)
        else:
            self.thickness_value = np.insert(self.thickness_value, index, 100.0)
            self.thickness_value_max = np.insert(self.thickness_value_max, index, 200.0)
            self.thickness_value_min = np.insert(self.thickness_value_min, index, 10.0)
            self.thickness_value_fix = np.insert(self.thickness_value_fix, index, False)

    def delete_layer(self, index: int):
        self.rho_value = np.delete(self.rho_value, index)
        self.rho_value_max = np.delete(self.rho_value_max, index)
        self.rho_value_min = np.delete(self.rho_value_min, index)
        self.rho_value_fix = np.delete(self.rho_value_fix, index)
        if index >= len(self.thickness_value):
            self.thickness_value = np.delete(self.thickness_value, len(self.thickness_value) - 1)
            self.thickness_value_max = np.delete(self.thickness_value_max, len(self.thickness_value) - 1)
            self.thickness_value_min = np.delete(self.thickness_value_min, len(self.thickness_value) - 1)
            self.thickness_value_fix = np.delete(self.thickness_value_fix, len(self.thickness_value) - 1)
        else:
            self.thickness_value = np.delete(self.thickness_value, index)
            self.thickness_value_max = np.delete(self.thickness_value_max, index)
            self.thickness_value_min = np.delete(self.thickness_value_min, index)
            self.thickness_value_fix = np.delete(self.thickness_value_fix, index)

    def paste_model(self, other_model: ModelEnvironment):
        if other_model is None:
            return
        if other_model.rho_value is not None:
            self.rho_value = other_model.rho_value.copy()
        if other_model.rho_value_max is not None:
            self.rho_value_max = other_model.rho_value_max.copy()
            for i, m in enumerate(self.rho_value_max):
                if self.rho_value[i] > m:
                    self.rho_value[i] = m
        if other_model.rho_value_min is not None:
            self.rho_value_min = other_model.rho_value_min.copy()
            for i, m in enumerate(self.rho_value_min):
                if self.rho_value[i] < m:
                    self.rho_value[i] = m
        if other_model.rho_value_fix is not None:
            self.rho_value_fix = other_model.rho_value_fix.copy()

        if other_model.thickness_value is not None:
            self.thickness_value = other_model.thickness_value.copy()
        if other_model.thickness_value_max is not None:
            self.thickness_value_max = other_model.thickness_value_max.copy()
            for i, m in enumerate(self.thickness_value_max):
                if self.thickness_value[i] > m:
                    self.thickness_value[i] = m
        if other_model.thickness_value_min is not None:
            self.thickness_value_min = other_model.thickness_value_min.copy()
            for i, m in enumerate(self.thickness_value_min):
                if self.thickness_value[i] < m:
                    self.thickness_value[i] = m
        if other_model.thickness_value_fix is not None:
            self.thickness_value_fix = other_model.thickness_value_fix.copy()

    @staticmethod
    def copy_only_borders(model: ModelEnvironment):
        res = copy.deepcopy(model)
        res.rho_value = None
        res.rho_value_fix = None
        res.thickness_value = None
        res.thickness_value_fix = None
        return res

    @staticmethod
    def copy_model(model: ModelEnvironment):
        return copy.deepcopy(model)
