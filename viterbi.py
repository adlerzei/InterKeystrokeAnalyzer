def viterbi(state_space, transition_matrix, observation_matrix, observation_sequence):
    t1 = []
    t2 = []

    for i in range(len(state_space)):
        # todo IV
        t1[i][0] = observation_matrix[state_space[i]][observation_sequence[0]]
        t2[i][0] = 0

    for j in range(1, len(observation_sequence)):
        for i in range(len(state_space)):
            max_transition = 0
            arg_max_transition = ""
            for k in range(len(state_space)):
                trans = transition_matrix[state_space[k]][state_space[i]] * t1[i][j-1]
                if trans > max_transition:
                    max_transition = trans
                    arg_max_transition = k
            t1[i][j] = observation_matrix[state_space[i]][observation_sequence[j]] * max_transition
            t2[i][j] = arg_max_transition

    max_last_entry = 0
    max_last_index = -1
    for i in range(len(state_space)):
        if t1[i][len(observation_sequence) - 1] > max_last_entry:
            max_last_entry = t1[i][len(observation_sequence) - 1]
            max_last_index = i

    highest_path = []
    output = []
    for j in reversed(range(1, len(observation_sequence) - 1)):
        highest_path.insert(0, t2[max_last_index][j])
        output.insert(0, state_space[t2[max_last_index][j]])

    return output
