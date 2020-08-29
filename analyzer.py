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

from key_pair_analyzer import KeyPairAnalyzer
from file_handler import FileHandler, make_file_name
from password_analyzer import PasswordAnalyzer
import key_pair_generator as keygen
import key_interval_analyzer as interval_plt
import keystroke_analyzer as stroke_plt
import config
import utils
import viterbi
import time


def run_debug(n=1, parallel=False, with_dict=True):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    password_analyzer = PasswordAnalyzer()

    file_name = make_file_name("4810", "4", "niequai4")
    file_handler.make_test_read_path_and_file(file_name, "4810", "4", "niequai4")

    password_analyzer.set_password("niequai4")
    password_analyzer.set_password_id(3)
    password_analyzer.read_packet_list(file_handler)
    password_analyzer.read_password_data()
    password_analyzer.read_other_packet_lists("4810")
    password_analyzer.calculate_max_overlapping_keystrokes()

    # len(all_states) = 9949 -> sum(15 choose x, x=1 to 6) + 1
    # all_states = utils.get_all_states(utils.extend_list_with_empty(config.chars), False)
    all_states = utils.extend_list_with_empty_state(
        utils.get_all_states_with_length(config.chars, False, password_analyzer.max_overlapping_keystrokes))
    all_states = utils.sort_states(all_states)

    file_name = make_file_name("4810", "1", "4a")
    file_handler.make_training_read_path_and_file(file_name, "4810", "1", "4a")

    analyzer.read_packet_list(file_handler)
    analyzer.calculate_probabilities()
    analyzer.calculate_initialization_vector()
    analyzer.transition_probabilities = utils.fill_transition_array(all_states, analyzer.transition_probabilities)
    analyzer.observation_probabilities = utils.fill_observation_array(all_states, analyzer.observation_probabilities)
    analyzer.normalize_probabilities()
    analyzer.normalize_initialization_vector()

    file_handler.set_path_and_file_name("debug_data/", "viterbi_debug_data")
    observation_list = file_handler.read_csv_to_list()
    observation_sequence = []
    for i in range(2, len(observation_list)):
        observation_sequence.append(observation_list[i][2])

    initialization_vector = analyzer.initialization_vector
    transition_array = analyzer.transition_probabilities
    observation_array = analyzer.observation_probabilities

    all_possible_states = utils.get_all_possible_states(observation_array)
    print("all poss states: " + str(len(all_possible_states)))

    state_space = utils.make_numpy_array_from_state_space(all_possible_states)
    IV = utils.make_numpy_array_from_initialisation_vector(all_possible_states, initialization_vector)
    A = utils.make_numpy_array_from_transition_matrix(all_possible_states, transition_array)
    B = utils.make_numpy_arrays_from_observation_matrix(all_possible_states, observation_array)
    y = utils.make_numpy_array_from_observation_sequence(observation_sequence)

    if not parallel:
        if with_dict:
            results = viterbi.n_viterbi_with_dict(
                all_possible_states,
                initialization_vector,
                transition_array,
                observation_array,
                observation_sequence,
                n
            )
        else:
            results = viterbi.n_viterbi(
                state_space,
                IV,
                A,
                B,
                y,
                n
            )
    else:
        results = viterbi.n_viterbi_parallel(
            all_possible_states,
            initialization_vector,
            transition_array,
            observation_array,
            observation_sequence,
            n
        )

    for result in results:
        print(result)


