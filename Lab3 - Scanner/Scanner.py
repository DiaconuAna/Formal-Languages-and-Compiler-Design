import re
from enum import Enum

from SymbolTable import SymbolTable


# 2 symbol tables - 1 for identifiers, 1 for constants

class ElementPIF(Enum):
    CONSTANT = 'ct'
    IDENTIFIER = 'id'


class Scanner:
    def __init__(self, file_info):
        self._lineCount = 0
        self._file = file_info
        self._identifiersSymbolTable = SymbolTable()
        self._constantsSymbolTable = SymbolTable()
        self._programInternalForm = []
        self._tokens = []
        try:
            self.readTokens()
            self.scan()
        except ValueError as err:
            print(err)

    def readTokens(self):
        with open("token.in.txt") as file:
            for line in file:
                self._tokens.append(line.rstrip())

    def writeToFile(self):
        with open('PIF.out', 'w') as file:
            for element in self._programInternalForm:
                file.write(str(element)+'\n')
        with open('ST.out', 'w') as file:
            file.write("\nIdentifiers Symbol Table\n")
            file.write(str(self._identifiersSymbolTable))
            file.write("\nConstants Symbol Table\n")
            file.write(str(self._constantsSymbolTable))

    def scan(self):
        lines = re.split('[\n]', self._file)
        code_lines = [x for x in lines if x != ' ' and x != '']

        for cline in code_lines:
            line_tokens = self.tokenizeLine(cline)
            # print(line_tokens)
            for token in line_tokens:
                if token in self._tokens:
                    self._programInternalForm.append((token, 0))
                else:
                    if self.classifyToken(token) == 0:
                        raise ValueError(
                            "Lexical error: Token {} cannot be classified: line {}".format(token, self._lineCount))
                    if self.classifyToken(token) == 1:
                        self._identifiersSymbolTable.add(token)
                        self._programInternalForm.append(('id', (
                            self._identifiersSymbolTable.getPos(token)[0],
                            self._identifiersSymbolTable.getPos(token)[1])))
                    if self.classifyToken(token) == 2 or self.classifyToken(token) == 3 or self.classifyToken(
                            token) == 4:
                        self._constantsSymbolTable.add(token)
                        self._programInternalForm.append(('ct', self._constantsSymbolTable.getPos(token)[0]))
        self.writeToFile()
        print("Lexically corect")

    def tokenizeLine(self, line_string):
        self._lineCount += 1
        line_data = re.split('("[^a-zA-Z0-9\"\']")|([^a-zA-Z0-9\"\'])', line_string)
        line_elements = [x for x in line_data if x is not None and x != '' and x != ' ' and x != '\t']
        final_line_tokens = []
        i = 0
        n = len(line_elements)

        # perform the look-ahead part for tokens such as: <-, <=, >=, <>, end_if, end_while, end_for
        while i < n:
            if i > n:
                break
            if line_elements[i] == '=' and line_elements[i + 1] == '=':
                raise ValueError("Invalid token == on line {}".format(self._lineCount))
            if line_elements[i] == '<':
                if line_elements[i + 1] in ['-', '=', '>']:
                    final_line_tokens.append('<' + line_elements[i + 1])
                    i = i + 1
                else:
                    final_line_tokens.append('<')
            elif line_elements[i] == '>':
                if line_elements[i + 1] == '=':
                    final_line_tokens.append('>=')
                    i = i + 1
                else:
                    final_line_tokens.append('>')
            elif line_elements[i] == 'end' and i + 1 < n:
                tmp_token = line_elements[i]
                if line_elements[i + 1] == '_' and i + 2 < n:
                    if line_elements[i + 2] in ['if', 'while', 'for']:
                        tmp_token += '_' + line_elements[i + 2]
                        final_line_tokens.append(tmp_token)
                        i += 2
                    else:
                        raise ValueError("Lexical error: Invalid token {} on line {}".format(
                            line_elements[i] + line_elements[i + 1] + line_elements[i + 2], self._lineCount))
                # else:
                #     raise ValueError(
                #         "Invalid token of type end before end of program is reached: line {}".format(self._lineCount))
            else:
                final_line_tokens.append(line_elements[i])
            i = i + 1

        return final_line_tokens

    def classifyToken(self, token):
        """
        Classify a token either as an identifier or a constant
        :param token:
        :return:
        """
        # identifier - letter{letter|digit}
        match = re.match('^[a-zA-Z]+[a-zA-Z0-9_]*$', token)
        if match is not None:
            return 1

        # constant
        # string constant - """{character}"""
        # character - 'letter|digit'
        # integer - "0"|["+"|"-"]nzDigit{digit}
        string_match = re.match('^\"[a-zA-Z0-9]+\"$', token)
        if string_match is not None:
            return 2
        else:
            char_match = re.match('^\'[a-zA-Z0-9\'$]', token)
            if char_match is not None:
                return 3
            else:
                int_match = re.match('^0$|^(\+|-)?[1-9][0-9]*$', token)
                if int_match is not None:
                    return 4

        return 0
