import sys
import collections
import re


class TextFile(object):
    def __init__(self, filename):
        with open(filename, 'r') as text_file:
            self._text = text_file.read().lower()
        self._word_counter = None

    def getWordFreq(self, n=None):
        if self._word_counter is None:
            words = re.findall(r'\w+', self._text)
            self._word_counter = collections.Counter(words)
        return self._word_counter.most_common(n)


def printMenu():
    print('0, Exit')
    print('1. Get word frequency')
    print('2. Get most common N words')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit('Usage: python main.py <text_filename>')

    filename = sys.argv[1].strip()
    text_file = TextFile(filename)

    while True:
        printMenu()
        usr_input = input()
        if usr_input == '0':
            break
        elif usr_input == '1':
            with open('word_frequency.csv', 'w') as word_frequency_file:
                for data in text_file.getWordFreq():
                    word_frequency_file.write('{},{}\n'.format(*data))
        elif usr_input == '2':
            n = int(input('Enter number of words: '))
            for data in text_file.getWordFreq(n):
                print('{}\t{}'.format(*data))