def run_debug_2(n=1, with_dict=True):
    all_states = [
        ('', ('', '', '', '', '', 'a')),
        ('', ('', '', '', '', '', 'b')),
        ('', ('', '', '', '', '', 'c')),
        ('', ('', '', '', '', '', 'd')),
        ('', ('', '', '', '', '', 'e'))
    ]

    str_state_a = ('', ('', '', '', '', '', 'a'))
    str_state_b = ('', ('', '', '', '', '', 'b'))
    str_state_c = ('', ('', '', '', '', '', 'c'))
    str_state_d = ('', ('', '', '', '', '', 'd'))
    str_state_e = ('', ('', '', '', '', '', 'e'))

    transition_matrix = {
        str_state_a: {
            str_state_a: 0.5,
            str_state_b: 0.6,
            str_state_c: 0.7,
            str_state_e: 0.1
        },
        str_state_b: {
            str_state_a: 0.2,
            str_state_b: 0.1,
            str_state_d: 0.8,
        },
        str_state_c: {
            str_state_c: 0.1,
            str_state_d: 0.7
        },
        str_state_d: {
            str_state_a: 0.6,
            str_state_b: 0.2,
            str_state_e: 0.9
        },
        str_state_e: {
            str_state_b: 0.4,
            str_state_c: 0.5,
            str_state_d: 0.1
        }
    }

    observation_matrix = {
        str_state_a: {
            0: 0.3,
            1: 0.4,
            2: 0.7
        },
        str_state_b: {
            0: 0.1,
            1: 0.8,
            2: 0.1,
            3: 0.6
        },
        str_state_c: {
            1: 0.1,
            2: 0.2,
            3: 0.4
        },
        str_state_d: {
            0: 0.6,
            2: 0.3,
            3: 0.1
        },
        str_state_e: {
            0: 0.4,
            1: 0.2,
            3: 0.2
        }
    }

    initialisation_vector = {
        str_state_a: 0,
        str_state_b: 0.7,
        str_state_c: 0.2,
        str_state_d: 0.3,
        str_state_e: 0.1
    }

    observation_sequence = [
        1,
        3,
        0,
        2
    ]

    # state_space = np.array([('', ('', '', '', '', '', 'a')), ('', ('', '', '', '', '', 'b')), ('', ('', '', '', '', '', 'c')), ('', ('', '', '', '', '', 'd')), ('', ('', '', '', '', '', 'e'))])
    # A = np.array([[0.5, 0.6, 0.7, 0, 0.1], [0.2, 0.1, 0, 0.8, 0], [0, 0, 0.1, 0.7, 0], [0.6, 0.2, 0, 0, 0.9], [0, 0.4, 0.5, 0.1, 0]])
    # B = np.array([[0.3, 0.4, 0.7, 0], [0.1, 0.8, 0.1, 0.6], [0, 0.1, 0.2, 0.4], [0.6, 0, 0.3, 0.1], [0.4, 0.2, 0, 0.2]])
    # IV = np.array([0, 0.7, 0.2, 0.3, 0.1])
    # y = np.array([1, 3, 0, 2])
    state_space = utils.make_numpy_array_from_state_space(all_states)
    A = utils.make_numpy_array_from_transition_matrix(all_states, transition_matrix)
    B = utils.make_numpy_arrays_from_observation_matrix(all_states, observation_matrix)
    IV = utils.make_numpy_array_from_initialisation_vector(all_states, initialisation_vector)
    y = utils.make_numpy_array_from_observation_sequence(observation_sequence)

    if not with_dict:
        result = viterbi.n_viterbi(
            state_space,
            IV,
            A,
            B,
            y,
            n
        )
    else:
        result = viterbi.n_viterbi_with_dict(
            all_states,
            initialisation_vector,
            transition_matrix,
            observation_matrix,
            observation_sequence,
            n
        )

    print(result[0])
    print(result[1])


