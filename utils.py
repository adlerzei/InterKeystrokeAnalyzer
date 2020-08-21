import config
import numpy as np
from itertools import combinations


def try_eval_tuple(to_eval):
    if not to_eval or type(to_eval) is tuple:
        outer_eval = to_eval
    else:
        outer_eval = eval(to_eval)

    if type(outer_eval) is tuple:
        if type(outer_eval[0]) is tuple:
            if not outer_eval[0][0]:
                inner_eval_0_0 = outer_eval[0][0]
            else:
                inner_eval_0_0 = eval(outer_eval[0][0])

            if not outer_eval[0][1]:
                inner_eval_0_1 = outer_eval[0][1]
            else:
                inner_eval_0_1 = eval(outer_eval[0][1])

            inner_eval_0 = (inner_eval_0_0, inner_eval_0_1)
        else:
            inner_eval_0 = outer_eval[0]

        if type(outer_eval[1]) is tuple:
            if not outer_eval[1][0]:
                inner_eval_1_0 = outer_eval[1][0]
            else:
                inner_eval_1_0 = eval(outer_eval[1][0])

            if not outer_eval[1][1]:
                inner_eval_1_1 = outer_eval[1][1]
            else:
                inner_eval_1_1 = eval(outer_eval[1][1])

            inner_eval_1 = (inner_eval_1_0, inner_eval_1_1)
        else:
            if not outer_eval[1]:
                inner_eval_1 = outer_eval[1]
            else:
                inner_eval_1 = eval(outer_eval[1])

        outer_eval = (inner_eval_0, inner_eval_1)

    return outer_eval


def get_length_of_state(state):
    count = 0
    if state[0] != "":
        count += 1
    for char in state[1]:
        if char != "":
            count += 1
    return count


def to_string_tuple(state_tuple):
    if type(state_tuple) is not tuple:
        return ''
    return tuple(map(lambda entry: str(entry), state_tuple))


def to_string_hidden_state(hidden_state):
    return to_string_tuple(hidden_state[0]), to_string_tuple(hidden_state[1])


def is_task_completed(user_id, task_id, file_handler):
    file_handler.make_training_read_path_and_file(config.completed_tasks_file_name, user_id)
    completed_tasks = file_handler.read_csv_to_list()
    return [str(task_id), config.task_completed] in completed_tasks


def get_all_states_with_length(chars, shift_allowed, length=6):
    all_states = []
    for i in range(1, length+1):
        all_states.extend(list(map(lambda permu: ("", ([""] * (6 - i)) + list(permu)), combinations(chars, i))))
        if shift_allowed:
            all_states.extend(list(map(lambda permu: (config.shift, ([""] * (6 - i)) + list(permu)), combinations(chars, i))))

    return all_states


def get_all_states(chars, shift_allowed):
    all_states = []
    for i in range(len(chars)):
        for j in range(i, len(chars)):
            if i == j and chars[i] != "":
                continue
            for k in range(j, len(chars)):
                if j == k and chars[j] != "":
                    continue
                for m in range(k, len(chars)):
                    if k == m and chars[k] != "":
                        continue
                    for n in range(m, len(chars)):
                        if m == n and chars[m] != "":
                            continue
                        for o in range(n, len(chars)):
                            if n == o and chars[n] != "":
                                continue
                            new_state = ("", [chars[o], chars[n], chars[m], chars[k], chars[j], chars[i]])
                            all_states.append(new_state)
                            if shift_allowed:
                                new_state = (config.shift, [chars[o], chars[n], chars[m], chars[k], chars[j], chars[i]])
                                all_states.append(new_state)

    return all_states


def get_all_probable_states(chars, shift_allowed):
    all_states = []
    for i in range(len(chars)):
        for j in range(i, len(chars)):
            if i == j and chars[i] != "":
                continue
            for k in range(j, len(chars)):
                if j == k and chars[j] != "":
                    continue
                new_state = ("", [chars[k], chars[j], chars[i]])
                all_states.append(new_state)
                if shift_allowed:
                    new_state = (config.shift, [chars[k], chars[j], chars[i]])
                    all_states.append(new_state)

    return all_states


def extend_list_with_empty(chars):
    to_return = [""]
    to_return.extend(chars)
    return to_return


def extend_list_with_empty_state(state_list):
    return [("", ["", "", "", "", "", ""])] + state_list


def is_empty(state):
    return state[0] == "" and state[1] == ["", "", "", "", "", ""]


def get_key_events(old_state, next_state):
    changed = []
    if next_state[0] != old_state[0]:
        changed.append((old_state[0], next_state[0]))
    for key in old_state[1]:
        if key == "":
            continue
        if key not in next_state[1]:
            changed.append((key, ""))

    for key in next_state[1]:
        if key == "":
            continue
        if key not in old_state[1]:
            changed.append(("", key))

    return changed


def equals_key_events(first_change_list, second_change_list):
    for changed in first_change_list:
        if changed in second_change_list:
            second_change_list.remove(changed)
        else:
            return False
    return len(second_change_list) == 0


