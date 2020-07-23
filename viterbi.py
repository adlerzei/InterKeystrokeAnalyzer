import utils
import numpy as np
from multiprocessing import Pool
from max_transition_list import MaxTransitionList
from itertools import starmap


def calculate_next_state_probabilities(t1_prev, k, m, observation_matrix_i_j, transition_matrix_k_i):
    if t1_prev is None:
        return

    trans = observation_matrix_i_j * transition_matrix_k_i * t1_prev

    return trans, (k, m)


def viterbi_with_list(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence):
    len_state_space = len(state_space)
    len_observation_sequence = len(observation_sequence)

    t1 = [[]] * len_state_space
    t2 = [[]] * len_state_space

    for i in range(len_state_space):
        str_state_i = utils.to_string_hidden_state(state_space[i])
        int_observation_0 = int(observation_sequence[0])

        t1[i] = [None] * len_observation_sequence
        t2[i] = [None] * len_observation_sequence

        if str_state_i not in observation_matrix \
                or int_observation_0 not in observation_matrix[str_state_i]:
            continue
        if str_state_i not in initialization_vector:
            t1[i][0] = 0
        else:
            t1[i][0] = initialization_vector[str_state_i] * observation_matrix[str_state_i][int_observation_0]
        t2[i][0] = 0

    for j in range(1, len_observation_sequence):
        for i in range(len_state_space):
            str_state_i = utils.to_string_hidden_state(state_space[i])
            int_observation_j = int(observation_sequence[j])
            if str_state_i not in observation_matrix \
                    or int_observation_j not in observation_matrix[str_state_i]:
                continue

            max_transition = 0
            arg_max_transition = 0
            for k in range(len_state_space):
                str_state_k = utils.to_string_hidden_state(state_space[k])

                if str_state_k not in transition_matrix \
                        or str_state_i not in transition_matrix[str_state_k]:
                    continue

                if t1[k][j-1] is None:
                    continue

                trans = transition_matrix[str_state_k][str_state_i] * t1[k][j-1]

                if trans > max_transition:
                    max_transition = trans
                    arg_max_transition = k

            t1[i][j] = observation_matrix[str_state_i][int_observation_j] * max_transition
            t2[i][j] = arg_max_transition

    max_last_entry = 0
    max_index = -1
    for i in range(len_state_space):
        if t1[i][len_observation_sequence - 1] is None:
            continue

        if t1[i][len_observation_sequence - 1] > max_last_entry:
            max_last_entry = t1[i][len_observation_sequence - 1]
            max_index = i

    highest_path = [None] * len_observation_sequence
    output = [None] * len_observation_sequence
    highest_path[len_observation_sequence - 1] = max_index
    output[len_observation_sequence - 1] = state_space[max_index]

    print("max index: " + str(max_index))
    print("max_last_entry: " + str(max_last_entry))

    for j in reversed(range(1, len_observation_sequence)):
        print("t2[max_index][j]: " + str(t2[max_index][j]))
        highest_path[j-1] = t2[max_index][j]
        print("state_space[t2[max_index][j]]: " + str(state_space[t2[max_index][j]]))
        output[j-1] = state_space[t2[max_index][j]]
        print("t2[max_index][j]: " + str(t2[max_index][j]))
        max_index = t2[max_index][j]
        print("max index: " + str(max_index))

    return highest_path, output


def viterbi(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence):
    len_state_space = state_space.shape[0]
    len_observation_sequence = observation_sequence.shape[0]

    t1 = np.empty((len_state_space, len_observation_sequence), np.float)
    t2 = np.empty((len_state_space, len_observation_sequence), np.uint16)

    # Initialize the tracking tables from first observation
    t1[:, 0] = initialization_vector * observation_matrix[:, observation_sequence[0]]
    t2[:, 0] = 0

    # Iterate through observations updating the tracking tables
    for j in range(1, len_observation_sequence):
        t1[:, j] = np.amax(t1[:, j - 1] * transition_matrix.T * observation_matrix[np.newaxis, :, observation_sequence[j]].T, 1)
        t2[:, j] = np.argmax(t1[:, j - 1] * transition_matrix.T, 1)

    # Build the output, optimal model trajectory
    x = np.empty(len_observation_sequence, np.uint16)
    output = np.empty(len_observation_sequence, np.object)

    x[-1] = np.argmax(t1[:, len_observation_sequence - 1])
    output[-1] = state_space[x[-1]]
    for i in reversed(range(1, len_observation_sequence)):
        x[i - 1] = t2[x[i], i]
        output[i - 1] = state_space[x[i - 1]]

    return x, output


