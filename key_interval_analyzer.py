import matplotlib.pyplot as plt
import utils


def plot_key_interval_distribution(observation_probabilities):
    print("not implemented yet...")
    # todo


def plot_single_interval_distribution(observation_probabilities, hidden_state):
    plt.bar(observation_probabilities[hidden_state].keys(), observation_probabilities[hidden_state].values())
    plt.ylabel('Frequency', fontsize=16)
    plt.xlabel('Sniff Intervals for ' + str(hidden_state), fontsize=12)
    plt.show()


def get_key_press_interval_distribution(observation_probabilities):
    key_press_intervals = {}
    for hidden_state in observation_probabilities:
        change_list = utils.get_key_events(hidden_state[0], hidden_state[1])
        is_key_press = False
        for changed in change_list:
            if not changed[0] and changed[1]:
                is_key_press = True
                break
        if is_key_press:
            for sniff_interval in observation_probabilities[hidden_state]:
                if sniff_interval not in key_press_intervals:
                    key_press_intervals[sniff_interval] = 0

                key_press_intervals[sniff_interval] += observation_probabilities[hidden_state][sniff_interval]
    return key_press_intervals


def get_key_release_interval_distribution(observation_probabilities):
    key_release_intervals = {}
    for hidden_state in observation_probabilities:
        change_list = utils.get_key_events(hidden_state[0], hidden_state[1])
        is_key_release = False
        for changed in change_list:
            if not changed[1] and changed[0]:
                is_key_release = True
                break
        if is_key_release:
            for sniff_interval in observation_probabilities[hidden_state]:
                if sniff_interval not in key_release_intervals:
                    key_release_intervals[sniff_interval] = 0

                key_release_intervals[sniff_interval] += observation_probabilities[hidden_state][sniff_interval]
    return key_release_intervals


def plot_key_press_interval_distribution(observation_probabilities):
    key_press_intervals = get_key_press_interval_distribution(observation_probabilities)
    plt.bar(key_press_intervals.keys(), key_press_intervals.values())
    plt.ylabel('Frequency', fontsize=16)
    plt.xlabel('Sniff Intervals for Key Press Events', fontsize=12)
    plt.show()


def plot_key_release_interval_distribution(observation_probabilities):
    key_release_intervals = get_key_release_interval_distribution(observation_probabilities)
    plt.bar(key_release_intervals.keys(), key_release_intervals.values())
    plt.ylabel('Frequency', fontsize=16)
    plt.xlabel('Sniff Intervals for Key Release Events', fontsize=12)
    plt.show()