def is_substate(substate, state):
    if substate[0] != state[0]:
        return False
    for key in substate[1]:
        if key not in state[1]:
            return False
    return True


def is_compatible_first_state(first_state, to_check, first_state_is_empty):
    if first_state_is_empty and not is_empty(to_check):
        return False
    elif not is_substate(first_state, to_check):
        return False
    else:
        return True


def is_compatible_next_state(first_state, to_check, changed):
    if first_state == to_check:
        return False
    possible_changed = get_key_events(first_state, to_check)
    return equals_key_events(changed, possible_changed)


def deep_copy_state(state):
    new_state = (state[0], [])
    for key in state[1]:
        new_state[1].append(key)
    return new_state


def can_execute_change_list(state, change_list):
    new_state = deep_copy_state(state)
    for change in change_list:
        if change[1] != '' and change[1] in new_state[1]:
            return False
        if change[0] not in new_state[1]:
            return False
        new_state[1].remove(change[0])
    return True


def execute_change_list(state, change_list):
    new_state = deep_copy_state(state)
    for change in change_list:
        for i in range(len(new_state[1])):
            if new_state[1][i] == change[0]:
                new_state[1][i] = change[1]
                break
    new_state[1].sort()
    return new_state


def fill_observation_array(all_states, recorded_observations):
    observation_array = {}
    for (old_state, next_state) in recorded_observations:
        old_state_evaluated = try_eval_tuple(old_state)
        next_state_evaluated = try_eval_tuple(next_state)

        old_state_is_empty = False
        if is_empty(old_state_evaluated):
            old_state_is_empty = True

        changed = get_key_events(old_state_evaluated, next_state_evaluated)
        for possible_old_state in all_states:
            if not is_compatible_first_state(old_state_evaluated, possible_old_state, old_state_is_empty):
                continue

            if not can_execute_change_list(possible_old_state, changed):
                continue

            possible_next_state = execute_change_list(possible_old_state, changed)

            if possible_next_state not in all_states:
                continue

            str_possible_old_state = to_string_tuple(possible_old_state)
            str_possible_next_state = to_string_tuple(possible_next_state)

            if (str_possible_old_state, str_possible_next_state) in recorded_observations:
                observation_array[(str_possible_old_state, str_possible_next_state)] = \
                    recorded_observations[(str_possible_old_state, str_possible_next_state)]
                continue

            if (str_possible_old_state, str_possible_next_state) not in observation_array:
                observation_array[(str_possible_old_state, str_possible_next_state)] = {}

            for sniff_intervals in recorded_observations[(old_state, next_state)]:
                if sniff_intervals not in observation_array[(str_possible_old_state, str_possible_next_state)]:
                    observation_array[(str_possible_old_state, str_possible_next_state)][sniff_intervals] = \
                        recorded_observations[(old_state, next_state)][sniff_intervals]
                else:
                    observation_array[(str_possible_old_state, str_possible_next_state)][sniff_intervals] += \
                        recorded_observations[(old_state, next_state)][sniff_intervals]

    return observation_array


def fill_transition_array(all_states, recoded_transitions):
    transition_array = {}
    for (old_state, next_state) in recoded_transitions:
        old_state_evaluated = try_eval_tuple(old_state)
        next_state_evaluated = try_eval_tuple(next_state)

        old_state_is_empty = False
        if is_empty(old_state_evaluated):
            old_state_is_empty = True

        changed_first_state = get_key_events(old_state_evaluated, next_state_evaluated)
        for possible_old_state in all_states:
            if not is_compatible_first_state(old_state_evaluated, possible_old_state, old_state_is_empty):
                continue

            if not can_execute_change_list(possible_old_state, changed_first_state):
                continue

            possible_next_state = execute_change_list(possible_old_state, changed_first_state)

            if possible_next_state not in all_states:
                continue

            str_possible_old_state = to_string_tuple(possible_old_state)
            str_possible_next_state = to_string_tuple(possible_next_state)

            if (str_possible_old_state, str_possible_next_state) in recoded_transitions:
                transition_array[(str_possible_old_state, str_possible_next_state)] = \
                    recoded_transitions[(str_possible_old_state, str_possible_next_state)]
                continue

            for (_, last_state) in recoded_transitions[(old_state, next_state)]:
                last_state_evaluated = try_eval_tuple(last_state)
                changed_second_state = get_key_events(next_state_evaluated, last_state_evaluated)

                if not can_execute_change_list(possible_next_state, changed_second_state):
                    continue

                possible_last_state = execute_change_list(possible_next_state, changed_second_state)
                str_possible_last_state = to_string_tuple(possible_last_state)

                if (str_possible_old_state, str_possible_next_state) not in transition_array:
                    transition_array[(str_possible_old_state, str_possible_next_state)] = {}

                if (str_possible_next_state, str_possible_last_state) \
                        not in transition_array[(str_possible_old_state, str_possible_next_state)]:
                    transition_array[(str_possible_old_state,
                                      str_possible_next_state)][(str_possible_next_state,
                                                                 str_possible_last_state)] = \
                        recoded_transitions[(old_state,
                                             next_state)][(next_state,
                                                           last_state)]
                else:
                    transition_array[(str_possible_old_state,
                                      str_possible_next_state)][(str_possible_next_state,
                                                                 str_possible_last_state)] += \
                        recoded_transitions[(old_state,
                                             next_state)][(next_state,
                                                           last_state)]
    return transition_array


