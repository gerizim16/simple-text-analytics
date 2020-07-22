import sys
import os
import string
import collections
from pathlib import Path

import xlsxwriter
import nltk
from nltk.text import Text


def main():
    # Check arguments
    if not (2 <= len(sys.argv) <= 3):
        sys.exit('Usage: python main.py <text_filename> [file_encoding]')
    filename, fileext = os.path.splitext(sys.argv[1])
    encoding = None
    if len(sys.argv) == 3:
        encoding = sys.argv[2]

    # Create output folder and define paths
    OUTPUT_FOLDER = 'results_' + filename
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    FREQ_DIST_PATH = os.path.join(OUTPUT_FOLDER,
                                  'frequency_distribution_' + filename)
    CONCORDANCE_PATH = os.path.join(OUTPUT_FOLDER, 'concordance_' + filename)
    TEXT_CLUSTERING_PATH = os.path.join(OUTPUT_FOLDER,
                                        'text_clustering_' + filename)
    SENT_PATH = os.path.join(OUTPUT_FOLDER, 'sentence')

    # Open file
    text_string = None
    with open(filename + fileext, 'r', encoding=encoding) as text_file:
        text_string = text_file.read()
    text = Text(nltk.word_tokenize(text_string))

    # Create frequency distribution of words
    stopwords = set(nltk.corpus.stopwords.words('english'))
    punctuations = set(string.punctuation)

    freq_dist = nltk.FreqDist(word.lower() for word in text
                              if word not in punctuations)
    # Save to csv
    with open(FREQ_DIST_PATH + '.csv', 'w',
              encoding=encoding) as freq_dist_file:
        freq_dist_file.write('word,frequency\n')
        for data in freq_dist.most_common():
            freq_dist_file.write('{},{}\n'.format(*data))
            # print('{}\t{}'.format(*data))

    # Create concordance
    keys = list()
    print(
        'Enter the words you want to search for concordance and text clustering: (enter nothing to end)'
    )
    while (True):
        key = input().strip().lower()
        if key in (None, '\n', ''):
            break
        keys.append(key)

    # Save to csv and txt
    with open(CONCORDANCE_PATH + '.tsv', 'w',
              encoding=encoding) as conc_tsv, open(
                  CONCORDANCE_PATH + '.txt', 'w',
                  encoding=encoding) as conc_txt:
        conc_tsv.write('left Context\tword\tright context\n')

        for key in keys:
            concordance = text.concordance_list(key, width=150, lines=None)
            for concordance_line in concordance:
                # print(concordance_line.line)
                conc_tsv.write('{}\t{}\t{}\n'.format(
                    concordance_line.left_print, concordance_line.query,
                    concordance_line.right_print))
                conc_txt.write(concordance_line.line + '\n')

    # Create text clustering
    sentences = list(
        nltk.word_tokenize(sentence)
        for sentence in nltk.sent_tokenize(text_string))
    workbook = xlsxwriter.Workbook(TEXT_CLUSTERING_PATH + '.xlsx')
    worksheet_summary = workbook.add_worksheet('summary')

    for i, key in enumerate(keys):
        counter = collections.Counter()

        for sentence in sentences:
            sentence = tuple(map(str.lower, sentence))
            if key in sentence:
                counter.update(sentence)

        worksheet_summary.write(0, i * 2, key)
        for row, data in enumerate(counter.most_common(), 1):
            worksheet_summary.write(row, i * 2, data[0])
            worksheet_summary.write(row, i * 2 + 1, data[1])

    workbook.close()

    # Create sentences and save to tsv file
    workbook = xlsxwriter.Workbook(SENT_PATH + '.xlsx')
    worksheet_summary = workbook.add_worksheet('summary')
    for i, key in enumerate(keys):
        worksheet_summary.write(0, i, key)
        row = 1
        for sentence in sentences:
            if key in tuple(map(str.lower, sentence)):
                worksheet_summary.write(row, i, ' '.join(sentence))
                row += 1
    
    workbook.close()


if __name__ == '__main__':
    main()