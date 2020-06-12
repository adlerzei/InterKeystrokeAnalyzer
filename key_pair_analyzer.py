import utils

class KeyPairAnalyzer:

    def __init__(self):
        self.packet_list = []
        self.transition_probabilities = {}
        self.observation_probabilities = {}
        self.initialization_vector = {}

    def read_packet_list(self, handler):
        self.packet_list = handler.read_csv_to_list()

        del self.packet_list[0]

    def calculate_initialization_vector(self):
        i = 1
        first_iteration = True
        last_keyboard_state = ()
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
                    if new_hidden_state not in self.initialization_vector:
                        self.initialization_vector[new_hidden_state] = 0
                    self.initialization_vector[new_hidden_state] += 1
                    i += 1
                else:
                    first_iteration = False
            else:
                first_iteration = True

            last_keyboard_state = new_keyboard_state

    def normalize_initialization_vector(self):
        total = 0

        for state in self.initialization_vector:
            total += self.initialization_vector[state]

        for state in self.initialization_vector:
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
            for sniff_intervals in observ_dict:
                total += observ_dict[sniff_intervals]

            # finally: normalize
            for sniff_intervals in observ_dict:
                observ_dict[sniff_intervals] /= total

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

