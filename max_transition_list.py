class MaxTransitionList(list):

    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        list.__init__(self, *args, **kwargs)

    def append(self, item):
        if type(item) != tuple:
            return

        if type(item[1]) != tuple:
            return

        prob = item[0]
        k = item[1][0]
        m = item[1][1]

        if len(self) == self.max_length:
            if prob > self[self.max_length-1][0]:
                del self[self.max_length-1]
            else:
                return

        list.append(self, (prob, (k, m)))
        list.sort(self, key=lambda elem: elem[0], reverse=True)

    def extend(self, items):
        for item in items:
            self.append(item)

    def get_probabilities(self):
        return [item[0] for item in self]

    def get_pointer(self):
        return [item[1] for item in self]


# max_transition_list = MaxTransitionList(5, [])
# max_transition_list.append((0.5, (5, 5)))
# max_transition_list.append((0.1, (1, 1)))
# max_transition_list.append((0.2, (2, 2)))
# max_transition_list.append((0.4, (4, 4)))
# max_transition_list.append((0.3, (3, 3)))
# max_transition_list.extend([(0.6, (6, 6)), (0.0, (0, 0))])
# print(max_transition_list)
# print(max_transition_list.get_probabilities())
# print(max_transition_list.get_pointer())



