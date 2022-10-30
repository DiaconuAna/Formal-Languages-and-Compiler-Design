# This is a sample Python script.
from Scanner import Scanner


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def test_p1():
    file = open('p1.txt', 'r')
    scanner = Scanner(file.read())


def test_p1err():
    file = open('p1err.txt', 'r')
    scanner = Scanner(file.read())


def test_p2():
    file = open('p2.txt', 'r')
    scanner = Scanner(file.read())


def test_p3():
    file = open('p3.txt', 'r')
    scanner = Scanner(file.read())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_p1()
    # test_p2()
    # test_p3()
    # test_p1err()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
