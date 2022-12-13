from domain.grammar import Grammar
from domain.parser import Parser
from domain.parserOutput import ParserOutput
from tests import Tests

if __name__ == '__main__':
    grammar = Grammar()
    grammar.readFromFile("g1.txt")
    parser = Parser(grammar)
    print('Input sequence to be parsed: ')
    sequence = input()
    parser.parsingStrategy(sequence)

    if parser.getState() == 'f':
        out = ParserOutput(parser.getTree())
        out.printTree()


