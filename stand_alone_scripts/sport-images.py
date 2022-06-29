"""


"""

import re
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

MAIN_URL = 'https://www.sport-images.ru'
EVENT_URL = '/events/ecofest-ruskeala-swim-2022/tags/swim2/'
EVENT_PAGE_NUMBER = range(1, 123 + 1)


# Step 01 - get all urls photo and name photo
def get_data_from_page(main_url=MAIN_URL, event_url=EVENT_URL, page=None):
    html = urlopen(f'{main_url}{event_url}?page={page}')
    bs = BeautifulSoup(html.read(), 'lxml')
    page_data = bs.find('div', {'class': 'photo-wrap'})
    links = page_data.find_all('a')
    result = {}
    for link in links:
        href = link['href']
        src = link.find('img')['src']
        result[href] = src

    return result


# # save url_foto and name to file
# for page in tqdm(EVENT_PAGE_NUMBER):
#     raw_data = get_data_from_page(page=page)
#     df_tmp = pd.DataFrame.from_dict(raw_data, orient='index').reset_index()
#     df_tmp.to_csv('t.csv', mode='a', header=False)


# Step 02 - get preview photo
df = pd.read_csv('t.csv', header=None, names=['href', 'src'])
df.reset_index(drop=True, inplace=True)

for i in tqdm(df['src']):
    file_name = re.findall('\w+.jpg', i)
    file_url = f"{MAIN_URL}{i}"
    urlretrieve(file_url, f'../data/photo/{file_name[0]}')


