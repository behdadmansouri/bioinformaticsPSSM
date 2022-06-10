import math
from itertools import chain, combinations

class PSSM:
    def __init__(self, number_of_sequence, data_query, sequences):
        self.position = None
        self.characters = None
        self.matrix_profile = None
        self.sequences = sequences
        self.number_of_sequence = number_of_sequence
        self.data_query = data_query
        self.pseudo_count = 2
        self.max_score_substring = None
        self.substrings = []
        self.make_profile()

    def make_substrings_from_query(self):
        substring_length = len(self.sequences[0])
        list_of_seqes = []
        if len(self.data_query) <= substring_length:
            list_of_seqes.append(self.data_query)
        else:
            for i in range(0, len(self.data_query) - substring_length + 1):
                list_of_seqes.append(self.data_query[i:i + substring_length])
        for x in list_of_seqes:
            all_strings = list(powerset(range(0, len(x))))
            new_seq = []
            for i in range(substring_length):
                combination = [j for j in all_strings if len(j) == i]
                for b in combination:
                    x_array = list(x[0:substring_length - i])
                    for c in b:
                        x_array.insert(c, '-')
                    x_array = ''.join(x_array)
                    new_seq.append(x_array)
            self.substrings.extend(new_seq)

    def make_and_fill_profile(self):
        self.make_profile()
        self.count_characters()
        self.apply_pseudo_count()
        self.divide_by_background_chance_and_log()

    def make_profile(self):
        self.position = list(range(0, len(self.sequences[0])))
        self.characters = set().union(*self.sequences)
        self.characters.add('-')
        self.matrix_profile = {x: [0 for _ in range(len(self.position))] for x in self.characters}

    def divide_by_background_chance_and_log(self):
        overall = {x: sum(self.matrix_profile[x]) / len(self.matrix_profile[x]) for x in self.characters}
        for x in self.matrix_profile.keys():
            for y in range(len(self.matrix_profile[x])):
                self.matrix_profile[x][y] = (self.matrix_profile[x][y] / overall[x])
                self.matrix_profile[x][y] = math.log2(self.matrix_profile[x][y])

    def apply_pseudo_count(self):
        for x in self.matrix_profile.keys():
            for y in range(len(self.matrix_profile[x])):
                self.matrix_profile[x][y] = (self.matrix_profile[x][y] + self.pseudo_count) / \
                                            (self.number_of_sequence + self.pseudo_count * len(self.characters))

    def count_characters(self):
        for x in range(self.number_of_sequence):
            for c in self.position:
                self.matrix_profile[self.sequences[x][c]][c] += 1

    def find_max_scoring_substring(self):
        max_score = -100
        seq_of_max_score = ''
        for seq in self.substrings:
            score = 0
            for i, y in enumerate(seq):
                score += self.matrix_profile[y][i]
            if score > max_score:
                max_score = score
                seq_of_max_score = seq
        self.max_score_substring = seq_of_max_score


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def get_inputs():
    number_of_sequence = int(input())
    sequences = []
    for i in range(number_of_sequence):
        sequences.append(input())
    data_query = input()
    return number_of_sequence, data_query, sequences

def test():
    global our_pssm
    our_pssm = PSSM(4, "LIVPHHVPIPVLVIHPVLPPHIVLHHIHVHIHLPVLHIVHHLVIHLHPIVL", ["HVLIP", "H-MIP", "HVL-P", "LVLIP"])
    our_pssm.make_and_fill_profile()
    our_pssm.make_substrings_from_query()
    our_pssm.find_max_scoring_substring()
    assert our_pssm.max_score_substring == "H-L-P"
    print("test 1 successful")
    our_pssm = PSSM(4, "ATCCTATATCTTCTCTATACTATCCTTCA", ["T-CT", "--CT", "A-CT", "ATCT"])
    our_pssm.make_and_fill_profile()
    our_pssm.make_substrings_from_query()
    our_pssm.find_max_scoring_substring()
    assert our_pssm.max_score_substring == "A-CT"
    print("test 2 successful")


# uncomment test() to test the code
# test()
our_pssm = PSSM(*get_inputs())
our_pssm.make_and_fill_profile()
our_pssm.make_substrings_from_query()
our_pssm.find_max_scoring_substring()
print(our_pssm.max_score_substring)