def run(user_id, password_task_id, password_to_classify, password_id, n=1, parallel=False, with_dict=True):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    password_analyzer = PasswordAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    file_name = make_file_name(user_id, password_task_id, password_to_classify)
    file_handler.make_test_read_path_and_file(file_name, user_id, password_task_id, password_to_classify)

    password_analyzer.set_password(password_to_classify)
    password_analyzer.set_password_id(password_id)
    password_analyzer.read_packet_list(file_handler)
    password_analyzer.read_password_data()
    password_analyzer.read_other_packet_lists(user_id)
    password_analyzer.calculate_max_overlapping_keystrokes()

    # generate all states (optionally for extension of the observation and transition array, choose one)
    # len(all_states) = 9949 -> sum(15 choose x, x=1 to 6) + 1
    # all_states = utils.get_all_states(utils.extend_list_with_empty(config.chars), False)

    # all_states = utils.extend_list_with_empty_state(
    #     utils.get_all_states_with_length(config.chars, False, password_analyzer.max_overlapping_keystrokes))
    # all_states = utils.sort_states(all_states)

    for task_id in range(1, 3):
        if utils.is_task_completed(user_id, task_id, file_handler):
            if task_id == 1:
                key_pairs = char_pairs
            elif task_id == 2:
                key_pairs = shift_pairs
            else:
                break

            for (s1, s2) in key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.calculate_probabilities()
                analyzer.calculate_initialization_vector()

    analyzer.normalize_initialization_vector()

    # extend the observation and transition array with related states (optionally)
    # analyzer.transition_probabilities = utils.fill_transition_array(all_states, analyzer.transition_probabilities)
    # analyzer.observation_probabilities = utils.fill_observation_array(all_states, analyzer.observation_probabilities)

    analyzer.normalize_probabilities()

    # store the transition array and observation array for later usage (optionally)
    # file_handler.make_training_read_path_and_file(config.transitions_file_name, user_id)
    # analyzer.save_transition_probabilities(file_handler)

    # file_handler.make_training_read_path_and_file(config.observations_file_name, user_id)
    # analyzer.save_observation_probabilities(file_handler)

    # analyzer.print_probabilities()

    observation_sequence = password_analyzer.observation_sequence
    initialization_vector = analyzer.initialization_vector
    transition_array = analyzer.transition_probabilities
    observation_array = analyzer.observation_probabilities

    print("length observation_array: " + str(len(observation_array)))
    print("length transition_array: " + str(len(transition_array)))
    print()

    all_possible_states = utils.get_all_possible_states(observation_array)
    print("count all poss states: " + str(len(all_possible_states)))
    print()

    state_space = utils.make_numpy_array_from_state_space(all_possible_states)
    IV = utils.make_numpy_array_from_initialisation_vector(all_possible_states, initialization_vector)
    A = utils.make_numpy_array_from_transition_matrix(all_possible_states, transition_array)
    B = utils.make_numpy_arrays_from_observation_matrix(all_possible_states, observation_array)
    y = utils.make_numpy_array_from_observation_sequence(observation_sequence)

    if not parallel:
        if with_dict:
            results = viterbi.n_viterbi_with_dict(
                all_possible_states,
                initialization_vector,
                transition_array,
                observation_array,
                observation_sequence,
                n
            )
        else:
            results = viterbi.n_viterbi(
                state_space,
                IV,
                A,
                B,
                y,
                n
            )
    else:
        results = viterbi.n_viterbi_parallel(
            all_possible_states,
            initialization_vector,
            transition_array,
            observation_array,
            observation_sequence,
            n
        )

    # store the state sequences (optionally)
    # file_handler.set_path_and_file_name(
    #     "debug_data/out/classified_state_sequences/",
    #     password_to_classify + "_" + str(password_id) + "_top" + str(n)
    # )
    # file_handler.ensure_created()
    # file_handler.clear_file()
    # for result in results:
    #     file_handler.write_csv_row([str(result)])

    # store the passwords from the results
    outputs = []
    for result in results[1]:
        output = ""
        changed = utils.get_key_events(('', ['', '', '', '', '', '']), result[0][0])
        for change in changed:
            if change[1] == config.shift:
                continue

            if change[0] == '':
                output += change[1]

        for state in result:
            changed = utils.get_key_events(state[0], state[1])
            for change in changed:
                if change[1] == config.shift:
                    continue

                if change[0] == '':
                    new_key = change[1]
                    if state[1][0] == config.shift:
                        new_key = new_key.upper()
                    output += new_key

        if output not in outputs:
            outputs.append(output)

    file_handler.set_path_and_file_name(
        "classification_data/out/" +
        user_id +
        "/" +
        password_task_id +
        "/" +
        password_to_classify +
        "/" +
        str(password_id) +
        "/",
        password_to_classify + "_" + str(password_id) + "_top" + str(n)
    )
    file_handler.ensure_created()
    file_handler.clear_file()

    for output in outputs:
        file_handler.write_csv_row([output])
        print(output)


