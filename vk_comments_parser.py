from typing import List, Tuple
import requests

TOKEN = "token"


def get_groups(query: str) -> List[str]:
    group_ids = []
    res = requests.get(
        'https://api.vk.com/method/groups.search',
        params={
            'q': query,
            'access_token': TOKEN,
            'count': 1000,
            'v': '5.199',
        }
    )
    counter = res.json()["response"]["count"]
    for i in range(counter):
        group_ids.append(res.json()["response"]["items"][i]["id"])
    return group_ids


def count_posts(owner_id: str) -> Tuple[int, List[str], List[int]]:
    res = requests.get(
        'https://api.vk.com/method/wall.get',
        params={
            'owner_id': "-"+owner_id,
            'access_token': TOKEN,
            'count': 100,
            'v': '5.199',
        }
    )
    counter = res.json()["response"]["count"]
    items_100_1st = res.json()["response"]["items"]
    texts_100_1st = []
    ids_100_1st = []

    for i in range(100):
        ids_100_1st.append(items_100_1st[i]["id"])
        if len(texts_100_1st) == 0:
            texts_100_1st.append(items_100_1st[i]["text"])
        elif len(texts_100_1st) > 0 and items_100_1st[i]["text"] != texts_100_1st[-1]:
            texts_100_1st.append(items_100_1st[i]["text"])

    return counter, texts_100_1st, ids_100_1st


def get_posts(owner_id: str) -> Tuple[List[int], List[str]]:
    quantity = count_posts(owner_id)[0] - 100
    posts_texts = count_posts(owner_id)[1]
    posts_ids = count_posts(owner_id)[2]
    num_iter = quantity//100
    offset = 100
    if quantity % 100 > 0:
        num_iter += 1

    for i in range(num_iter):
        res = requests.get(
            'https://api.vk.com/method/wall.get',
            params={
                'owner_id': "-"+owner_id,
                'offset': offset,
                'access_token': TOKEN,
                'count': 100,
                'v': '5.199',
            }
        )
        offset += 100
        posts_items = res.json()["response"]["items"]

        for j in range(len(posts_items)):
            posts_ids.append(posts_items[i]["id"])
            if len(posts_texts) == 0:
                posts_texts.append(posts_items[i]["text"])
            elif len(posts_texts) > 0 and posts_items[i]["text"]!= posts_texts[-1]:
                posts_texts.append(posts_items[i]["text"])

    return posts_ids, posts_texts


def get_comments(owner_id: str, post_ids: List[int]) -> List[str]:
    texts = []
    for post_id in post_ids:
        res = requests.get(
                'https://api.vk.com/method/wall.getComments',
                params={
                    'owner_id': "-"+owner_id,
                    'post_id': post_id,
                    'access_token': TOKEN,
                    'count': 100,
                    'v': '5.199',
                }
            )
        for j in res.json()["response"]["items"]:
            if len(texts) == 0:
                texts.append(j["text"])
            elif len(texts) > 0 and j["text"] != texts[-1]:
                texts.append(j["text"])
    return texts


def parsing():
    print("Input your query:")
    query = str(input())
    print("Searching groups...")
    groupids = get_groups(query)
    print(f"Groups found: {len(groupids)}. Do you want to crop the list? y/n")
    response = str(input()).lower()
    if response == "y":
        print("How many items do you want to leave in the list? Input your number:")
        crop = int(input())
        groupids = groupids[:crop]
    elif response == "n":
        groupids = groupids
    print("Ok! Saving posts to the file...")
    for groupid in groupids:
        getposts = get_posts(str(groupid))
        postids = getposts[0]
        posttexts = getposts[1]
        for posttext in posttexts:
            with open("posts_texts.txt", "a", encoding="utf-8") as posts:
                posts.write(posttext+'\n'+'_____'+'\n')
        print("The posts have been saved. Let's get the comments!")
        comment_texts = get_comments(str(groupid), postids)
        for postcomment in comment_texts:
            with open("posts_comments.txt", "a", encoding="utf-8") as posts:
                posts.write(postcomment+'\n'+'_____'+'\n')
    print("You're all set!")
    return 0


if __name__ == '__main__':
    parsing()
