from domain.grammar import Grammar

if __name__ == '__main__':
    grammar = Grammar()
    grammar.readFromFile("g1.txt")
    print('Non-terminals:')
    print(grammar.printNonTerminals())
    print('Alphabet:')
    print(grammar.printAlphabet())
    print('Starting symbol: ')
    print(grammar.printStartingSymbol())
    print('Productions:')
    print(grammar.printProductions())
