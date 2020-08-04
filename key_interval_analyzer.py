import matplotlib.pyplot as plt
from tikzplotlib import save as tikz_save
from scipy.stats import norm
import numpy as np
import utils
import config

plt.style.use(config.matplotlib_style)


def plot_key_interval_distribution(observation_probabilities):
    print("not implemented yet...")
    # todo


def plot_single_interval_distribution(observation_probabilities, hidden_state):
    # Fit a normal distribution to the data:
    x_max = 0
    y_max = 0
    for sniff_interval in observation_probabilities[hidden_state]:
        x_max = sniff_interval if sniff_interval > x_max else x_max
        y_max = observation_probabilities[hidden_state][sniff_interval] if observation_probabilities[hidden_state][sniff_interval] > y_max else y_max

    total = 0
    mean = 0
    for sniff_intervals in observation_probabilities[hidden_state]:
        total += observation_probabilities[hidden_state][sniff_intervals]
        mean += sniff_intervals * observation_probabilities[hidden_state][sniff_intervals]
    mean /= total

    std = 0
    for sniff_intervals in observation_probabilities[hidden_state]:
        std += ((sniff_intervals - mean) ** 2) * observation_probabilities[hidden_state][sniff_intervals]
    std = (std / total) ** 0.5

    # Plot the Hist
    plt.bar(observation_probabilities[hidden_state].keys(), observation_probabilities[hidden_state].values())

    # Plot the PDF
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std) * total
    plt.plot(x, y, 'k', linewidth=2)

    plt.ylabel('Frequency', fontsize=16)
    # plt.xlabel('Sniff Intervals for ' + str(hidden_state), fontsize=12)

    tikz_save(
        "fig/single_interval_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=2"]
    )

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

    # Filter
    key_press_intervals = {k: v for k, v in key_press_intervals.items() if k <= 25}

    # Fit a normal distribution to the data:
    x_max = 0
    y_max = 0
    for sniff_interval in key_press_intervals:
        x_max = sniff_interval if sniff_interval > x_max else x_max
        y_max = key_press_intervals[sniff_interval] if key_press_intervals[sniff_interval] > y_max else y_max

    total = 0
    mean = 0
    for sniff_intervals in key_press_intervals:
        total += key_press_intervals[sniff_intervals]
        mean += sniff_intervals * key_press_intervals[sniff_intervals]
    mean /= total

    std = 0
    for sniff_intervals in key_press_intervals:
        std += ((sniff_intervals - mean) ** 2) * key_press_intervals[sniff_intervals]
    std = (std / total) ** 0.5

    # Plot the Hist
    plt.bar(key_press_intervals.keys(), key_press_intervals.values())

    # Plot the PDF
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std) * total
    plt.plot(x, y, 'k', linewidth=2)

    plt.ylabel('Frequency', fontsize=16)
    # plt.xlabel('Sniff Intervals for Key Press Events', fontsize=12)

    tikz_save(
        "fig/press_interval_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=5", "ytick distance=100"]
    )

    plt.show()


def plot_key_release_interval_distribution(observation_probabilities):
    key_release_intervals = get_key_release_interval_distribution(observation_probabilities)

    # Filter
    key_release_intervals = {k: v for k, v in key_release_intervals.items() if k <= 10}

    # Fit a normal distribution to the data:
    x_max = 0
    y_max = 0
    for sniff_interval in key_release_intervals:
        x_max = sniff_interval if sniff_interval > x_max else x_max
        y_max = key_release_intervals[sniff_interval] if key_release_intervals[sniff_interval] > y_max else y_max

    total = 0
    mean = 0
    for sniff_intervals in key_release_intervals:
        total += key_release_intervals[sniff_intervals]
        mean += sniff_intervals * key_release_intervals[sniff_intervals]
    mean /= total

    std = 0
    for sniff_intervals in key_release_intervals:
        std += ((sniff_intervals - mean) ** 2) * key_release_intervals[sniff_intervals]
    std = (std / total) ** 0.5

    # Plot the Hist
    plt.bar(key_release_intervals.keys(), key_release_intervals.values())

    # Plot the PDF
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std) * total
    plt.plot(x, y, 'k', linewidth=2)

    plt.ylabel('Frequency', fontsize=16)
    # plt.xlabel('Sniff Intervals for Key Release Events', fontsize=12)

    tikz_save(
        "fig/release_interval_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2", "ytick distance=500"]
    )

    plt.show()
