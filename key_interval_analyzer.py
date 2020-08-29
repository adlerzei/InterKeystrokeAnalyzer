import matplotlib.pyplot as plt
from tikzplotlib import save as tikz_save
from scipy.stats import norm
import numpy as np
import utils
import config
import math

plt.style.use(config.matplotlib_style)


def plot_all_key_interval_distributions(observation_probabilities):
    max_x_axis = 9
    for hidden_state in observation_probabilities:
        # Fit a normal distribution to the data:
        x_max = 0
        y_max = 0

        # Filter
        key_intervals = {k: v for k, v in observation_probabilities[hidden_state].items() if 0 <= k <= max_x_axis}

        for sniff_interval in key_intervals:
            x_max = sniff_interval if sniff_interval > x_max else x_max
            y_max = key_intervals[sniff_interval] if key_intervals[sniff_interval] > y_max else y_max

        total = 0
        mean = 0
        for sniff_intervals in key_intervals:
            total += key_intervals[sniff_intervals]
            mean += sniff_intervals * key_intervals[sniff_intervals]

        if total == 0:
            continue

        mean /= total

        std = 0
        for sniff_intervals in key_intervals:
            std += ((sniff_intervals - mean) ** 2) * key_intervals[sniff_intervals]
        std = (std / total) ** 0.5

        if std == 0:
            std = 1

        x_max = max_x_axis if x_max >= max_x_axis - 2 else x_max + 2
        x = np.linspace(0, x_max, 100)
        y = norm.pdf(x, mean, std)
        if max(y) > 1:
            continue

        if max(y) > 0.95:
            print(hidden_state)

        plt.plot(x, y, 'k', linewidth=0.5)

        plt.ylabel('Probability', fontsize=16)
        plt.xlabel('Latency (sniff intervals)', fontsize=16)

        tikz_save(
            "fig/all_key_interval_distributions.tex",
            float_format='.3g',
            axis_height='\\figH',
            axis_width='\\figW',
            extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=0.2"]
        )

    plt.show()


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

    if std == 0:
        std = 1

    # Plot the Hist
    plt.bar(observation_probabilities[hidden_state].keys(), observation_probabilities[hidden_state].values())

    # Plot the PDF
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std) * total
    plt.plot(x, y, 'k', linewidth=2)

    plt.ylabel('Frequency', fontsize=16)
    plt.xlabel('Latency (sniff intervals)', fontsize=16)

    tikz_save(
        "fig/single_interval_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=2"]
    )

    plt.show()


def get_interval_distribution(observation_probabilities):
    key_press_intervals = {}
    for hidden_state in observation_probabilities:
        for sniff_interval in observation_probabilities[hidden_state]:
            if sniff_interval not in key_press_intervals:
                key_press_intervals[sniff_interval] = 0

            key_press_intervals[sniff_interval] += observation_probabilities[hidden_state][sniff_interval]
    return key_press_intervals


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


def plot_interval_distribution(observation_probabilities):
    key_intervals = get_interval_distribution(observation_probabilities)

    # Filter
    key_intervals = {k: v for k, v in key_intervals.items() if k <= 12}

    # Plot the Hist
    plt.bar(key_intervals.keys(), key_intervals.values())

    plt.ylabel('Frequency', fontsize=16)
    plt.xlabel('Latency (sniff intervals)', fontsize=16)

    tikz_save(
        "fig/key_interval_distribution_8502.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2", "ytick distance=500"]
    )

    plt.show()


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

    if std == 0:
        std = 1

    # Plot the Hist
    plt.bar(key_press_intervals.keys(), key_press_intervals.values())

    # Plot the PDF
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std) * total
    plt.plot(x, y, 'k', linewidth=2)

    plt.ylabel('Frequency', fontsize=16)
    plt.xlabel('Latency (sniff intervals)', fontsize=16)

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

    if std == 0:
        std = 1

    # Plot the Hist
    plt.bar(key_release_intervals.keys(), key_release_intervals.values())

    # Plot the PDF
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std) * total
    plt.plot(x, y, 'k', linewidth=2)

    plt.ylabel('Frequency', fontsize=16)
    plt.xlabel('Latency (sniff intervals)', fontsize=16)

    tikz_save(
        "fig/release_interval_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2", "ytick distance=500"]
    )

    plt.show()


