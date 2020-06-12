import utils
from max_transition_list import MaxTransitionList


def viterbi(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence):
    t1 = [[]] * len(state_space)
    t2 = [[]] * len(state_space)

    for i in range(len(state_space)):
        t1[i] = [None] * len(observation_sequence)
        t2[i] = [None] * len(observation_sequence)
        if utils.to_string_hidden_state(state_space[i]) not in observation_matrix \
                or int(observation_sequence[0]) not in observation_matrix[utils.to_string_hidden_state(state_space[i])]:
            continue
        if utils.to_string_hidden_state(state_space[i]) not in initialization_vector:
            t1[i][0] = 0
        else:
            t1[i][0] = initialization_vector[utils.to_string_hidden_state(state_space[i])] * observation_matrix[utils.to_string_hidden_state(state_space[i])][int(observation_sequence[0])]
        t2[i][0] = 0

    for j in range(1, len(observation_sequence)):
        for i in range(len(state_space)):
            if utils.to_string_hidden_state(state_space[i]) not in observation_matrix \
                    or int(observation_sequence[j]) not in observation_matrix[utils.to_string_hidden_state(state_space[i])]:
                continue

            max_transition = 0
            arg_max_transition = 0
            for k in range(len(state_space)):
                if utils.to_string_hidden_state(state_space[k]) not in transition_matrix \
                        or utils.to_string_hidden_state(state_space[i]) not in transition_matrix[utils.to_string_hidden_state(state_space[k])]:
                    continue

                if t1[k][j-1] is None:
                    continue

                trans = transition_matrix[utils.to_string_hidden_state(state_space[k])][utils.to_string_hidden_state(state_space[i])] * t1[k][j-1]
                if trans > max_transition:
                    max_transition = trans
                    arg_max_transition = k
            t1[i][j] = observation_matrix[utils.to_string_hidden_state(state_space[i])][int(observation_sequence[j])] * max_transition
            t2[i][j] = arg_max_transition

    max_last_entry = 0
    max_index = -1
    for i in range(len(state_space)):
        if t1[i][len(observation_sequence) - 1] is None:
            continue

        if t1[i][len(observation_sequence) - 1] > max_last_entry:
            max_last_entry = t1[i][len(observation_sequence) - 1]
            max_index = i

    highest_path = [None] * len(observation_sequence)
    output = [None] * len(observation_sequence)
    highest_path[len(observation_sequence) - 1] = max_index
    output[len(observation_sequence) - 1] = state_space[max_index]

    print("max index: " + str(max_index))
    print("max_last_entry: " + str(max_last_entry))

    for j in reversed(range(1, len(observation_sequence))):
        print("t2[max_index][j]: " + str(t2[max_index][j]))
        highest_path[j-1] = t2[max_index][j]
        print("state_space[t2[max_index][j]]: " + str(state_space[t2[max_index][j]]))
        output[j-1] = state_space[t2[max_index][j]]
        print("t2[max_index][j]: " + str(t2[max_index][j]))
        max_index = t2[max_index][j]
        print("max index: " + str(max_index))

    return output


def n_viterbi(state_space, initialization_vector, transition_matrix, observation_matrix, observation_sequence, n):
    t1 = [[]] * len(state_space)
    t2 = [[]] * len(state_space)

    for i in range(len(state_space)):
        t1[i] = [[]] * len(observation_sequence)
        t2[i] = [[]] * len(observation_sequence)
        if utils.to_string_hidden_state(state_space[i]) not in observation_matrix \
                or int(observation_sequence[0]) not in observation_matrix[utils.to_string_hidden_state(state_space[i])]:
            continue
        if utils.to_string_hidden_state(state_space[i]) not in initialization_vector:
            t1[i][0] = [0]
        else:
            t1[i][0] = [initialization_vector[utils.to_string_hidden_state(state_space[i])] * observation_matrix[utils.to_string_hidden_state(state_space[i])][int(observation_sequence[0])]]
        t2[i][0] = [0]

    for j in range(1, len(observation_sequence)):
        for i in range(len(state_space)):
            if utils.to_string_hidden_state(state_space[i]) not in observation_matrix \
                    or int(observation_sequence[j]) not in observation_matrix[utils.to_string_hidden_state(state_space[i])]:
                continue

            max_transition_list = MaxTransitionList(n)
            for k in range(len(state_space)):

                for m in range(len(t1[k][j-1])):
                    if utils.to_string_hidden_state(state_space[k]) not in transition_matrix \
                            or utils.to_string_hidden_state(state_space[i]) not in transition_matrix[utils.to_string_hidden_state(state_space[k])]:
                        continue

                    if t1[k][j-1][m] is None:
                        continue

                    trans = observation_matrix[utils.to_string_hidden_state(state_space[i])][int(observation_sequence[j])] * transition_matrix[utils.to_string_hidden_state(state_space[k])][utils.to_string_hidden_state(state_space[i])] * t1[k][j-1][m]
                    max_transition_list.append((trans, (k, m)))

            t1[i][j] = max_transition_list.get_probabilities()
            t2[i][j] = max_transition_list.get_pointer()

    max_transition_list = MaxTransitionList(n)
    for i in range(len(state_space)):
        for m in range(len(t1[i][len(observation_sequence) - 1])):
            max_transition_list.append((t1[i][len(observation_sequence) - 1][m], (i, m)))

    outputs = []

    for max_transition in max_transition_list:
        max_state_index = max_transition[1][0]
        max_state_transition_index = max_transition[1][1]
        max_last_entry = max_transition[0]

        highest_path = [None] * len(observation_sequence)
        output = [None] * len(observation_sequence)
        highest_path[len(observation_sequence) - 1] = (max_state_index, max_state_transition_index)
        output[len(observation_sequence) - 1] = state_space[max_state_index]

        print("max_state_index: " + str(max_state_index))
        print("max_state_transition_index: " + str(max_state_transition_index))
        print("max_last_entry: " + str(max_last_entry))

        for j in reversed(range(1, len(observation_sequence))):
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

