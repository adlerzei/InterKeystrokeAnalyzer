import matplotlib.pyplot as plt
from tikzplotlib import save as tikz_save
import config

plt.style.use(config.matplotlib_style)


def plot_computing_performance():
    x = [5, 500, 2000, 5000, 10000, 15000]
    x_10 = [5, 500, 2000, 5000, 10000, 15000, 25000, 50000, 150000]
    x_16 = [5, 500, 2000, 5000, 10000]

    # ---------------------- NUMPY ARRAYS ------------------------ #

    # obs. seq. length = 8, numpy arrays, not parallel
    states_324_numpy = [1.1, 12.6, 158.5, 1267, 3278.9, 11202.3]
    states_302_numpy = [0.9, 11.4, 164.8, 1279.2, 3173.5, 9981.1]
    states_199_numpy = [0.8, 6.6, 99.4, 756, 2714.2, 5867.3]
    states_83_numpy = [0.7, 2.9, 34.5, 242.5, 816.2, 1878.1]

    # obs. seq. length = 10, numpy arrays, not parallel
    states_264_numpy = [1.1, 19, 277, 1704.4, 4637.4, 24142.1, 33109.4]

    # obs. seq. length = 16, numpy arrays, not parallel
    states_199_numpy_16 = [0.7, 18.4, 289.5, 1743.9, 6246.2]

    # ---------------------- PYTHON LISTS ----------------------- #

    # obs. seq. length = 8, python lists, not parallel
    states_324_lists = [3.7, 5.9, 16.4, 37.8, 71.3, 95.9]
    states_302_lists = [3.2, 5.7, 20.8, 50.7, 118.1, 156.6]
    states_199_lists = [1.7, 4.1, 15.6, 37.6, 71.3, 98.5]
    states_83_lists = [0.8, 1.9, 7.6, 13.8, 25.4, 36]

    # obs. seq. length = 10, python lists, not parallel
    states_264_lists = [3.3, 9.4, 57.8, 240.7, 713.2, 1154, 2007.7, 4297.4, 17761.4]

    print()

    # obs. seq. length = 16, python lists, not parallel
    states_199_lists_16 = [3.1, 16.5, 163.3, 976.2, 3432.8]

    # obs. seq. length = 16, python lists, parallel
    states_199_lists_parallel_16 = [498.5, 505.1, 605.3, 1376.7, 4049.6]

    # ------------------ Compare all methods --------------------- #

    plt.plot(x_16, states_199_numpy_16, label="Numpy array")
    plt.plot(x_16, states_199_lists_16, label="Python dict, not parallelized")
    plt.plot(x_16, states_199_lists_parallel_16, label="Python dict, parallelized")
    plt.xlabel("Number of results to calculate", fontsize=12)
    plt.ylabel("Computation time (\\SI{}{\\second})", fontsize=12)
    plt.legend()

    tikz_save(
        "fig/all_algorithms_comparison.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2000", "ytick distance=1000"]
    )

    plt.show()

    # ------------------ Compare numpy intern ------------------- #

    plt.plot(x, states_324_numpy, label="324 hidden states")
    plt.plot(x, states_302_numpy, label="302 hidden states")
    plt.plot(x, states_199_numpy, label="199 hidden states")
    plt.plot(x, states_83_numpy, label="83 hidden states")
    plt.xlabel("Number of results to calculate", fontsize=12)
    plt.ylabel("Computation time (\\SI{}{\\second})", fontsize=12)
    plt.legend()

    tikz_save(
        "fig/numpy_intern_comparison.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2000",  "ytick distance=2000"]
    )

    plt.show()

    # ------------------ Compare lists intern ------------------- #

    plt.plot(x, states_324_lists, label="324 hidden states")
    plt.plot(x, states_302_lists, label="302 hidden states")
    plt.plot(x, states_199_lists, label="199 hidden states")
    plt.plot(x, states_83_lists, label="83 hidden states")
    plt.xlabel("Number of results to calculate", fontsize=12)
    plt.ylabel("Computation time (\\SI{}{\\second})", fontsize=12)
    plt.legend()

    tikz_save(
        "fig/dict_intern_comparison.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2000",  "ytick distance=20"]
    )

    plt.show()

    # ------------------ Compare shift calculations ------------- #

    plt.plot(x_10[:7], states_264_numpy, label="Numpy array")
    plt.plot(x_10[:7], states_264_lists[:7], label="Python dict, not parallelized")
    plt.xlabel("Number of results to calculate", fontsize=12)
    plt.ylabel("Computation time (\\SI{}{\\second})", fontsize=12)
    plt.legend()

    tikz_save(
        "fig/shift_computation_comparison.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2000",  "ytick distance=5000"]
    )

    plt.show()

    # ------------------ Single shift calculation -------------- #

    plt.plot(x_10, states_264_lists, label="Python dict, not parallelized")
    plt.xlabel("Number of results to calculate", fontsize=12)
    plt.ylabel("Computation time (\\SI{}{\\second})", fontsize=12)
    plt.legend()

    tikz_save(
        "fig/single_shift_computation.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=2000",  "ytick distance=5000"]
    )

    plt.show()


