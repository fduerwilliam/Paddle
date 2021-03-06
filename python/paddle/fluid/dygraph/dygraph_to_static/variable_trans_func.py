#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

from __future__ import print_function

import six
import gast

from paddle.fluid.layers import fill_constant

__all__ = ['to_static_variable_gast_node', 'create_static_variable_gast_node']


def to_static_variable_gast_node(name):
    func_code = "{} = fluid.dygraph.dygraph_to_static.variable_trans_func.to_static_variable({})".format(
        name, name)
    return gast.parse(func_code).body[0]


def create_static_variable_gast_node(name):
    func_code = "{} = fluid.layers.data(name='{}', shape=[-1], dtype='float32')".format(
        name, name)
    return gast.parse(func_code).body[0]


def create_fill_constant_node(name, value):
    func_code = "{} = fluid.layers.fill_constant(shape=[1], ".format(name)
    if isinstance(value, bool):
        func_code += "dtype='bool', value={})".format(value)
        return gast.parse(func_code).body[0]
    if isinstance(value, float):
        func_code += "dtype='float64', value={})".format(value)
        return gast.parse(func_code).body[0]

    if six.PY2:
        if isinstance(value, int):
            func_code += "dtype='int32', value={})".format(value)
            return gast.parse(func_code).body[0]
        if isinstance(value, long):
            func_code += "dtype='int64', value={})".format(value)
            return gast.parse(func_code).body[0]
    else:
        if isinstance(value, int):
            func_code += "dtype='int64', value={})".format(value)
            return gast.parse(func_code).body[0]


def to_static_variable(x):
    '''
    Translate a Python variable to PaddlePaddle static graph variable
    '''
    if isinstance(x, bool):
        return fill_constant(shape=[1], dtype='bool', value=x)
    if isinstance(x, float):
        return fill_constant(shape=[1], dtype='float64', value=x)

    if six.PY2:
        if isinstance(x, int):
            return fill_constant(shape=[1], dtype='int32', value=x)
        if isinstance(x, long):
            return fill_constant(shape=[1], dtype='int64', value=x)
    else:
        if isinstance(x, int):
            return fill_constant(shape=[1], dtype='int64', value=x)
    return x