def plot_key_interval_distribution_for_hidden_state(user_id, x):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    for task_id in range(1, 2):
        if utils.is_task_completed(user_id, task_id, file_handler):
            if task_id == 1:
                key_pairs = char_pairs
            elif task_id == 2:
                key_pairs = shift_pairs
            else:
                break

            for (s1, s2) in key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.calculate_probabilities()

    print(analyzer.observation_probabilities[list(analyzer.observation_probabilities.keys())[x]])

    interval_plt.plot_single_interval_distribution(
        analyzer.observation_probabilities,
        list(analyzer.observation_probabilities.keys())[x]
    )


def plot_key_interval_distribution_for_user(user_id):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    for task_id in range(1, 3):
        if utils.is_task_completed(user_id, task_id, file_handler):
            if task_id == 1:
                key_pairs = char_pairs
            elif task_id == 2:
                key_pairs = shift_pairs
            else:
                break

            for (s1, s2) in key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.calculate_probabilities()

    # interval_plt.plot_key_press_interval_distribution(analyzer.observation_probabilities)
    # interval_plt.plot_key_release_interval_distribution(analyzer.observation_probabilities)
    interval_plt.plot_interval_distribution(analyzer.observation_probabilities)


def plot_all_key_interval_distributions_for_user(user_id):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    all_states = utils.extend_list_with_empty_state(
        utils.get_all_states_with_length(config.chars, False, 2))
    all_states = utils.sort_states(all_states)

    for task_id in range(1, 2):
        if utils.is_task_completed(user_id, task_id, file_handler):
            if task_id == 1:
                key_pairs = char_pairs
            elif task_id == 2:
                key_pairs = shift_pairs
            else:
                break

            for (s1, s2) in key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.calculate_probabilities()

    # observation_array = utils.fill_observation_array(all_states, analyzer.observation_probabilities)
    observation_array = analyzer.observation_probabilities

    interval_plt.plot_all_key_interval_distributions(observation_array)


def plot_key_interval_distribution(user_list=None):
    file_handler = FileHandler()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()
    analyzer = KeyPairAnalyzer()
    if user_list is None:
        file_handler.set_path_and_file_name("", config.users_file_name)
        file_handler.ensure_created()
        user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

    for user_id in user_list:
        for task_id in range(1, 3):
            if utils.is_task_completed(user_id, task_id, file_handler):
                if task_id == 1:
                    key_pairs = char_pairs
                elif task_id == 2:
                    key_pairs = shift_pairs
                else:
                    break

                for (s1, s2) in key_pairs:
                    string_to_enter = s1 + s2
                    file_name = make_file_name(user_id, task_id, string_to_enter)
                    file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                    analyzer.read_packet_list(file_handler)
                    analyzer.calculate_probabilities()

    # interval_plt.plot_key_press_interval_distribution(analyzer.observation_probabilities)
    # interval_plt.plot_key_release_interval_distribution(analyzer.observation_probabilities)
    interval_plt.plot_interval_distribution(analyzer.observation_probabilities)


def plot_entropy_and_information_gain_distribution(user_id):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    for task_id in range(1, 2):
        if utils.is_task_completed(user_id, task_id, file_handler):
            if task_id == 1:
                key_pairs = char_pairs
            elif task_id == 2:
                key_pairs = shift_pairs
            else:
                break

            for (s1, s2) in key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.calculate_probabilities()

    state_distribution = None
    # state_distribution = interval_plt.get_state_distribution(analyzer.observation_probabilities)

    analyzer.normalize_probabilities()

    interval_plt.plot_entropy_distribution(analyzer.observation_probabilities, state_distribution)
    interval_plt.plot_information_gain_distribution(analyzer.observation_probabilities, state_distribution)
    information_gain = interval_plt.calculate_information_gain(analyzer.observation_probabilities, state_distribution)
    print("Information Gain: " + str(information_gain))


def plot_key_changes_distribution(user_id):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    for task_id in range(1, 2):
        if utils.is_task_completed(user_id, task_id, file_handler):
            if task_id == 1:
                key_pairs = char_pairs
            elif task_id == 2:
                key_pairs = shift_pairs
            else:
                break

            for (s1, s2) in key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.calculate_probabilities()

    stroke_plt.plot_key_changes_distribution(analyzer.observation_probabilities)


def plot_overlapping_vs_non_overlapping_for_user(user_id, keystrokes=False, pie_chart=False):
    stroke_plt.plot_overlapping_vs_non_overlapping_for_user(user_id, keystrokes, pie_chart)


