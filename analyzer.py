from key_pair_analyzer import KeyPairAnalyzer
from file_handler import FileHandler, make_file_name
from password_analyzer import PasswordAnalyzer
import key_pair_generator as keygen
import key_interval_analyzer as interval_plt
import config
import utils
import viterbi
import time


def run_debug():
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    password_analyzer = PasswordAnalyzer()
    char_pairs = keygen.get_char_pairs()
    shift_pairs = keygen.get_shift_pairs()
    file_handler.set_path_and_file_name("", config.users_file_name)
    file_handler.ensure_created()
    user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

    file_name = make_file_name("4810", "1", "4a")
    file_handler.make_training_read_path_and_file(file_name, "4810", "1", "4a")

    analyzer.read_packet_list(file_handler)
    analyzer.calculate_probabilities()
    analyzer.normalize_probabilities()
    analyzer.calculate_initialization_vector()
    analyzer.normalize_initialization_vector()

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

    file_handler.set_path_and_file_name("debug_data/", "viterbi_debug_data")
    observation_list = file_handler.read_csv_to_list()
    observation_sequence = []
    for i in range(2, len(observation_list)):
        observation_sequence.append(observation_list[i][2])

    initialization_vector = analyzer.initialization_vector
    transition_array = utils.fill_transition_array(all_states, analyzer.transition_probabilities)
    observation_array = utils.fill_observation_array(all_states, analyzer.observation_probabilities)

    all_possible_states = utils.get_all_possible_states(observation_array)

    all_states_reduced = utils.reduce_to_possible_states(all_possible_states)
    print("all states reduced: " + str(all_states_reduced))
    print("count all states reduced: " + str(len(all_states_reduced)))

    results = viterbi.n_viterbi(all_possible_states,
                                initialization_vector,
                                transition_array,
                                observation_array,
                                observation_sequence,
                                5)

    for result in results:
        print(result)


def run(n, parallel=False):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()
    password_analyzer = PasswordAnalyzer()
    char_pairs = keygen.get_char_pairs()
    shift_pairs = keygen.get_shift_pairs()
    file_handler.set_path_and_file_name("", config.users_file_name)
    file_handler.ensure_created()
    user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

    for user_id in user_list:
        file_name = make_file_name(user_id, "4", "niequai4")
        file_handler.make_test_read_path_and_file(file_name, user_id, "4", "niequai4")

        password_analyzer.set_password("niequai4")
        password_analyzer.set_password_id(5)
        password_analyzer.read_packet_list(file_handler)
        password_analyzer.read_password_data()
        password_analyzer.read_other_packet_lists(user_id)
        password_analyzer.calculate_max_overlapping_keystrokes()

        # len(all_states) = 9949 -> sum(15 choose x, x=1 to 6) + 1
        # all_states = utils.get_all_states(utils.extend_list_with_empty(config.chars), False)
        all_states = utils.extend_list_with_empty_state(
            utils.get_all_states_with_length(config.chars, False, password_analyzer.max_overlapping_keystrokes))
        all_states = utils.sort_states(all_states)

        for task_id in range(1, 2):
            if utils.is_task_completed(user_id, task_id, file_handler):
                for (s1, s2) in char_pairs:
                    string_to_enter = s1 + s2
                    file_name = make_file_name(user_id, task_id, string_to_enter)
                    file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                    analyzer.read_packet_list(file_handler)
                    analyzer.calculate_probabilities()
                    analyzer.calculate_initialization_vector()

        analyzer.normalize_initialization_vector()
        analyzer.normalize_probabilities()

    #   file_handler.make_training_read_path_and_file(config.transitions_file_name, user_id)
    #   analyzer.save_transition_probabilities(file_handler)

    #   file_handler.make_training_read_path_and_file(config.observations_file_name, user_id)
    #   analyzer.save_observation_probabilities(file_handler)

    #   analyzer.print_probabilities()

        observation_sequence = password_analyzer.observation_sequence
        initialization_vector = analyzer.initialization_vector
        transition_array = utils.fill_transition_array(all_states, analyzer.transition_probabilities)
        observation_array = utils.fill_observation_array(all_states, analyzer.observation_probabilities)

        print("length observation_array: " + str(len(observation_array)))
        print("length transition_array: " + str(len(transition_array)))
        print()

        all_possible_states = utils.get_all_possible_states(observation_array)
        print("count all poss states: " + str(len(all_possible_states)))
        print()

    #   all_possible_keyboard_states_from_observations = \
    #       utils.get_all_possible_keyboard_states_from_observations(observation_array)
    #   print("all possible keyboard states from observations: " + str(all_possible_keyboard_states_from_observations))
    #   print("count all poss keyboard states from observations:" + str(len(all_possible_keyboard_states_from_observations)))
    #   print()

    #   all_possible_keyboard_states_from_transitions = \
    #       utils.get_all_possible_keyboard_states_from_transitions(transition_array)
    #   print("all possible keyboard states from transitions: " + str(all_possible_keyboard_states_from_transitions))
    #   print("count all poss keyboard states from transitions:" + str(len(all_possible_keyboard_states_from_transitions)))
    #   print()

        all_states_reduced = utils.reduce_to_possible_states(all_possible_states)
        print("count all states reduced: " + str(len(all_states_reduced)))

        if not parallel:
            results = viterbi.n_viterbi(all_possible_states,
                                        initialization_vector,
                                        transition_array,
                                        observation_array,
                                        observation_sequence,
                                        n)
        else:
            results = viterbi.n_viterbi_parallel(all_possible_states,
                                                 initialization_vector,
                                                 transition_array,
                                                 observation_array,
                                                 observation_sequence,
                                                 n)

        print(results)

        file_handler.set_path_and_file_name("debug_data/out", "classified_state_sequences")
        file_handler.ensure_created()
        file_handler.clear_file()
        for result in results:
            file_handler.write_csv_row([str(result)])

        outputs = []
        for result in results:
            output = ""
            changed = utils.get_key_events(('', ['', '', '', '', '', '']), result[0][0])
            for change in changed:
                if change[0] == '':
                    output += change[1]

            for state in result:
                changed = utils.get_key_events(state[0], state[1])
                for change in changed:
                    if change[0] == '':
                        output += change[1]

            outputs.append(output)

        print()
        print()
        file_handler.set_path_and_file_name("debug_data/out/" + str(n), "classified_passwords")
        file_handler.ensure_created()
        file_handler.clear_file()
        for output in outputs:
            file_handler.write_csv_row([output])
            print(output)

    # x = 1
    # print(analyzer.observation_probabilities[list(analyzer.observation_probabilities.keys())[x]])
    # interval_plt.plot_single_interval_distribution(analyzer.observation_probabilities, list(analyzer.observation_probabilities.keys())[x])

    # interval_plt.plot_key_press_interval_distribution(analyzer.observation_probabilities)
    # interval_plt.plot_key_release_interval_distribution(analyzer.observation_probabilities)


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


st = time.time()

# run_debug()
run(n=2000, parallel=True)

# check_passwords_for_double(n=500)

runtime_sec = time.time() - st
runtime_min = int(runtime_sec / 60)
runtime_min_sec = int(runtime_sec % 60)
print("---- %.2f sec ----" % runtime_sec)
print("---- %02d:%02d min ----" % (runtime_min, runtime_min_sec))
