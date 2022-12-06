class Tests:
    def __init__(self, parser):
        self.parser = parser

    def test_momentaryInsucces(self):
        self.parser.momentaryInsuccess()
        assert self.parser.getState(), 'b'

    def test_advance(self):
        self.parser.setInputStack(['a', 'A'])
        self.parser.setWorkingStack([('S', 0)])
        self.parser.setIndex(1)
        self.parser.advance()
        assert self.parser.getIndex(), 2
        assert self.parser.getInputStack(), ['A']
        assert self.parser.getWorkingStack(), ['a']

    def test_expand(self):
        self.parser.setInputStack(['S'])
        self.parser.setWorkingStack([])
        self.parser.setIndex(1)
        self.parser.expand()
        assert self.parser.getInputStack(), ['a', 'A']
        assert self.parser.getWorkingStack(), [('S', 0)]
        assert self.parser.getIndex(), 1

    def test_success(self):
        self.parser.success()
        assert self.parser.getState(), "f"

    def test_back(self):
        self.parser.setState("b")
        self.parser.setIndex(2)
        self.parser.setWorkingStack([("S", 1), "a"])
        self.parser.setInputStack(["b", "c"])
        self.parser.back()

        assert self.parser.getWorkingStack(), [("S", 1)]
        assert self.parser.getInputStack(),["a","b","c"]

    def test_anotherTry(self):
        self.parser.setState("b")
        self.parser.setIndex(2)
        self.parser.setWorkingStack([("S", 1), "a", ("A", 2)])
        self.parser.setInputStack(["a", "A"])
        self.parser.anotherTry()

        assert self.parser.getWorkingStack(), [("S", 1), "a", ("A", 3)]
        assert self.parser.getInputStack(), ["b", "A"]

        self.parser.anotherTry()
        self.parser.anotherTry()
        self.parser.anotherTry()

        assert self.parser.getWorkingStack(), [("S", 1), "a"]
        assert self.parser.getInputStack(),["A"]

    def run(self):
        self.test_momentaryInsucces()
        self.test_advance()
        self.test_expand()
        self.test_success()
        self.test_back()
        self.test_anotherTry()


