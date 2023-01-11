from domain.grammar import Grammar
from domain.parser import Parser
from domain.parserOutput import ParserOutput
from tests import Tests

if __name__ == '__main__':
    grammar = Grammar()
    # grammar.readFromFile("g1.txt")
    grammar.readFromFile("g2.txt")
    # parser = Parser(grammar, "out1.txt", "seq.txt")
    parser = Parser(grammar, "out2.txt", "PIF.out")
    # parser = Parser(grammar, "out2.txt")
    print('Input sequence to be parsed: ')
    sequence = '' #input()
    parser.parsingStrategy(sequence)

    if parser.getState() == 'f':
        out = ParserOutput(parser.getTree())
        out.printTree()
        out.printFile("out2.txt")
        # out.printFile("out1.txt")


