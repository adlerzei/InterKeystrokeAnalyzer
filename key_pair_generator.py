# Copyright (C) 2020  Christian Zei
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random
import config


def get_shift_pairs():
    random.seed(config.random_seed)
    alpha_chars = list(filter(lambda x: str.isalpha(x), config.chars))
    shift_pairs = []

    for char in config.chars:
        shift_pairs.append((char, config.shift))
        shift_pairs.append((config.shift, char))

    for char in alpha_chars:
        shift_pairs.append((char.upper(), ''))

    return shift_pairs


def get_all_possible_char_pairs(chars):
    all_char_pairs = []

    # generate all possible key pairs
    for first_char in chars:
        for second_char in chars:
            if (first_char, second_char) not in all_char_pairs:
                all_char_pairs.append((first_char, second_char))

    return all_char_pairs


# print(get_char_pairs())
# print(get_shift_pairs())
