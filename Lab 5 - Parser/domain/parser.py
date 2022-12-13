import logging

from domain.item import Item
from domain.parserOutput import ParserOutput


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
        self._index = 0
        self._tree = []

    def getTree(self):
        return self._tree

    def getState(self):
        return self._state

    def setState(self, value):
        self._state = value

    def getIndex(self):
        return self._index

    def setIndex(self, value):
        self._index = value

    def getWorkingStack(self):
        return self._working_stack

    def setWorkingStack(self, stack):
        self._working_stack = stack

    def getInputStack(self):
        return self._input_stack

    def setInputStack(self, stack):
        self._input_stack = stack

    def printCurrentConfiguration(self):
        print('**************')
        print('State: {}\n'.format(self._state))
        print('Index: {}\n'.format(self._index))
        print('Working stack: {}\n'.format(self._working_stack))
        print('Input stack: {}\n'.format(self._input_stack))
        print('**************')

    def parsingStrategy(self, w):
        """
        Parse a sequence using descendent recursive parsing
        :param w: sequence to be parsed
        :return:
        """
        w = w.split(' ')
        while self._state != 'f' and self._state != 'e':
            self.printCurrentConfiguration()
            if self._index < len(w):
                print("&&&&", w[self._index])
            if self._state == 'q':
                # print("*********** {}".format(w[self._index-1]))
                # if i = n+1 and input stack is empty => success
                if self._index == len(w) and len(self._input_stack) == 0:
                    self.success()
                # empty input stack and end of the sequence not reached => momentary insuccess
                elif len(self._input_stack) == 0:
                    self.momentaryInsuccess()
                # else if head(input stack) is a non-terminal => expand
                elif self._input_stack[0] in self._grammar.getNonTerminals():
                    self.expand()
                # else if head of the input stack = current element in the sequence => advance
                elif self._index < len(w) and self._input_stack[0] == w[self._index]:
                    self.advance()
                else:
                    self.momentaryInsuccess()
            elif self._state == 'b':
                # if head(working stack) == a - terminal
                if self._working_stack[-1] in self._grammar.getTerminals():
                    self.back()
                else:
                    self.anotherTry()
        if self._state == 'e':
            print('Error at index {}!'.format(self._index))
        else:
            print('Sequence {} is accepted!'.format(w))
            print(self._working_stack)
        self.createParsingTree()

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
        print('>>> expand ')
        nonTerminal = self._input_stack.pop(0)  # step 1
        print("????", nonTerminal)
        # production = self._grammar.getProductions(nonTerminal[0])[0]  # step 3
        production = self._grammar.getProductions(nonTerminal)[0]  # step 3
        print('*****', production)
        self._working_stack.append((nonTerminal, production[1]))  # step 2
        production_elems = production[0].split('$')
        # self._input_stack = list(production[0]) + self._input_stack  # step 4
        self._input_stack = production_elems + self._input_stack  # step 4

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
        print('>>> advance')
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
        print('>>> momentary insuccess')
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
        print('>>> back')
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
        print('>>> another try')
        last = self._working_stack.pop()  # step 1
        # step 2
        if self._grammar.existsNextProduction(last[0], last[1]):
            self._state = "q"  # step 2.1
            self._working_stack.append((last[0], last[1] + 1))  # step 2.2
            lastLength = len(self._grammar.getProduction(last[0], last[1]))  # step 2.3
            self._input_stack = self._input_stack[lastLength:]  # step 2.4
            production_elems = self._grammar.getProduction(last[0], last[1] + 1)[0]
            # self._input_stack = list(self._grammar.getProduction(last[0], last[1] + 1)[0]) + self._input_stack  # step 2.5
            self._input_stack = production_elems.split('$') + self._input_stack  # step 2.5
        elif self._index == 0 and last[0] == self._grammar.getStartingSymbol():  # step 3
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
        print('>>> success')
        self._state = "f"  # step 1

    def createParsingTree(self):
        father = -1

        # For every elem in working stack
        for index in range(0, len(self._working_stack)):
            # If elem is a tuple -> (non-terminal, production number)
            if type(self._working_stack[index]) == tuple:
                # Add new entry in table and set the value along with production number used
                self._tree.append(Item(self._working_stack[index][0]))  # value
                self._tree[index].production = self._working_stack[index][1]
            else:
                # Else elem is a terminal -> add new entry in table and set the value
                self._tree.append(Item(self._working_stack[index]))

        # Update father - sibling relationship
        # For every elem in working stack
        for index in range(0, len(self._working_stack)):
            # If elem is a tuple -> (non-terminal, production number)
            if type(self._working_stack[index]) == tuple:
                # Set the father and update it

                if self._tree[index].father == -1:
                    self._tree[index].father = father
                father = index

                # Get the length of the used production
                # prodLen = len(self._grammar.getProduction(self._working_stack[index][0], self._working_stack[index][1])[0])
                prodLen = len(
                    self._grammar.getProduction(self._working_stack[index][0], self._working_stack[index][1])[0].split(
                        '$'))
                indexList = []

                # Store the indexes in a list
                for i in range(1, prodLen + 1):
                    indexList.append(index + i)

                # Compute the right indexes where the elements from the production used are
                # For every index in indexList
                for i in range(0, prodLen):
                    # If in the tree at position indexList[i] is a non-terminal
                    if self._tree[indexList[i]].production != -1:
                        # Compute the offset to update the indexes
                        offset = self.get_length_depth(indexList[i])

                        # For every index remained in indexList add the offset to get the right index position
                        for j in range(i + 1, prodLen):
                            indexList[j] += offset
                            if indexList[j] == len(self._tree):
                                indexList[j] -= 1

                # Update the left sibling relation
                # For every index in indexList, except last because it will not be a left sibling to anyone
                for i in range(0, prodLen - 1):
                    #   Now that we computed the right indexes we can surely say that the item in the tree at position
                    # indexList[i] will be a left sibling to item at pos indexList[i+1]
                    self._tree[indexList[i]].sibling = indexList[i + 1]
                    if self._tree[indexList[i]].father == -1:
                        self._tree[indexList[i]].father = father
                    if i == prodLen - 2 and self._tree[indexList[i + 1]].father == -1:
                        self._tree[indexList[i + 1]].father = father
            else:
                if self._tree[index].father == -1:
                    self._tree[index].father = father
                father = -1

    def get_length_depth(self, index):
        # Get the length of the used production

        prodLen = len(
            self._grammar.getProduction(self._working_stack[index][0], self._working_stack[index][1])[0].split('$'))
        # prodLen = len(self._grammar.getProduction(self._working_stack[index][0], self._working_stack[index][1])[0])
        sum = prodLen
        for i in range(1, prodLen + 1):
            if type(self._working_stack[index + i]) == tuple:
                sum += self.get_length_depth(index + i)
        return sum
