import sys
import os
from pathlib import Path
import nltk
from nltk.text import Text
import string


def main():
    # Check arguments
    if not (2 <= len(sys.argv) <= 3):
        sys.exit('Usage: python main.py <text_filename> [file_encoding]')
    filename = sys.argv[1].strip()
    encoding = None
    if len(sys.argv) == 3:
        encoding = sys.argv[2]

    # Create output folder and define paths
    OUTPUT_FOLDER = 'results_' + filename
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    FREQ_DIST_PATH = os.path.join(
        OUTPUT_FOLDER, 'frequency_distribution_' + filename + '.csv')
    CONCORDANCE_TSV_PATH = os.path.join(OUTPUT_FOLDER,
                                        'concordance_' + filename + '.tsv')
    CONCORDANCE_TXT_PATH = os.path.join(OUTPUT_FOLDER,
                                        'concordance' + filename + '.txt')

    # Open file
    with open(filename, 'r', encoding=encoding) as text_file:
        text = Text(nltk.word_tokenize(text_file.read()))

    # Create frequency distribution of words
    stopwords = set(nltk.corpus.stopwords.words('english'))
    punctuations = set(string.punctuation)

    freq_dist = nltk.FreqDist(word.lower() for word in text
                              if word not in stopwords | punctuations)
    # Save to csv
    with open(FREQ_DIST_PATH, 'w', encoding=encoding) as freq_dist_file:
        freq_dist_file.write('word,frequency\n')
        for data in freq_dist.most_common():
            freq_dist_file.write('{},{}\n'.format(*data))
            print('{}\t{}'.format(*data))

    # Create concordance
    concordance_keys = list()
    print(
        'Enter the words you want to search for concordance: (enter "!" to end)'
    )
    while (True):
        key = input().strip()
        if key == '!':
            break
        concordance_keys.append(key)

    # Save to csv and txt
    with open(CONCORDANCE_TSV_PATH, 'w', encoding=encoding) as conc_tsv, open(
            CONCORDANCE_TXT_PATH, 'w', encoding=encoding) as conc_txt:
        conc_tsv.write('left Context\tword\tright context\n')
        
        for key in concordance_keys:
            concordance = text.concordance_list(key, width=150, lines=None)
            for concordance_line in concordance:
                print(concordance_line.line)
                conc_tsv.write('{}\t{}\t{}\n'.format(
                    concordance_line.left_print, concordance_line.query,
                    concordance_line.right_print))
                conc_txt.write(concordance_line.line + '\n')


if __name__ == '__main__':
    main()