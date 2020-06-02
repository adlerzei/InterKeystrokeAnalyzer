import utils


def viterbi(state_space, transition_matrix, observation_matrix, observation_sequence):
    t1 = [[]] * len(state_space)
    t2 = [[]] * len(state_space)

    for i in range(len(state_space)):
        # todo IV
        t1[i] = [None] * len(observation_sequence)
        t2[i] = [None] * len(observation_sequence)
        if utils.to_string_hidden_state(state_space[i]) not in observation_matrix \
                or int(observation_sequence[0]) not in observation_matrix[utils.to_string_hidden_state(state_space[i])]:
            continue
        t1[i][0] = observation_matrix[utils.to_string_hidden_state(state_space[i])][int(observation_sequence[0])]
        t2[i][0] = 0

    for j in range(1, len(observation_sequence)):
        for i in range(len(state_space)):
            if utils.to_string_hidden_state(state_space[i]) not in observation_matrix \
                    or int(observation_sequence[j]) not in observation_matrix[utils.to_string_hidden_state(state_space[i])]:
                continue

            max_transition = 0
            arg_max_transition = ""
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

    for j in reversed(range(1, len(observation_sequence))):
        highest_path[j-1] = t2[max_index][j]
        output[j-1] = state_space[t2[max_index][j]]
        max_index = t2[max_index][j]

    return output

