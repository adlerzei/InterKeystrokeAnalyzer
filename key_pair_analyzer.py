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

import math
import config
import utils


class KeyPairAnalyzer:

    def __init__(self):
        self.packet_list = []
        self.file_name = ""
        self.transition_probabilities = {}
        self.observation_probabilities = {}
        self.initialization_vector = {}
        self.first_hidden_states_count = {}
        self.overlapping_count = 0
        self.non_overlapping_count = 0
        self.max_overlapping = 0
        self.overlapping_keystrokes_count = 0
        self.non_overlapping_keystrokes_count = 0
        self.bluetooth_packet_count = 0

    def read_packet_list(self, handler):
        self.packet_list = handler.read_csv_to_list()
        self.file_name = handler.file_name

        del self.packet_list[0]
        self.bluetooth_packet_count += len(self.packet_list)

    def calculate_initialization_vector(self):
        i = 1
        first_iteration = True
        last_keyboard_state = ()
        all_first_hidden_states = []
        for packet in self.packet_list:
            new_keyboard_state = (packet[5], packet[6])
            new_keyboard_state_eval = utils.try_eval_tuple(new_keyboard_state)
            new_keyboard_state_eval[1].sort()
            new_keyboard_state = utils.to_string_tuple(new_keyboard_state_eval)
            new_hidden_state = (last_keyboard_state, new_keyboard_state)

            # structure: i;delta;sniff-intervals;modifier-scan-code;keys-scan-code;modifier;keys
            if i == int(packet[0]):
                # transition probabilities
                if not first_iteration:
                    if new_hidden_state not in all_first_hidden_states:
                        all_first_hidden_states.append(new_hidden_state)

                    if new_hidden_state not in self.initialization_vector:
                        self.initialization_vector[new_hidden_state] = 0
                    self.initialization_vector[new_hidden_state] += 1
                    i += 1
                else:
                    first_iteration = False
            else:
                first_iteration = True

            last_keyboard_state = new_keyboard_state

        for hidden_state in all_first_hidden_states:
            if hidden_state not in self.first_hidden_states_count:
                self.first_hidden_states_count[hidden_state] = 0
            self.first_hidden_states_count[hidden_state] += 1

    def normalize_initialization_vector(self):
        total = 0

        for state in self.initialization_vector:
            # first normalize in terms of occurrences in packet_lists
            self.initialization_vector[state] /= self.first_hidden_states_count[state]
            # then count the total amount
            total += self.initialization_vector[state]

        for state in self.initialization_vector:
            # then normalize in terms of occurrences in total
            self.initialization_vector[state] /= total

    def calculate_probabilities(self):
        i = 0
        first_iteration = False
        last_keyboard_state = ()
        last_hidden_state = ()
        for packet in self.packet_list:
            new_keyboard_state = (packet[5], packet[6])
            new_keyboard_state_eval = utils.try_eval_tuple(new_keyboard_state)
            new_keyboard_state_eval[1].sort()
            new_keyboard_state = utils.to_string_tuple(new_keyboard_state_eval)
            sniff_intervals = int(packet[2])
            new_hidden_state = (last_keyboard_state, new_keyboard_state)

            # structure: i;delta;sniff-intervals;modifier-scan-code;keys-scan-code;modifier;keys
            if i == int(packet[0]):
                # transition probabilities
                if not first_iteration:
                    if last_hidden_state not in self.transition_probabilities:
                        self.transition_probabilities[last_hidden_state] = {}
                    trans_probs = self.transition_probabilities[last_hidden_state]

                    if new_hidden_state not in trans_probs:
                        trans_probs[new_hidden_state] = 0
                    trans_probs[new_hidden_state] += 1
                else:
                    first_iteration = False

                # observation probabilities
                if new_hidden_state not in self.observation_probabilities:
                    self.observation_probabilities[new_hidden_state] = {}
                observ_probs = self.observation_probabilities[new_hidden_state]

                if sniff_intervals not in observ_probs:
                    observ_probs[sniff_intervals] = 0
                observ_probs[sniff_intervals] += 1
            else:
                first_iteration = True

            last_keyboard_state = new_keyboard_state
            last_hidden_state = new_hidden_state
            i = int(packet[0])

    def normalize_probabilities(self):
        for initial_state in self.transition_probabilities:
            trans_dict = self.transition_probabilities[initial_state]
            # first: calculate total amount
            total = 0
            for next_state in trans_dict:
                total += trans_dict[next_state]

            # finally: normalize
            for next_state in trans_dict:
                trans_dict[next_state] /= total

        for hidden_state in self.observation_probabilities:
            observ_dict = self.observation_probabilities[hidden_state]
            # first: calculate total amount
            total = 0
            mean = 0
            for sniff_intervals in observ_dict:
                total += observ_dict[sniff_intervals]
                mean += sniff_intervals * observ_dict[sniff_intervals]
            mean /= total

            standard_deviation = 0
            for sniff_intervals in observ_dict:
                standard_deviation += ((sniff_intervals - mean) ** 2) * observ_dict[sniff_intervals]
            standard_deviation = (standard_deviation / total) ** 0.5

            if standard_deviation == 0:
                standard_deviation = 1

            denominator = (((math.pi * 2) ** 0.5) * standard_deviation)
            # finally: normalize
            for sniff_intervals in range(50):
                numerator = math.exp(-(((sniff_intervals - mean) ** 2) / (2 * (standard_deviation ** 2))))
                observ_dict[sniff_intervals] = numerator / denominator

    def save_transition_probabilities(self, file_handler):
        file_handler.write_json_dump(self.transition_probabilities)

    def save_observation_probabilities(self, file_handler):
        file_handler.write_json_dump(self.observation_probabilities)

    def print_probabilities(self):
        for probability_dict in self.transition_probabilities:
            for trans_prob in self.transition_probabilities[probability_dict]:
                print(str(probability_dict)
                      + " -> "
                      + str(trans_prob)
                      + ": "
                      + str(self.transition_probabilities[probability_dict][trans_prob])
                      )
            print()
        print()
        print()
        print()
        for observation_dict in sorted(self.observation_probabilities.keys()):
            for observ_prov in self.observation_probabilities[observation_dict]:
                print(str(observation_dict)
                      + " -> "
                      + str(observ_prov)
                      + ": "
                      + str(self.observation_probabilities[observation_dict][observ_prov])
                      )
            print()
        print()

    def count_overlapping_keystrokes_keyboard_states(self):
        for packet in self.packet_list:
            new_keyboard_state = (packet[5], packet[6])
            new_keyboard_state_eval = utils.try_eval_tuple(new_keyboard_state)
            new_keyboard_state_eval[1].sort()
            count = utils.get_length_of_state(new_keyboard_state_eval)

            # count if overlapping or not
            if count == 0:
                continue
            elif count == 1:
                self.non_overlapping_count += 1
            else:
                self.overlapping_count += 1

            # count max overlapping
            if count > self.max_overlapping:
                self.max_overlapping = count

    def count_overlapping_keystrokes(self):
        overlapping_key_pairs_list = []
        for packet in self.packet_list:
            if packet[0] in overlapping_key_pairs_list:
                continue

            new_keyboard_state = (packet[5], packet[6])
            new_keyboard_state_eval = utils.try_eval_tuple(new_keyboard_state)
            new_keyboard_state_eval[1].sort()
            count = utils.get_length_of_state(new_keyboard_state_eval)

            # count if overlapping or not
            if count > 1:
                overlapping_key_pairs_list.append(packet[0])

        self.overlapping_keystrokes_count += (len(overlapping_key_pairs_list)) * 2
        self.non_overlapping_keystrokes_count += (30 - len(overlapping_key_pairs_list)) * 2

    def check_data_consistency(self, shift_allowed):
        i = 0
        x = 100
        old_packet = None
        same_packet_content = 0
        same_packet_content_list = []
        wrong_modifier = 0
        wrong_modifier_list = []
        packet_interval_zero = 0
        packet_interval_zero_list = []
        packet_interval_greater_x = 0
        packet_interval_greater_x_list = []
        packet_count_per_recording_greater_4 = 0
        packet_count_per_recording_greater_4_list = []
        # packet_count_per_recording_smaller_4 = 0
        # packet_count_per_recording_smaller_4_list = []
        wrong_key_count = 0
        wrong_key_list = []
        packet_count_per_recording = 0
        for packet in self.packet_list:
            # if i != int(packet[0]) and i != 0 and packet_count_per_recording < 4:
            #     packet_count_per_recording_smaller_4 += 1
            #     packet_count_per_recording_smaller_4_list.append(int(packet[0])-1)

            key_list = eval(packet[6])
            for key in key_list:
                if key == "":
                    continue

                if key not in config.chars:
                    wrong_key_count += 1
                    wrong_key_list.append(packet[0])

            if i != int(packet[0]):
                packet_count_per_recording = 0
            packet_count_per_recording += 1

            if old_packet is not None:
                if (old_packet[5], old_packet[6]) == (packet[5], packet[6]):
                    same_packet_content += 1
                    same_packet_content_list.append(packet[0])

            if i == int(packet[0]) and int(packet[2]) == 0:
                packet_interval_zero += 1
                packet_interval_zero_list.append(packet[0])

            if i == int(packet[0]) and int(packet[2]) > x:
                packet_interval_greater_x += 1
                packet_interval_greater_x_list.append(packet[0])

            if packet_count_per_recording > 4:
                packet_count_per_recording_greater_4 += 1
                if packet[0] not in packet_count_per_recording_greater_4_list:
                    packet_count_per_recording_greater_4_list.append(packet[0])

            if packet[5] != "":
                if (packet[5] != "(shift)" and shift_allowed) or not shift_allowed:
                    wrong_modifier += 1
                    wrong_modifier_list.append(packet[0])

            if i != int(packet[0]) and i != int(packet[0]) - 1:
                print(self.file_name + " wrong packet numbering " + ": packet no " + packet[0])

            i = int(packet[0])
            old_packet = packet

        if same_packet_content > 0:
            print(
                self.file_name +
                " --> same packet content: " +
                str(same_packet_content) +
                " times: packet no. " +
                str(same_packet_content_list)
            )

        if wrong_modifier > 0:
            print(
                self.file_name +
                " --> wrong modifier: " +
                str(wrong_modifier) +
                " times: packet no. " +
                str(wrong_modifier_list)
            )

        if wrong_key_count > 0:
            print(
                self.file_name +
                " --> wrong key in packet: " +
                str(wrong_key_count) +
                " times: packet no. " +
                str(wrong_key_list)
            )

        if packet_interval_zero > 0:
            print(
                self.file_name +
                " --> packet interval zero: " +
                str(packet_interval_zero) +
                " times: packet no. " +
                str(packet_interval_zero_list)
            )

        if packet_interval_greater_x > 0:
            print(
                self.file_name +
                " --> packet interval greater " +
                str(x) + ": " +
                str(packet_interval_greater_x) +
                " times: packet no. " +
                str(packet_interval_greater_x_list)
            )

        if packet_count_per_recording_greater_4 > 0:
            print(
                self.file_name +
                " --> packet count per recording greater 4: " +
                str(packet_count_per_recording_greater_4) +
                " times: packet no. " +
                str(packet_count_per_recording_greater_4_list)
            )

        # if packet_count_per_recording_smaller_4 > 0:
        #     print(
        #         self.file_name +
        #         " --> packet count per recording smaller 4: " +
        #         str(packet_count_per_recording_smaller_4) +
        #         " times: packet no. " +
        #         str(packet_count_per_recording_smaller_4_list)
        #     )