def plot_number_of_hidden_states():
    num_hidden_states_touch = {
        60: 302,
        90: 324
    }
    num_hidden_states_hybrid = {
        37: 83,
        72: 199,
    }

    plt.bar(range(2), num_hidden_states_touch.values())
    plt.xticks(range(2), num_hidden_states_touch.keys())

    plt.ylabel('Number of hidden states', fontsize=12)
    plt.xlabel('Typing speed (\\SI{}{wpm})', fontsize=12)

    tikz_save(
        "fig/num_hidden_states_touch.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=100"]
    )

    plt.show()

    plt.bar(range(2), num_hidden_states_hybrid.values())
    plt.xticks(range(2), num_hidden_states_hybrid.keys())

    plt.ylabel('Number of hidden states', fontsize=12)
    plt.xlabel('Typing speed (\\SI{}{wpm})', fontsize=12)

    tikz_save(
        "fig/num_hidden_states_hybrid.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=100"]
    )

    plt.show()


def plot_experiments_results():
    touch_results = {
        60: 22.2,
        90: 11.0
    }

    hybrid_results = {
        37: 17,
        72: 29
    }

    mean_results = {
        'Touch': 16.6,
        'Hybrid': 22.6
    }

    plt.bar(range(2), hybrid_results.values())
    plt.xticks(range(2), hybrid_results.keys())

    plt.ylabel('Success rate (\\SI{}{\\percent})', fontsize=12)
    plt.xlabel('Typing speed (\\SI{}{wpm})', fontsize=12)

    plt.ylim(top=30)

    tikz_save(
        "fig/experiments_results_hybrid.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=5"]
    )

    plt.show()

    plt.bar(range(2), touch_results.values())
    plt.xticks(range(2), touch_results.keys())

    plt.ylabel('Success rate (\\SI{}{\\percent})', fontsize=12)
    plt.xlabel('Typing speed (\\SI{}{wpm})', fontsize=12)

    plt.ylim(top=30)

    tikz_save(
        "fig/experiments_results_touch.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=5"]
    )

    plt.show()

    plt.bar(range(2), mean_results.values())
    plt.xticks(range(2), mean_results.keys())

    plt.ylabel('Success rate (\\SI{}{\\percent})', fontsize=12)
    plt.xlabel('Typing style', fontsize=12)

    tikz_save(
        "fig/experiments_results_comparison.tex",
        axis_height='\\figH',
        axis_width='\\figW',
        extra_axis_parameters=["tick label style={font=\\footnotesize}", "xtick distance=1", "ytick distance=5"]
    )

    plt.show()


# plot_computing_performance()

plot_number_of_hidden_states()

# plot_experiments_results()
