from tabulate import tabulate


class ParserOutput:
    def __init__(self, tree):
        self._tree = tree

    def printTree(self):
        headers = ['Index', 'Value', 'Parent', 'Left Sibling']
        rows = []
        index = 0
        for item in self._tree:
            rows.append([index, item.value, item.father, item.sibling])
            index += 1
        print(tabulate(rows, headers, tablefmt='orgtbl'))

    def printFile(self, filename):
        headers = ['Index', 'Value', 'Parent', 'Left Sibling']
        rows = []
        index = 0
        for item in self._tree:
            rows.append([index, item.value, item.father, item.sibling])
            index += 1
        with open(filename, 'a') as writer:
            writer.write('\n')
            writer.write(tabulate(rows, headers, tablefmt='orgtbl'))