def get_all_possible_states(observation_array):
    possible_states = []
    for (first_state, next_state) in observation_array:
        first_state_eval = try_eval_tuple(first_state)
        next_state_eval = try_eval_tuple(next_state)
        if (first_state_eval, next_state_eval) not in possible_states:
            possible_states.append((first_state_eval, next_state_eval))
    return possible_states


def get_all_possible_keyboard_states_from_observations(observation_array):
    possible_keyboard_states = []
    for (first_state, next_state) in observation_array:
        first_state_eval = try_eval_tuple(first_state)
        next_state_eval = try_eval_tuple(next_state)
        if first_state_eval not in possible_keyboard_states:
            possible_keyboard_states.append(first_state_eval)
        if next_state_eval not in possible_keyboard_states:
            possible_keyboard_states.append(next_state_eval)
    return possible_keyboard_states


def get_all_possible_keyboard_states_from_transitions(transition_array):
    possible_keyboard_states = []
    for (first_state, next_state) in transition_array:
        first_state_eval = try_eval_tuple(first_state)
        next_state_eval = try_eval_tuple(next_state)
        if first_state_eval not in possible_keyboard_states:
            possible_keyboard_states.append(first_state_eval)
        if next_state_eval not in possible_keyboard_states:
            possible_keyboard_states.append(next_state_eval)

        for (_, last_state) in transition_array[(first_state, next_state)]:
            last_state_eval = try_eval_tuple(last_state)
            if last_state_eval not in possible_keyboard_states:
                possible_keyboard_states.append(last_state_eval)
    return possible_keyboard_states


def reduce_to_possible_keyboard_states(all_states):
    possible_states = [("", ["", "", "", "", "", ""])]
    for i in range(6):
        for (first_state, next_state) in all_states:
            if first_state not in possible_states \
                    and get_length_of_state(first_state) == 1:
                possible_states.append(first_state)

            if first_state in possible_states:
                if next_state not in possible_states:
                    possible_states.append(next_state)

    return possible_states


def reduce_to_possible_states(all_states):
    possible_keyboard_states = reduce_to_possible_keyboard_states(all_states)
    possible_states = []

    for (first_state, next_state) in all_states:
        if first_state in possible_keyboard_states and next_state in possible_keyboard_states:
            possible_states.append((first_state, next_state))

    return possible_states


def sort_states(all_states):
    for state in all_states:
        state[1].sort()
    return all_states


def make_numpy_array_from_initialisation_vector(all_states, initialisation_vector):
    IV = np.full(len(all_states), 0, np.float)
    for i in range(len(all_states)):
        str_state_i = to_string_hidden_state(all_states[i])
        if str_state_i in initialisation_vector:
            IV[i] = initialisation_vector[str_state_i]

    return IV


def make_numpy_arrays_from_observation_matrix(all_states, observation_matrix):
    # todo check if every sniff interval is within that range
    B = np.full((len(all_states), 50), 0, np.float)
    for i in range(len(all_states)):
        str_state_i = to_string_hidden_state(all_states[i])
        if str_state_i not in observation_matrix:
            continue

        for j in range(50):
            if j in observation_matrix[str_state_i]:
                B[i, j] = observation_matrix[str_state_i][j]

    return B


def make_numpy_array_from_transition_matrix(all_states, transition_matrix):
    A = np.full((len(all_states), len(all_states)), 0, np.float)
    for i in range(len(all_states)):
        str_state_i = to_string_hidden_state(all_states[i])
        if str_state_i not in transition_matrix:
            continue

        for j in range(len(all_states)):
            str_state_j = to_string_hidden_state(all_states[j])
            if str_state_j in transition_matrix[str_state_i]:
                A[i, j] = transition_matrix[str_state_i][str_state_j]

    return A


def make_numpy_array_from_observation_sequence(observation_sequence):
    return np.array(observation_sequence, np.uint16)


def make_numpy_array_from_state_space(state_space):
    out = np.empty(len(state_space), dtype=object)
    out[:] = state_space
    return out


def get_count_all_possible_passwords(n):
    potential_successors = {}
    for first_key_pair in config.key_pairs:
        for next_key_pair in config.key_pairs:
            if first_key_pair[1] != next_key_pair[0]:
                continue

            if first_key_pair not in potential_successors:
                potential_successors[first_key_pair] = []

            potential_successors[first_key_pair].append(next_key_pair)

    password_count = 0
    for key_pair in config.key_pairs:
        password_count += get_passwords_count(n-2, key_pair, potential_successors)
    return password_count


def get_passwords_count(n, actual_key_pair, potential_successors):
    if n == 0:
        return 1
    else:
        password_count = 0
        for next_key_pair in potential_successors[actual_key_pair]:
            password_count += get_passwords_count(n - 1, next_key_pair, potential_successors)
        return password_count