def n_viterbi_with_list(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence, n):
    if n == 1:
        return viterbi_with_list(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence)

    len_state_space = len(state_space)
    len_observation_sequence = len(observation_sequence)

    t1 = [[]] * len_state_space
    t2 = [[]] * len_state_space

    for i in range(len_state_space):
        str_state_i = utils.to_string_hidden_state(state_space[i])
        int_observation_0 = int(observation_sequence[0])

        t1[i] = [[]] * len_observation_sequence
        t2[i] = [[]] * len_observation_sequence

        if str_state_i not in observation_matrix \
                or int_observation_0 not in observation_matrix[str_state_i]:
            continue
        if str_state_i not in initialization_vector:
            t1[i][0] = [0]
        else:
            t1[i][0] = [initialization_vector[str_state_i] * observation_matrix[str_state_i][int_observation_0]]
        t2[i][0] = [0]

    for j in range(1, len_observation_sequence):
        for i in range(len_state_space):
            str_state_i = utils.to_string_hidden_state(state_space[i])
            int_observation_j = int(observation_sequence[j])
            if str_state_i not in observation_matrix \
                    or int_observation_j not in observation_matrix[str_state_i]:
                continue

            max_transition_list = MaxTransitionList(n)
            for k in range(len_state_space):
                str_state_k = utils.to_string_hidden_state(state_space[k])

                if str_state_k not in transition_matrix \
                        or str_state_i not in transition_matrix[str_state_k]:
                    continue

                observation_matrix_i_j = observation_matrix[str_state_i][int_observation_j]
                transition_matrix_k_i = transition_matrix[str_state_k][str_state_i]

                max_transition_list.extend(starmap(calculate_next_state_probabilities,
                                                   [(
                                                       t1_prev,
                                                       k,
                                                       m,
                                                       observation_matrix_i_j,
                                                       transition_matrix_k_i,
                                                   ) for m, t1_prev in enumerate(t1[k][j-1])]))

            t1[i][j] = max_transition_list.get_probabilities()
            t2[i][j] = max_transition_list.get_pointer()

    max_transition_list = MaxTransitionList(n)
    for i in range(len_state_space):
        for m in range(len(t1[i][len_observation_sequence - 1])):
            max_transition_list.append((t1[i][len_observation_sequence - 1][m], (i, m)))

    outputs = []
    highest_paths = []

    for max_transition in max_transition_list:
        max_state_index = max_transition[1][0]
        max_state_transition_index = max_transition[1][1]
        max_last_entry = max_transition[0]

        highest_path = [None] * len_observation_sequence
        output = [None] * len_observation_sequence
        highest_path[len_observation_sequence - 1] = (max_state_index, max_state_transition_index)
        output[len_observation_sequence - 1] = state_space[max_state_index]

        print("max_state_index: " + str(max_state_index))
        print("max_state_transition_index: " + str(max_state_transition_index))
        print("max_last_entry: " + str(max_last_entry))

        for j in reversed(range(1, len_observation_sequence)):
            print("t2[max_state_index][j][max_state_transition_index]: " + str(t2[max_state_index][j][max_state_transition_index]))
            highest_path[j-1] = t2[max_state_index][j][max_state_transition_index]
            print("state_space[t2[max_state_index][j]]: " + str(state_space[t2[max_state_index][j][max_state_transition_index][0]]))
            output[j-1] = state_space[t2[max_state_index][j][max_state_transition_index][0]]
            print("t2[max_state_index][j][max_state_transition_index]: " + str(t2[max_state_index][j][max_state_transition_index]))
            max_state_index = highest_path[j-1][0]
            print("max_state_index: " + str(max_state_index))
            max_state_transition_index = highest_path[j-1][1]
            print("max_state_transition_index: " + str(max_state_transition_index))

        outputs.append(output)
        highest_paths.append(highest_path)

    return highest_paths, outputs


