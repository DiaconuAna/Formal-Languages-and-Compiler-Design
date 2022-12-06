from domain.grammar import Grammar
from domain.parser import Parser
from tests import Tests

if __name__ == '__main__':
    grammar = Grammar()
    grammar.readFromFile("g1.txt")
    parser = Parser(grammar)
    tests = Tests(parser)
    tests.run()
    # print('Non-terminals:')
    # print(grammar.printNonTerminals())
    # print('Alphabet:')
    # print(grammar.printAlphabet())
    # print('Starting symbol: ')
    # print(grammar.printStartingSymbol())
    # print('Productions:')
    # print(grammar.printProductions())