def plot_overlapping_vs_non_overlapping(user_list=None, keystrokes=False, pie_chart=False):
    stroke_plt.plot_overlapping_vs_non_overlapping(user_list, keystrokes, pie_chart)


def plot_overlapping_keystrokes_distribution(user_list=None):
    stroke_plt.plot_overlapping_keystrokes_distribution(user_list)


def plot_overlapping_keystrokes_comparison(user_list=None, labels=None):
    stroke_plt.plot_overlapping_keystrokes_comparison(user_list, labels)


def calculate_all_possible_passwords_count(n, shift_allowed):
    print("All possible passwords count: " + str(utils.get_count_all_possible_passwords(n, shift_allowed)))


def calculate_information_gain_for_all_users():
    file_handler = FileHandler()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    file_handler.set_path_and_file_name("", config.users_file_name)
    file_handler.ensure_created()
    user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

    for user_id in user_list:
        analyzer = KeyPairAnalyzer()
        print("User: " + str(user_id))
        for task_id in range(1, 2):
            if utils.is_task_completed(user_id, task_id, file_handler):
                if task_id == 1:
                    key_pairs = char_pairs
                elif task_id == 2:
                    key_pairs = shift_pairs
                else:
                    break

                for (s1, s2) in key_pairs:
                    string_to_enter = s1 + s2
                    file_name = make_file_name(user_id, task_id, string_to_enter)
                    file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                    analyzer.read_packet_list(file_handler)
                    analyzer.calculate_probabilities()

        state_distribution = None
        # state_distribution = interval_plt.get_state_distribution(analyzer.observation_probabilities)

        analyzer.normalize_probabilities()

        h0 = interval_plt.calculate_h0(analyzer.observation_probabilities, state_distribution)
        information_gain = interval_plt.calculate_information_gain(analyzer.observation_probabilities,
                                                                   state_distribution)
        print("H0: " + str(h0))
        print("Information Gain: " + str(information_gain))
        print()


def calculate_number_of_hidden_states_for_user(user_id):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()

    # all_states = utils.extend_list_with_empty_state(
    #     utils.get_all_states_with_length(config.chars, False, 2))
    # all_states = utils.sort_states(all_states)

    for task_id in range(1, 2):
        if utils.is_task_completed(user_id, task_id, file_handler):
            if task_id == 1:
                key_pairs = char_pairs
            elif task_id == 2:
                key_pairs = shift_pairs
            else:
                break

            for (s1, s2) in key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.calculate_probabilities()

    # observation_array = utils.fill_observation_array(all_states, analyzer.observation_probabilities)
    observation_array = analyzer.observation_probabilities
    all_possible_states = utils.get_all_possible_states(observation_array)
    print("Number of hidden state for user " + user_id + ": " + str(len(all_possible_states)))


def check_passwords_for_double(password_list=None, handler=None, n=0):
    if password_list is not None:
        passwords = password_list
    elif handler is not None:
        file_handler = handler
        passwords = file_handler.read_csv_to_list()
    elif n != 0:
        file_handler = FileHandler()
        file_handler.set_path_and_file_name("debug_data/out/" + str(n) + "/", "classified_passwords")
        file_handler.ensure_created()
        passwords = file_handler.read_csv_to_list()
    else:
        file_handler = FileHandler()
        file_handler.set_path_and_file_name("debug_data/", "classified_passwords")
        file_handler.ensure_created()
        passwords = file_handler.read_csv_to_list()

    used_passwords = []
    double_passwords = {}
    for password in passwords:
        if password[0] not in used_passwords:
            used_passwords.append(password[0])
        elif password[0] not in double_passwords:
            double_passwords[password[0]] = 2
        else:
            double_passwords[password[0]] += 1

    print("len(used_passwords): " + str(len(used_passwords)))
    print("len(double_passwords): " + str(len(double_passwords)))
    print()
    print("double passwords:")
    for password in double_passwords:
        print(password + ": " + str(double_passwords[password]))

    return used_passwords, double_passwords


