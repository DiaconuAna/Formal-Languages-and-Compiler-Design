from finiteAutomata import fileRead


def printMenu():
    print("***************")
    print("0. Exit")
    print("1. Set of states")
    print("2. Alphabet")
    print("3. Transitions")
    print("4. Initial state")
    print("5. Set of final states")
    print("6. Check if sequence is accepted by the FA")
    print("***************")


def printStates(Q):
    print("Set of states: ")
    for state in Q:
        print(state, end=" ")
    print()


def printAlphabet(S):
    print("FA alphabet: ")
    for s in S:
        print(s, end=" ")
    print()


def printFinalStateSet(F):
    print("Set of final states: ")
    for state in F:
        print(state, end=" ")
    print()


def printTransitions(T):
    print("Set of transitions: ")
    for key in T.keys():
        print("({}, {}) -> {}".format(key[0], key[1], T[key]))


if __name__ == '__main__':
    FA = fileRead("FA.in")
    isOver = False

    while not isOver:
        printMenu()
        print("Your choice >>>")
        choice = int(input())
        match choice:
            case 0:
                isOver = True
                print("Goodbye")
            case 1:
                printStates(FA.Q)
            case 2:
                printAlphabet(FA.S)
            case 3:
                printTransitions(FA.T)
            case 4:
                print("Initial state: {}".format(FA.q0))
            case 5:
                printFinalStateSet(FA.F)
            case 6:
                print("Sequence: ")
                sequence = input()
                if FA.sequenceAccepted(sequence):
                    print("Sequence accepted")
                else:
                    print("Sequence not accepted")
            case _:
                print("Invalid option")
