import os
import re
import json
from tqdm import tqdm


def get_all_json_files(path=None):
    """Return list all json files in directory"""

    result = []
    for i in os.listdir(path):
        if re.search(r'json', i):
            result.append(i)

    return result


def get_metadata(path=None, file=None):
    """Returns main metadata from json file"""

    with open(f'{path}/{file}') as f:
        data = json.load(f)
        file_title = data['title']

        if 'photoTakenTime' in data.keys():
            file_create = data['photoTakenTime']['timestamp']
        elif 'date' in data.keys():
            file_create = data['date']['timestamp']
        else:
            file_create = 'no_date_create'

    return file_title, file_create


def rename_file(path=None, file=None, name=None):
    """Renames file"""

    full_name = file.split('.')
    if len(full_name) > 1:
        file_title = full_name[0]
        file_extension = full_name[1]

        os.rename(f'{path}/{file}', f'{path}/{file}/{name}.{file_extension}')

    else:
        file_title = full_name[0]


if __name__ == '__main__':
    path = '../data/google_photo_archive/2022'
    all_json = get_all_json_files(path)

    for json_file in tqdm(all_json):
        file_full_name, file_create = get_metadata(path, json_file)
        extension = file_full_name.split('.')

        try:
            if len(extension) > 1:
                old_name = f'{path}/{file_full_name}'
                new_name = f'{path}/{file_create}.{extension[1]}'
                os.rename(old_name, new_name)
                os.remove(f'{path}/{json_file}')

            else:
                old_name = f'{path}/{file_full_name}'
                new_name = f'{path}/{file_create}'
                os.rename(old_name, new_name)
                os.remove(f'{path}/{json_file}')

        except Exception as e:
            print(json_file, e)


