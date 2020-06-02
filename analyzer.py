from key_pair_analyzer import KeyPairAnalyzer
from file_handler import FileHandler, make_file_name
import key_pair_generator as keygen
import key_interval_analyzer as interval_plt
import config
import utils
import viterbi

# len(all_states) = 9949 -> sum(15 choose x, x=1 to 6) + 1
all_states = utils.get_all_states(utils.extend_list_with_empty(config.chars), False)
# all_states = utils.get_all_probable_states(utils.extend_list_with_empty([1, 2, 3]), False)
all_states = utils.sort_states(all_states)

file_handler = FileHandler()
analyzer = KeyPairAnalyzer()
char_pairs = keygen.get_char_pairs()
shift_pairs = keygen.get_shift_pairs()
file_handler.set_path_and_file_name("", config.users_file_name)
file_handler.ensure_created()
user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

file_name = make_file_name("4810", "1", "4a")
file_handler.make_training_read_path_and_file(file_name, "4810", "1", "4a")

analyzer.read_packet_list(file_handler)
analyzer.calculate_probabilities()

file_handler.set_path_and_file_name("debug_data/", "viterbi_debug_data")
observation_list = file_handler.read_csv_to_list()
observation_sequence = []
for i in range(2, len(observation_list)):
    observation_sequence.append(observation_list[i][2])

transition_array = utils.fill_transition_array(all_states, analyzer.transition_probabilities)
observation_array = utils.fill_observation_array(all_states, analyzer.observation_probabilities)

all_possible_states = utils.get_all_possible_states(observation_array)

result = viterbi.viterbi(all_possible_states,
                         transition_array,
                         observation_array,
                         observation_sequence)

#
# analyzer.print_probabilities()
#
# for user_id in user_list:
#     for task_id in range(1, 2):
#         if utils.is_task_completed(user_id, task_id, file_handler):
#             for (s1, s2) in char_pairs:
#                 string_to_enter = s1 + s2
#                 file_name = make_file_name(user_id, task_id, string_to_enter)
#                 file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)
#
#                 analyzer.read_packet_list(file_handler)
#                 analyzer.calculate_probabilities()

#    analyzer.normalize_probabilities()

#    file_handler.make_training_read_path_and_file(config.transitions_file_name, user_id)
#    analyzer.save_transition_probabilities(file_handler)

#    file_handler.make_training_read_path_and_file(config.observations_file_name, user_id)
#    analyzer.save_observation_probabilities(file_handler)
#
#     analyzer.print_probabilities()
#
#     transition_array = utils.fill_transition_array(all_states, analyzer.transition_probabilities)
#     observation_array = utils.fill_observation_array(all_states, analyzer.observation_probabilities)
#
#     # print("observation_array: " + str(observation_array))
#     print("length observation_array: " + str(len(observation_array)))
#     print()
#
#     # print("transition_array: " + str(transition_array))
#     print("length transition_array: " + str(len(transition_array)))
#     print()
#
#     all_possible_states = utils.get_all_possible_states(observation_array)
#     print("all possible states: " + str(all_possible_states))
#     print("count all poss states:" + str(len(all_possible_states)))
#     print()
#
#     all_possible_keyboard_states_from_observations = \
#         utils.get_all_possible_keyboard_states_from_observations(observation_array)
#     print("all possible keyboard states from observations: " + str(all_possible_keyboard_states_from_observations))
#     print("count all poss keyboard states from observations:" + str(len(all_possible_keyboard_states_from_observations)))
#     print()
#
#     all_possible_keyboard_states_from_transitions = \
#         utils.get_all_possible_keyboard_states_from_transitions(transition_array)
#     print("all possible keyboard states from transitions: " + str(all_possible_keyboard_states_from_transitions))
#     print("count all poss keyboard states from transitions:" + str(len(all_possible_keyboard_states_from_transitions)))
#     print()
#
#     all_states_reduced = utils.reduce_to_possible_states(all_possible_states)
#     print("all states reduced: " + str(all_states_reduced))
#     print("count all states reduced: " + str(len(all_states_reduced)))


# x = 1
# print(analyzer.observation_probabilities[list(analyzer.observation_probabilities.keys())[x]])
# interval_plt.plot_single_interval_distribution(analyzer.observation_probabilities, list(analyzer.observation_probabilities.keys())[x])

# interval_plt.plot_key_press_interval_distribution(analyzer.observation_probabilities)
# interval_plt.plot_key_release_interval_distribution(analyzer.observation_probabilities)
