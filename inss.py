import json
import time
import os
import sys
from instagrapi import Client
MEDIA_TYPES_GQL = {"GraphImage": 1, "GraphVideo": 2, "GraphSidecar": 8, "StoryVideo": 2}

cl = Client()
cl.login('xxxxx', 'xxxx')
# json.dump(
#     cl.get_settings(),
#     open('./file.json', 'w')
# )
# cl = Client(json.load(open('./file.json')))

def getInsImgs(name):
    user_id = cl.user_id_from_username(name)
    variables = {
        "id": user_id,
        "first": 10,
    }
    end_cursor = None
    variables["after"] = None
    sum = 0
    while True:
        if end_cursor:
            variables["after"] = end_cursor
        data = cl.public_graphql_request(
            variables, query_hash="e7e2f4da4b02303f74f0841279e52d76"
        )
        for edge in data['user']['edge_owner_to_timeline_media']['edges']:
            box = {
                "display_url": "",
                "tag": []
            }
            node = edge['node']
            mediaType = MEDIA_TYPES_GQL[node['__typename']]
            if mediaType == 8:
                for single_node in node['edge_sidecar_to_children']['edges']:
                    if MEDIA_TYPES_GQL[single_node['node']['__typename']] == 1:
                        if len(single_node['node']['edge_media_to_tagged_user']['edges']) >0:
                            box['display_url'] = single_node['node']['display_url']
                            for tag in single_node['node']['edge_media_to_tagged_user']['edges']:
                                box["tag"].append([tag['node']['user']['username'], [tag['node']['x'],tag['node']['y']]])
                            json_data = json.dumps(box)
                            with open('/Users/mac/Desktop/pyton/crawler-py/imgs/'+name+'.txt', 'a') as f:
                                sum = sum +1
                                f.write(json_data + '\n')
            if mediaType == 1:
                if len(node['edge_media_to_tagged_user']['edges']) > 0:
                    box['display_url'] = node['display_url']
                    for tag in node['edge_media_to_tagged_user']['edges']:
                            box["tag"].append([tag['node']['user']['username'], [tag['node']['x'],tag['node']['y']]])
                    json_data = json.dumps(box)
                    with open('/Users/mac/Desktop/pyton/crawler-py/imgs/'+name+'.txt', 'a') as f:
                        sum = sum +1
                        f.write(json_data + '\n')
        end_cursor = data['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        if not data['user']['edge_owner_to_timeline_media']['page_info']['has_next_page'] or not end_cursor or sum > 5000:
            break
                    
if __name__ == "__main__":
    file_name = sys.argv[1]
    if file_name:
        print(file_name)
        with open(file_name, 'r') as f:
            for line in f:
                time.sleep(120) 
                print('start crawler ' +line.strip())
                try:
                    getInsImgs(line.strip())
                except Exception as e:
                    print(e)
                    file_path = '/Users/mac/Desktop/pyton/crawler-py/imgs/'+line.strip()+'.txt'
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    continue