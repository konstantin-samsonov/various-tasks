import pandas as pd
import requests
from modules.gcp_sheets import download_sheet, upload_sheet
from tqdm import tqdm



def get_data(word):
    """Returns json data by words"""

    url = f"https://dictionary.yandex.net/dicservice.json/lookupMultiple?sid=1fca38c5.629b1126.b14f093c.74722d74657874&ui=ru&srv=tr-text&text={word}&type=regular%2Csyn%2Cant%2Cderiv&lang=en-ru&flags=15783&dict=en-ru.regular%2Cen.syn%2Cen.ant%2Cen.deriv&yu=4883800491645551089&yum=1652347526500158743"
    params = {
        "headers": {
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "Referer": "https://translate.yandex.ru/?lang=en-ru&text=around",
            "Referrer-Policy": "no-referrer-when-downgrade"
        },
        "body": None,
        "method": "GET"
    }

    headers = params['headers']
    body = params['body']
    if params['method'] == 'GET':
        result = requests.get(url, headers=headers)
        return result.json()
    if params['method'] == 'POST':
        result = requests.post(url, headers=headers, body=body)
        return result.json()


def get_translate(data):
    # We process the results in which only idioms.
    if 'card' in data['head'].keys():
        translate = '[ - ]'
        example = data['en-ru']['def'][0]['tr'][0]['def']
        return translate, f'[{example}];'

    # We process the results with different options.
    else:
        # The answer may contain many "lines" with results depending on the part of speech to which the word refers.
        # Now, for the simplicity of the script, we will collect only information from the first "line"
        # with one word form.
        first_rows = data['en-ru']['regular'][0]

        # translate
        pos = first_rows['pos']['tooltip']
        translate = []
        for i in first_rows['tr']:
            translate.append(i['text'])

        # translate = ', '.join(translate)

        # examples
        examples = []
        if 'ex' in first_rows['tr'][0].keys():
            all_examples = first_rows['tr'][0]['ex']

            for example in all_examples:
                result = f"{example['text']} - {example['tr'][0]['text']}"
                examples.append(result)

        def get_max_len_example(lst, fallback=''):
            return max(lst, key=len) if lst else fallback

        example = get_max_len_example(examples)

        if len(example) > 0:
            return f'{translate}', f'[{example}];'
        else:
            return f'{translate}', f'[ - ];'

def get_raw_word(start, stop):
    sheets_file = 'https://docs.google.com/spreadsheets/d/1gEjFuNyljZ9eS4iWZuLZ4dKkBdltd7R2l-9xAId54Ho/edit#gid=1079817712'
    sheets_list = 'raw_data'
    data = download_sheet(sheets_file, sheets_list)
    result = data['word'][start:stop].tolist()
    return result


if __name__ == '__main__':
    raw_words = get_raw_word(0, 500)
    for word in tqdm(raw_words):
        try:
            data = get_data(word)
            translate, example = get_translate(data)
            string = f"{word},{translate}\n{example}"
            with open('../data/first_500_word.txt', 'a') as the_file:
                the_file.write(f'{string}')
        except:
            print(word)

