import vk
import re
import os
import requests
vk_session = vk.API(access_token='02b8aaf902b8aaf902b8aaf92d01a963e2002b802b8aaf961282e7e08d73d16fe180447', v='5.81', lang='ru')

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
# print(emoji_pattern.sub('', result[0]['text']))

groups_dict = {
    'treugolnikrockbar': -566218,
    'rockbasebar': -176573126,
}
def get_reposts_img_and_txt(count, offset, group_list=None):
    result = dict(vk_session.wall.get(domain='treugolnikrockbar', count=count, offset=offset))['items']
    
    for entry in result:
        if 'copy_history' in entry:
            print(entry['copy_history'])
            if 'photo' in entry['copy_history'][0]['attachments'][0]:
                image_url = entry['copy_history'][0]['attachments'][0]['photo']['sizes'][-1]['url']
            else:
                print('No images...Break!')
                continue
            response = requests.get(image_url, stream=True)
            img = open(f"{entry['copy_history'][0]['owner_id']}_{entry['copy_history'][0]['date']}.jpg",'wb')
            text = open(f"{entry['copy_history'][0]['owner_id']}_{entry['copy_history'][0]['date']}.txt",'wb')
            text.write(entry['copy_history'][0]['text'].encode('UTF-8'))
            for block in response.iter_content(1024):
                if not block:
                    break
                img.write(block)
        else:
            print(entry)
            if 'photo' in entry[0]['attachments'][0]:
                image_url = entry[0]['attachments'][0]['photo']['sizes'][-1]['url']
            else:
                print('No images...Break!')
                continue


def get_group_topics(group_id: int):
    result = dict(vk_session.board.getTopics(group_id=group_id))
    print(result)

def search_price(filename: str):
    file = open(filename, 'r')
    # regex price = (?:[В|в]ход|[[Ц|ц]ена|[С|с]тоимость) {0,}(\d{3,4}) ищет со словом, захватывает только 3-4 цифры
    # phone = \d{11}
    # date = (\d{2})(?:0.|:|-|\/|\\){1}(\d{2})(?2){0,1}(\d{0,4}) not working
# get_group_topics(176573126)