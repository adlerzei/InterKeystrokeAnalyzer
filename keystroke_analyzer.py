import matplotlib.pyplot as plt
from tikzplotlib import save as tikz_save
from file_handler import FileHandler, make_file_name
from key_pair_analyzer import KeyPairAnalyzer
from password_analyzer import PasswordAnalyzer
import utils
import config

plt.style.use(config.matplotlib_style)


def calculate_overlapping_keystrokes_distribution_for_user(user_id):
    file_handler = FileHandler()
    analyzer = KeyPairAnalyzer()

    for task_id in range(1, 2):
        if utils.is_task_completed(user_id, task_id, file_handler):
            for (s1, s2) in config.key_pairs:
                string_to_enter = s1 + s2
                file_name = make_file_name(user_id, task_id, string_to_enter)
                file_handler.make_training_read_path_and_file(file_name, user_id, task_id, string_to_enter)

                analyzer.read_packet_list(file_handler)
                analyzer.count_overlapping_keystrokes()

    return analyzer


def plot_overlapping_vs_non_overlapping_for_user(user_id):
    analyzer = calculate_overlapping_keystrokes_distribution_for_user(user_id)

    print("non overlapping: " + str(analyzer.non_overlapping_count))
    print("overlapping: " + str(analyzer.overlapping_count))

    # Plot overlapping vs. non overlapping count

    explode = (0, 0.1)
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    ax.pie([analyzer.non_overlapping_count, analyzer.overlapping_count], labels=["Overlapping", "Non-Overlapping"], shadow=True, explode=explode)

    tikz_save(
        "fig/overlapping_vs_non_overlapping.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_tikzpicture_parameters=["font=\LARGE"],
        extra_axis_parameters=["xtick=\empty, ytick=\empty, axis lines=none, clip=false"],
    )

    plt.show()


def calculate_overlapping_keystrokes_distribution():
    file_handler = FileHandler()
    file_handler.set_path_and_file_name("", config.users_file_name)
    file_handler.ensure_created()
    user_list = list(map(lambda x: x[0], file_handler.read_csv_to_list()))

    max_overlapping_count = {}
    for user_id in user_list:
        password_analyzer = PasswordAnalyzer()
        password_analyzer.read_other_packet_lists(user_id)
        password_analyzer.calculate_max_overlapping_keystrokes()

        if password_analyzer.max_overlapping_keystrokes not in max_overlapping_count:
            max_overlapping_count[password_analyzer.max_overlapping_keystrokes] = 0
        max_overlapping_count[password_analyzer.max_overlapping_keystrokes] += 1

    return max_overlapping_count


def plot_overlapping_keystrokes_distribution():
    max_overlapping_count = calculate_overlapping_keystrokes_distribution()
    max_overlapping_count = dict(reversed(list(max_overlapping_count.items())))

    print("max overlapping: " + str(max_overlapping_count))

    # Plot the Hist
    plt.bar(max_overlapping_count.keys(), max_overlapping_count.values())

    plt.ylabel('User', fontsize=16)
    # plt.xlabel('Sniff Intervals for ' + str(hidden_state), fontsize=12)

    tikz_save(
        "fig/overlapping_keystrokes_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=2"]
    )

    plt.show()


def calculate_key_changes_distribution(observation_probabilities):
    changed_count = {}
    key_press_count = {}
    key_release_count = {}
    press_and_release = 0
    for old_state, new_state in observation_probabilities:
        changed = utils.get_key_events(old_state, new_state)

        if len(changed) not in changed_count:
            changed_count[len(changed)] = 0
        changed_count[len(changed)] += 1

        press_count = 0
        release_count = 0
        for old, new in changed:
            if old == "":
                press_count += 1
            elif new == "":
                release_count += 1

        if press_count > 0:
            if press_count not in key_press_count:
                key_press_count[press_count] = 0
            key_press_count[press_count] += 1

        if release_count > 0:
            if release_count not in key_release_count:
                key_release_count[release_count] = 0
            key_release_count[release_count] += 1

        if press_count > 0 and release_count > 0:
            press_and_release += 1

    return changed_count, key_press_count, key_release_count, press_and_release


def plot_key_changes_distribution(observation_probabilities):
    changed_count, key_press_count, key_release_count, press_and_release = calculate_key_changes_distribution(observation_probabilities)

    print("Count simultaneously press and release: " + str(press_and_release))

    # Plot change counts

    plt.bar(changed_count.keys(), changed_count.values())

    plt.ylabel('Frequency', fontsize=16)
    # plt.xlabel('Sniff Intervals for ' + str(hidden_state), fontsize=12)

    tikz_save(
        "fig/key_changes_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=50"]
    )

    plt.show()

    # Plot press counts

    explode = tuple(([0.0] * (len(key_press_count) - 1)) + [0.1])
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    ax.pie(key_press_count.values(), labels=key_press_count.keys(), shadow=True, explode=explode)

    tikz_save(
        "fig/press_count_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_tikzpicture_parameters=["font=\LARGE"],
        extra_axis_parameters=["xtick=\empty, ytick=\empty, axis lines=none, clip=false"]
    )

    plt.show()

    # Plot release counts

    explode = tuple(([0.0] * (len(key_release_count) - 1)) + [0.1])
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    ax.pie(key_release_count.values(), labels=key_release_count.keys(), shadow=True, explode=explode)

    tikz_save(
        "fig/release_count_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_tikzpicture_parameters=["font=\LARGE"],
        extra_axis_parameters=["xtick=\empty, ytick=\empty, axis lines=none, clip=false"]
    )

    plt.show()

    # Plot 2 changes distribution

    two_changes_values = [press_and_release]
    two_changes_labels = ["Press and Release"]

    if 2 in key_release_count:
        two_changes_values.append(key_release_count[2])
        two_changes_labels.append("2x Release")

    if 2 in key_press_count:
        two_changes_values.append(key_press_count[2])
        two_changes_labels.append("2x Press")

    explode = tuple(([0.0] * (len(two_changes_values) - 1)) + [0.1])
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    ax.pie(two_changes_values, labels=two_changes_labels, shadow=True, explode=explode)

    tikz_save(
        "fig/two_changes_distribution.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_tikzpicture_parameters=["font=\LARGE"],
        extra_axis_parameters=["xtick=\empty, ytick=\empty, axis lines=none, clip=false"]
    )

    plt.show()
