class Grammar:
    def __init__(self):
        self._N = []
        self._E = []
        self._P = {}
        self._S = []

    def getTerminals(self):
        return self._E

    def getNonTerminals(self):
        return self._N

    def getStartingSymbol(self):
        return self._S

    def getProductions(self, symbol):
        return self._P[symbol]

    def existsNextProduction(self, symbol, prodNr):
        if self._P[symbol][-1][1] == prodNr:
            return False
        return True

    def getProduction(self, symbol, prodNr):
        for p in self._P[symbol]:
            if p[1] == prodNr:
                # return p[0]
                return p

    def readFromFile(self, filename):
        """
        Reads a grammar from a file
        :param filename: given filename
        """
        with open(filename, 'r') as file:
            # Read the set of non-terminals
            self._N = Grammar.parseLine(file.readline())
            # Read the alphabet
            self._E = Grammar.parseLine(file.readline())
            # for val in self._E:
            #     print(val)
            # Read the starting symbol
            self._S = file.readline().split('=')[1].strip()
            # Read the production rules
            file.readline()
            rules = []
            for line in file:
                rules.append(line.strip())
            self._P = Grammar.parseRules(rules)

        if not Grammar.checkCFG(rules, self._N):
            raise Exception('Grammar is not CFG')

    def printNonTerminals(self):
        return str(self._N)

    def printAlphabet(self):
        return str(self._E)

    def printStartingSymbol(self):
        return str(self._S)

    def printProductions(self):
        return str(self._P)

    @staticmethod
    def parseLine(line):
        """
        Parses a line from the file that has the given structure: symbol = symbol { , symbol }
        :param line: given line from file
        :return: the list of values after equal
        """
        result = []
        after_equal = line.strip().split('=', 1)[1]
        if after_equal.strip()[-1] == ',':
            result = [',']
        result += [value.strip() for value in after_equal.split(',')]
        return result

    @staticmethod
    def parseRules(rules):
        """
        Parses the list of rules of the form A -> alpha { | beta }
        :return: a dictionary that contains the set of productions
        """
        result = {}
        # Index of the production
        index = 1

        for rule in rules:
            # Split by lhs and rhs
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [value.strip() for value in rhs.split('|')]

            # For each value in rhs:
            for value in rhs:
                if lhs in result.keys():
                    # If lsh is in the dictionary we append in the list of values
                    result[lhs].append((value, index))
                else:
                    # Else we add a new entry in the dictionary
                    result[lhs] = [(value, index)]
                index += 1
        return result

    @staticmethod
    def checkCFG(rules, N):
        """
        Checks if a grammar is a context free grammar: we check if every lhs has the form of: A [ -> alpha ]
        :param rules: the set of rules
        :param N: set of non-terminals
        :return: true | false
        """
        for rule in rules:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            count = 0
            for element in lhs.split('|'):
                element = element.strip()
                if element in N:
                    count += 1
            if count > 1:
                return False
        return True
