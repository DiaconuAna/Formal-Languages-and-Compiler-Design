"""
A finite automaton (FA) is a 5-tuple
M = (Q,Σ,δ,q0,F)

• Q - finite set of states (|Q|<∞)
• Σ - finite alphabet (|Σ|<∞)
• δ – transition function : δ:Q×Σ→P(Q)
• q0 – initial state q0 ε Q
• F⊆Q – set of final states
"""


def fileRead(file_name="FA.in"):
    """
    Read the elements of a FA (from file).
    :param file_name: name of the file
    :return: the FA or an error if the file content is incorrect
    """
    with open(file_name) as file:
        Q_line = file.readline()
        # remove leading and trailing spaces, split by ' ' and
        # take into consideration that the first 2 elements are Q/S/q0/F/T and =
        Q = Q_line.strip().split(' ')[2:]
        S_line = file.readline()
        S = S_line.strip().split(' ')[2:]
        q0_line = file.readline()  # q0 = A
        q0 = q0_line.strip().split(' ')[2]
        # print("q0 = {}".format(q0))
        F_line = file.readline()
        F = F_line.strip().split(' ')[2:]

        # now on to the set of transitions
        # first line : T =
        file.readline()

        T = {}  # dictionary where key = (source, value), value = destination
        for line in file:
            # (A,a) -> B; A - source, a - value, B - destination
            bare_line = line.strip().replace('(', '').replace(')', '').replace(',', '')
            source = bare_line[0]
            value = bare_line[1]
            destination = bare_line.strip().split('->')[1].strip()

            if (source, value) in T.keys():
                T[(source, value)].append(destination)  # add a new state
            else:
                T[(source, value)] = [destination]  # in case there are several other states to append2

        # check if the FA is valid before actually creating it

        # 1. initial state q0 must be in the set of states
        if q0 not in Q:
            raise Exception("Invalid input file FA.in: initial state q0 = {} is not in the set of states Q".format(q0))
        # 2. each final state must be in the set of states
        for final_state in F:
            if final_state not in Q:
                raise Exception(
                    "Invalid input file FA.in: final state = {} is not in the set of states Q".format(final_state))
        # 3. each transition in composed of an initial state (source), a final state (destination) and a value (
        # terminal symbol) the source and the destination must be in the set of states Q the value must be in the
        # alphabet S
        for key in T.keys():
            source = key[0]
            if source not in Q:
                raise Exception("Invalid input file FA.in: state {} is not in the set of states Q".format(source))
            value = key[1]
            if value not in S:
                raise Exception("Invalid input file FA.in: symbol {} is not in the alphabet S".format(value))
            for destination in T[key]:
                if destination not in Q:
                    raise Exception(
                        "Invalid input file FA.in: state {} is not in the set of states Q".format(destination))

        # if we reached this code, the finite automata is valid, and we can create it
        return FiniteAutomata(Q, S, q0, F, T)


class FiniteAutomata:
    def __init__(self, Q, S, q0, F, T):
        """
        :param Q: finite set of states
        :param S: finite alphabet
        :param q0: initial state
        :param F: set of final states
        :param T: set of state transitions
        """
        self.Q = Q
        self.S = S
        self.q0 = q0
        self.F = F
        self.T = T

    def isDFA(self):
        """
        Checks whether a FA is a DFA (deterministic finite automaton - there is at most a transition per symbol)
        :return: true if FA is DFA, else false
        """
        for key in self.T.keys():
            transition_count = len(self.T[key])
            if transition_count > 1:
                return False
        return True

    def sequenceAccepted(self, sequence):
        """
        3. For a DFA, verifies if a sequence is accepted by the FA.
        - we check if we get to a final state
        :param sequence:
        :return:
        """
        if not self.isDFA():
            return False
        else:
            current_state = self.q0  # start from the initial state
            for value in sequence:
                if (current_state, value) in self.T.keys():
                    current_state = self.T[(current_state, value)][0]  # destination becomes next starting point
                else:
                    return False  # the current value has no corresponding arrow in the FA
            # we should reach the end of the sequence
            return current_state in self.F
