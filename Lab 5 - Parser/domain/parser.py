import logging


class Parser:
    def __init__(self, grammar):
        """
        working stack: working stack alpha which stores the way the parse is built
        input_stack: input stack beta which is a part of the tree to be built
        state: state of the parsing which can take one of the following values:
            • q = normal state
            • b = back state
            • f = final state - corresponding to success: w ε L(G)
            • e = error state – corresponding to insuccess: w ∉ L(G)
         i: position of current symbol in input sequence
        :param grammar: grammar of the language for which we will perform the sequence check
        """
        self._grammar = grammar
        self._working_stack = []
        self._input_stack = [self._grammar.getStartingSymbol()]
        self._state = "q"
        self._index = 1

    def getState(self):
        return self._state

    def setState(self, value):
        self._state = value

    def getIndex(self):
        return self._index

    def setIndex(self, value):
        self._index=value

    def getWorkingStack(self):
        return self._working_stack

    def setWorkingStack(self, stack):
        self._working_stack = stack

    def getInputStack(self):
        return self._input_stack

    def setInputStack(self, stack):
        self._input_stack = stack

    def expand(self):
        """
        Occurs when the head of the stack is a non-terminal
        (q,i, 𝜶, A𝜷) ⊢ (q,i, 𝜶A1, 𝜸1𝜷)
        where:
        A → 𝜸1 | 𝜸2 | … represents the productions corresponding to A
        1 = first prod of A

        Steps:

        1. pop A from the input stack beta
        2. add A1 to the working stack alpha
        3. Get the first production of A
        4. Add the corresponding production to the input stack beta
        :return:
        """
        nonTerminal = self._input_stack.pop(0)  # step 1
        self._working_stack.append((nonTerminal, 0))  # step 2
        production = self._grammar.getProductions(nonTerminal[0])[0]  # step 3
        self._input_stack = list(production[0]) + self._input_stack  # step 4

    def advance(self):
        """
        WHEN: head of input stack is a terminal = current symbol from input
        (q,i, 𝜶, ai𝜷) ⊢ (q,i+1, 𝜶ai, 𝜷)

        Steps:

        1. get the top of the input stack
        2. add it to the working stack
        3. increase index i
        :return:
        """
        nonTerminal = self._input_stack.pop(0)
        self._working_stack.append(nonTerminal)  # step 2
        self._index += 1  # step 3

    def momentaryInsuccess(self):
        """
        WHEN: head of input stack is a terminal ≠ current symbol from input
        (q,i, 𝜶, ai𝜷) ⊢ (b,i, 𝜶, ai𝜷)

        Steps:

        1.State becomes back.
        :return:
        """
        self._state = "b"  # step 1

    def back(self):
        """
        WHEN: head of working stack is a terminal
        (b,i, 𝜶a, 𝜷) ⊢ (b,i-1, 𝜶, a𝜷)

        Steps:

        1. get the last element from the working stack
        2. add it back to the input stack
        3. decrease index
        :return:
        """
        last = self._working_stack.pop()  # step 1
        self._input_stack = [last] + self._input_stack  # step 2
        self._index -= 1  # step 3

    def anotherTry(self):
        """
        WHEN: head of working stack is a nonterminal
        (b,i, 𝜶 Aj, 𝜸j 𝜷) ⊢ (q,i, 𝜶Aj+1, 𝜸j+1𝜷) , if ∃ A → 𝜸j+1
                            (b,i, 𝜶, A𝜷), otherwise with the exception
                            (e,i, 𝜶,𝜷), if i=1, A =S, ERROR

        Steps:

        1. get the top of the working stack: tuple of form (non_terminal, production_nr)
        2. check if we have more productions for that non-terminal
            2.1. update the state as 'q': normal state
            2.2. create a new tuple consisting of (non_terminal, production_nr+1) and add it to the working stack
                 (moving on to the next production)
            2.3. Update the top of input stack with the new production: delete old one and replace it
            2.4. Slice the list to delete last production
            2.5. Insert the new one on top
        3. if there are no more productions for the current terminal we check the following condition:
           (e,i, 𝜶,𝜷), if i=1, A =S, ERROR
        4. otherwise, delete the last production from the working stack and put the corresponding non-terminal in the
           input stack

        :return:
        """

        last = self._working_stack.pop()  # step 1
        # step 2
        if self._grammar.existsNextProduction(last[0], last[1]):
            self._state = "q"  # step 2.1
            self._working_stack.append((last[0], last[1] + 1))  # step 2.2
            lastLength = len(self._grammar.getProduction(last[0], last[1]))  # step 2.3
            self._input_stack = self._input_stack[lastLength:]  # step 2.4
            self._input_stack = list(self._grammar.getProduction(last[0], last[1] + 1)[0]) + self._input_stack  # step 2.5
        elif self._index == 1 and last[0] == self._grammar.getStartingSymbol:  # step 3
            self._state = "e"
        else:  # step 4
            lastLength = len(self._grammar.getProduction(last[0], last[1]))
            self._input_stack = self._input_stack[lastLength:]
            self._input_stack = [last[0]] + self._input_stack

    def success(self):
        """
        (q,n+1, 𝜶, 𝜀) ⊢ (f,n+1, 𝜶, 𝜀)

        Steps:

        1. Mark the state as final
        :return:
        """
        self._state = "f"  # step 1
