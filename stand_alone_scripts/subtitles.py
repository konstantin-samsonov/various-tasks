"""
Converting files with subtitles to txt format for further loading into Quizlet cards.
The resulting file contains unique words from subtitles with translation into Russian.
"""


import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from modules.gcp_translate import translate_text
import tqdm

PATH = '../data/mandalorian_se_01/'


def get_file_name(path):
    files = [file for file in os.listdir(path)]
    return files


def get_keywords(path):
    """Returns a list of words from a .srt file"""

    file = open(path, 'r')
    lines = file.readlines()
    file.close()

    keywords_raw = []
    for line in lines:
        if re.match(r"([^_][A-z]+)", line):
            keywords_raw.append(line.strip())

    # tokenization
    vectorizer = CountVectorizer()
    vectorizer.fit_transform(keywords_raw)
    keywords_tokens = vectorizer.get_feature_names_out()

    result = []
    for keyword in keywords_tokens:
        if not keyword.isdigit():
            result.append(keyword)

    return result


def main(path, out_file_name):
    files = get_file_name(path)

    all_keywords = []
    for file in files:
        chapter = get_keywords(f'{path}{file}')
        all_keywords += chapter
    all_keywords = set(all_keywords)

    # translate
    result = {}
    for i in tqdm.tqdm(all_keywords):
        result[i] = translate_text(i)

    # save file
    f = open(f'{out_file_name}.txt', 'w')
    for key, val in result.items():
        f.write(f'{key} - {val}\n')
    f.close()


if __name__ == '__main__':
    main(PATH, 'mandalorian_se01_all_keywords')