def get_state_distribution(observation_probabilities):
    state_distribution = {}
    total = 0
    for state in observation_probabilities:
        state_distribution[state] = 0
        for sniff_intervals in observation_probabilities[state]:
            state_distribution[state] += observation_probabilities[state][sniff_intervals]
            total += observation_probabilities[state][sniff_intervals]

    for state in state_distribution:
        state_distribution[state] /= total

    return state_distribution


def calculate_pr_q_y0(observation_probabilities, sniff_intervals, state_to_calc, state_distribution=None):
    denominator = 0
    for state in observation_probabilities:
        if state_distribution is None:
            denominator += observation_probabilities[state][sniff_intervals] * 1 / len(observation_probabilities)
        else:
            denominator += observation_probabilities[state][sniff_intervals] * state_distribution[state]

    if state_distribution is None:
        numerator = observation_probabilities[state_to_calc][sniff_intervals] * 1 / len(observation_probabilities)
    else:
        numerator = observation_probabilities[state_to_calc][sniff_intervals] * state_distribution[state_to_calc]

    return numerator / denominator


def calculate_entropy(observation_probabilities, sniff_intervals, state_distribution=None):
    entropy = 0
    for state in observation_probabilities:
        pr_q_y0 = calculate_pr_q_y0(observation_probabilities, sniff_intervals, state, state_distribution)
        if pr_q_y0 > 0:
            entropy += pr_q_y0 * math.log2(pr_q_y0)
    entropy = -entropy
    return entropy


def calculate_entropy_distribution(observation_probabilities, x, state_distribution=None):
    entropy_distribution = np.empty(x)
    for i in range(x):
        entropy_distribution[i] = calculate_entropy(observation_probabilities, i, state_distribution)
    return entropy_distribution


def plot_entropy_distribution(observation_probabilities, state_distribution=None):
    x = 12
    entropy_distribution = calculate_entropy_distribution(observation_probabilities, x, state_distribution)
    plt.xlabel('Latency (sniff intervals)', fontsize=16)
    plt.ylabel('Entropy (\\SI{}{bits})', fontsize=16)
    plt.scatter(range(x), entropy_distribution)

    tikz_save(
        "fig/entropy_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2", "ytick distance=0.25"]
    )

    plt.show()


def calculate_information_gain_distribution(observation_probabilities, x, state_distribution=None):
    entropy_distribution = calculate_entropy_distribution(observation_probabilities, x, state_distribution)
    if state_distribution is None:
        start_entropy = math.log2(len(observation_probabilities))
    else:
        start_entropy = 0
        for state in state_distribution:
            start_entropy += state_distribution[state] * math.log2(state_distribution[state])
        start_entropy = -start_entropy

    information_gain_distribution = np.array([start_entropy - new_entropy for new_entropy in entropy_distribution])
    return information_gain_distribution


def plot_information_gain_distribution(observation_probabilities, state_distribution=None):
    x = 12
    information_gain_distribution = calculate_information_gain_distribution(observation_probabilities, x, state_distribution)
    plt.xlabel('Latency (sniff intervals)', fontsize=16)
    plt.ylabel('Information Gain (\\SI{}{bits})', fontsize=16)
    plt.scatter(range(x), information_gain_distribution)

    tikz_save(
        "fig/information_gain_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2", "ytick distance=0.25"]
    )

    plt.show()


def calculate_pr_y0(observation_probabilities, y0, state_distribution=None):
    pr_y0 = 0
    for state in observation_probabilities:
        if state_distribution is None:
            pr_y0 += observation_probabilities[state][y0] * 1 / len(observation_probabilities)
        else:
            pr_y0 += observation_probabilities[state][y0] * state_distribution[state]
    return pr_y0


def calculate_information_gain(observation_probabilities, state_distribution=None):
    x = 12
    if state_distribution is None:
        start_entropy = math.log2(len(observation_probabilities))
    else:
        start_entropy = 0
        for state in state_distribution:
            start_entropy += state_distribution[state] * math.log2(state_distribution[state])
        start_entropy = -start_entropy

    new_entropy = 0
    for i in range(x):
        pr_y0 = calculate_pr_y0(observation_probabilities, i, state_distribution)
        entropy = calculate_entropy(observation_probabilities, i, state_distribution)
        new_entropy += pr_y0 * entropy

    return start_entropy - new_entropy


def calculate_h0(observation_probabilities, state_distribution=None):
    if state_distribution is None:
        start_entropy = math.log2(len(observation_probabilities))
    else:
        start_entropy = 0
        for state in state_distribution:
            start_entropy += state_distribution[state] * math.log2(state_distribution[state])
        start_entropy = -start_entropy

    return start_entropy