def check_data_for_inconsistencies():
    file_handler = FileHandler()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()
    file_handler.set_path_and_file_name("", config.users_file_name)
    file_handler.ensure_created()
    user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

    for user_id in user_list:
        analyzer = KeyPairAnalyzer()
        print()
        print("User: " + str(user_id))

        task_id = 1
        if utils.is_task_completed(user_id, task_id, file_handler):
            for (s1, s2) in char_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.check_data_consistency(False)

        task_id = 2
        if utils.is_task_completed(user_id, task_id, file_handler):
            for (s1, s2) in shift_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.check_data_consistency(True)


def count_all_bluetooth_packets():
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    password_analyzer = PasswordAnalyzer()
    char_pairs = config.key_pairs
    shift_pairs = keygen.get_shift_pairs()
    file_handler.set_path_and_file_name("", config.users_file_name)
    file_handler.ensure_created()
    user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

    for user_id in user_list:
        task_id = 1
        with_shift = False
        if utils.is_task_completed(user_id, task_id, file_handler):
            for (s1, s2) in char_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.check_data_consistency(False)

        task_id = 2
        if utils.is_task_completed(user_id, task_id, file_handler):
            with_shift = True
            for (s1, s2) in shift_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

        password_analyzer.read_other_packet_lists(user_id, with_shift)

    packet_count = analyzer.bluetooth_packet_count + password_analyzer.bluetooth_packet_count
    print("Bluetooth packet count: " + str(packet_count))


st = time.time()

# -------------------------------- VITERBI ----------------------------------------------------- #

# run_debug()
# run_debug_2(n=2, with_dict=False)

# run("4810", "4", "niequai4", 5, n=10000, parallel=True, with_dict=True)
# run("9963", "5", "s4ci", 1, n=5, parallel=False, with_dict=True)


# -------------------------------- PLOTS ------------------------------------------------------- #

# plot_key_interval_distribution_for_hidden_state("4810", 3)      # p -> p + u
# plot_key_interval_distribution_for_hidden_state("4810", 152)    # 4 + q -> q
# plot_key_interval_distribution_for_user("2680")
# plot_key_interval_distribution_for_user("8502")
# plot_all_key_interval_distributions_for_user("8502")

# plot_key_interval_distribution()
# plot_key_interval_distribution(["2680", "4589", "8502", "9222"])  # Hybrid Typists
# plot_key_interval_distribution(["4810", "8150", "9086", "9963"])  # Touch Typists

# plot_key_changes_distribution("4810")

# plot_overlapping_vs_non_overlapping_for_user("4810")
# plot_overlapping_vs_non_overlapping_for_user("9222")

# plot_overlapping_vs_non_overlapping(keystrokes=True)
# plot_overlapping_vs_non_overlapping(["2680", "4589", "8502", "9222"], keystrokes=True)  # Hybrid Typists
# plot_overlapping_vs_non_overlapping(["4810", "8150", "9086", "9963"], keystrokes=True)  # Touch Typists

# plot_overlapping_keystrokes_distribution()
# plot_overlapping_keystrokes_distribution(["2680", "4589", "8502", "9222"])  # Hybrid Typists
# plot_overlapping_keystrokes_distribution(["4810", "8150", "9086", "9963"])  # Touch Typists

# plot_overlapping_keystrokes_comparison(["9222", "4589", "2680", "8502"], ["34", "37", "61", "72"])    # Hybrid Typists
# plot_overlapping_keystrokes_comparison(["9086", "8150", "9963", "4810"], ["53", "60", "64", "90"])    # Touch Typists

# plot_entropy_and_information_gain_distribution("4810")
# plot_entropy_and_information_gain_distribution("4589")

# -------------------------------- CALCULATIONS AND ANALYSES ----------------------------------- #

# check_data_for_inconsistencies()

# calculate_information_gain_for_all_users()

# calculate_number_of_hidden_states_for_user("8502")

# count_all_bluetooth_packets()

# check_passwords_for_double(n=500)

# calculate_all_possible_passwords_count(n=10, shift_allowed=True)


runtime_sec = time.time() - st
runtime_min = int(runtime_sec / 60)
runtime_min_sec = int(runtime_sec % 60)
print("---- %.2f sec ----" % runtime_sec)
print("---- %02d:%02d min ----" % (runtime_min, runtime_min_sec))
