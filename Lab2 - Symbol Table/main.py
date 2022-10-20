from SymbolTable import SymbolTable

# 2 symbol tables - 1 for identifiers, 1 for constants
if __name__ == '__main__':
    identifiersTable = SymbolTable()
    constantsTable = SymbolTable()
    identifiersTable.add('key')
    identifiersTable.add('hello')
    identifiersTable.add('world')
    identifiersTable.add('ad')
    identifiersTable.add('bc')
    identifiersTable.add('c')
    identifiersTable.add('d')
    identifiersTable.add(13)
    # print(identifiersTable.getPos('world'))
    # print(identifiersTable.getPos(13))
    # print(identifiersTable.getPos('nothing'))
    print(identifiersTable)
