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

import csv
import json
import os
import config


def make_file_name(user_id, task_id, string_to_enter=""):
    if string_to_enter == "":
        return str(user_id) + "_" + str(task_id)
    else:
        return str(user_id) + "_" + str(task_id) + "_" + string_to_enter


class FileHandler:

    def __init__(self):
        self.path = ""
        self.file_name = ""

    def set_path_and_file_name(self, sub_path, file_name):
        parent_path = config.data_base_folder
        self.path = str(parent_path) + str(sub_path)
        self.file_name = str(file_name)

    def ensure_created(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        open(self.path + self.file_name, 'a+')

    def make_training_read_path_and_file(self, file_name, user_id="", task_id="", string_to_enter=""):
        if user_id == "" and task_id == "" and string_to_enter == "":
            path = "raw_data/"
        elif task_id == "" and string_to_enter == "":
            path = "raw_data/" + str(user_id) + "/"
        elif string_to_enter == "":
            path = "raw_data/" + str(user_id) + "/" + str(task_id) + "/"
        else:
            path = "raw_data/" + str(user_id) + "/" + str(task_id) + "/" + string_to_enter + "/"

        self.set_path_and_file_name(path, file_name)
        self.ensure_created()

    def make_training_write_path_and_file(self, file_name, user_id=""):
        if user_id == "":
            path = "training_data/"
        else:
            path = "training_data/" + str(user_id) + "/"

        self.set_path_and_file_name(path, file_name)
        self.ensure_created()

    def make_test_read_path_and_file(self, file_name, user_id="", task_id="", string_to_enter=""):
        self.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

    def make_test_write_path_and_file(self, file_name, user_id=""):
        if user_id == "":
            path = "out/"
        else:
            path = "out/" + str(user_id) + "/"

        self.set_path_and_file_name(path, file_name)
        self.ensure_created()

    def write_csv_row(self, row):
        with open(self.path + self.file_name, 'a+') as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(row)

    def read_csv_to_dict(self):
        with open(self.path + self.file_name, mode='r') as f:
            reader = csv.reader(f, delimiter=";")
            return dict((str(rows[0]), str(rows[1])) for rows in reader)

    def read_csv_to_list(self):
        with open(self.path + self.file_name, mode='r') as f:
            reader = csv.reader(f, delimiter=";")
            return list(reader)

    def write_json_dump(self, dict_to_save):
        json_dict = {}
        for outer_key in dict_to_save:
            json_dict[str(outer_key)] = {}
            for inner_key in dict_to_save[outer_key]:
                json_dict[str(outer_key)][str(inner_key)] = str(dict_to_save[outer_key][inner_key])

        with open(self.path + self.file_name, mode="w") as f:
            json.dump(json_dict, f)

    def read_json_to_dict(self):
        with open(self.path + self.file_name, mode='r') as f:
            json_dict = json.load(f)
            return json_dict

    def read_json_to_dict_eval(self):
        json_dict = self.read_json_to_dict()
        eval_dict = {}
        for outer_key in json_dict:
            eval_dict[eval(outer_key)] = {}
            for inner_key in json_dict[outer_key]:
                eval_dict[eval(outer_key)][eval(inner_key)] = eval(json_dict[outer_key][inner_key])

        return eval_dict

    def clear_file(self):
        open(self.path + self.file_name, mode="w")