def n_viterbi(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence, N):
    if N == 1:
        return viterbi(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence)

    len_state_space = state_space.shape[0]
    len_observation_sequence = observation_sequence.shape[0]
    increasing_states_array = np.repeat(np.arange(len_state_space)[np.newaxis, :], len_state_space, axis=0)

    t1 = np.empty((len_state_space, len_observation_sequence, N), np.float)
    t2 = np.empty((len_state_space, len_observation_sequence, N, 2), np.object)

    # Initialize the tracking tables from first observation
    t1[:, 0, 0] = initialization_vector * observation_matrix[:, observation_sequence[0]]
    t1[:, 0, 1:N] = 0
    t2[:, 0, :] = (0, 0)

    # Iterate through observations updating the tracking tables
    for j in range(1, len_observation_sequence):
        all_probabilities = t1[:, j - 1, 0] * transition_matrix.T

        if len_state_space > N:
            best_state_indices = np.argpartition(all_probabilities, all_probabilities.shape[1] - N)[:, all_probabilities.shape[1] - N:]
            all_probabilities = np.take_along_axis(all_probabilities, best_state_indices, axis=-1) \
                                * observation_matrix[np.newaxis, :, observation_sequence[j]].T
            best_n_indices = np.zeros((len_state_space, N))
        else:
            best_state_indices = increasing_states_array
            best_n_indices = np.zeros((len_state_space, len_state_space))

        for n in range(1, N):
            all_probabilities = np.append(
                all_probabilities,
                t1[:, j - 1, n] * transition_matrix.T,
                axis=1
            )

            all_state_indices = np.append(
                best_state_indices,
                increasing_states_array,
                axis=1
            )

            all_n_indices = np.append(
                best_n_indices,
                np.full((len_state_space, len_state_space), n),
                axis=1
            )

            max_indices = np.argpartition(all_probabilities, all_probabilities.shape[1] - N)[:, all_probabilities.shape[1] - N:]
            all_probabilities = np.take_along_axis(all_probabilities, max_indices, axis=-1)
            best_state_indices = np.take_along_axis(all_state_indices, max_indices, axis=-1)
            best_n_indices = np.take_along_axis(all_n_indices, max_indices, axis=-1)

        t1[:, j, :] = all_probabilities * observation_matrix[np.newaxis, :, observation_sequence[j]].T
        t2[:, j, :, 0] = best_state_indices
        t2[:, j, :, 1] = best_n_indices

    # Build the output, optimal model trajectory
    x = np.empty((N, len_observation_sequence, 2), np.uint16)
    output = np.empty((N, len_observation_sequence), np.object)

    all_last_elements = t1[:, -1, :].ravel()
    largest_elements = -np.sort(-np.argpartition(all_last_elements, all_last_elements.shape[0] - N)[all_last_elements.shape[0] - N:])

    x[:, -1, 0] = largest_elements // N
    x[:, -1, 1] = largest_elements % N
    output[:, -1] = np.take_along_axis(state_space, x[:, -1, 0], axis=-1)
    for i in reversed(range(1, len_observation_sequence)):
        x[:, i - 1, :] = t2[x[:, i, 0], i, x[:, i, 1]]
        output[:, i - 1] = np.take_along_axis(state_space, x[:, i - 1, 0], axis=-1)

    return x, output


def n_viterbi_parallel(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence, n):
    len_state_space = len(state_space)
    len_observation_sequence = len(observation_sequence)

    t1 = [[]] * len_state_space
    t2 = [[]] * len_state_space

    for i in range(len_state_space):
        str_state_i = utils.to_string_hidden_state(state_space[i])
        int_observation_0 = int(observation_sequence[0])

        t1[i] = [[]] * len_observation_sequence
        t2[i] = [[]] * len_observation_sequence

        if str_state_i not in observation_matrix \
                or int_observation_0 not in observation_matrix[str_state_i]:
            continue
        if str_state_i not in initialization_vector:
            t1[i][0] = [0]
        else:
            t1[i][0] = [initialization_vector[str_state_i] * observation_matrix[str_state_i][int_observation_0]]
        t2[i][0] = [0]

    for j in range(1, len_observation_sequence):
        for i in range(len_state_space):
            str_state_i = utils.to_string_hidden_state(state_space[i])
            int_observation_j = int(observation_sequence[j])
            if str_state_i not in observation_matrix \
                    or int_observation_j not in observation_matrix[str_state_i]:
                continue

            max_transition_list = MaxTransitionList(n)
            for k in range(len_state_space):
                str_state_k = utils.to_string_hidden_state(state_space[k])

                if str_state_k not in transition_matrix \
                        or str_state_i not in transition_matrix[str_state_k]:
                    continue

                observation_matrix_i_j = observation_matrix[str_state_i][int_observation_j]
                transition_matrix_k_i = transition_matrix[str_state_k][str_state_i]

                # parallelized code:
                # for m in range(len(t1[k][j-1])):
                #
                #     if t1[k][j-1][m] is None:
                #         continue
                #
                #     trans = observation_matrix_i_j * transition_matrix_k_i * t1[k][j-1][m]
                #     max_transition_list.append((trans, (k, m)))

                with Pool(5) as p:
                    # t1_prev, k, m, str_state_k, str_state_i, transition_matrix, observation_matrix
                    max_transition_list.extend(p.starmap(calculate_next_state_probabilities,
                                                         [(
                                                             t1_prev,
                                                             k,
                                                             m,
                                                             observation_matrix_i_j,
                                                             transition_matrix_k_i,
                                                           ) for m, t1_prev in enumerate(t1[k][j-1])]))

            t1[i][j] = max_transition_list.get_probabilities()
            t2[i][j] = max_transition_list.get_pointer()

    max_transition_list = MaxTransitionList(n)
    for i in range(len_state_space):
        for m in range(len(t1[i][len_observation_sequence - 1])):
            max_transition_list.append((t1[i][len_observation_sequence - 1][m], (i, m)))

    outputs = []

    for max_transition in max_transition_list:
        max_state_index = max_transition[1][0]
        max_state_transition_index = max_transition[1][1]
        max_last_entry = max_transition[0]

        highest_path = [None] * len_observation_sequence
        output = [None] * len_observation_sequence
        highest_path[len_observation_sequence - 1] = (max_state_index, max_state_transition_index)
        output[len_observation_sequence - 1] = state_space[max_state_index]

        print("max_state_index: " + str(max_state_index))
        print("max_state_transition_index: " + str(max_state_transition_index))
        print("max_last_entry: " + str(max_last_entry))

        for j in reversed(range(1, len_observation_sequence)):
            print("t2[max_state_index][j][max_state_transition_index]: " + str(t2[max_state_index][j][max_state_transition_index]))
            highest_path[j-1] = t2[max_state_index][j][max_state_transition_index]
            print("state_space[t2[max_state_index][j]]: " + str(state_space[t2[max_state_index][j][max_state_transition_index][0]]))
            output[j-1] = state_space[t2[max_state_index][j][max_state_transition_index][0]]
            print("t2[max_state_index][j][max_state_transition_index]: " + str(t2[max_state_index][j][max_state_transition_index]))
            max_state_index = highest_path[j-1][0]
            print("max_state_index: " + str(max_state_index))
            max_state_transition_index = highest_path[j-1][1]
            print("max_state_transition_index: " + str(max_state_transition_index))

        outputs.append(output)

    return outputs
