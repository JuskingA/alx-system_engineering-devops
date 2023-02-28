import requests

def count_words(subreddit, word_list, instances=None):
    if instances is None:
        instances = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Invalid subreddit: {subreddit}")
        return

    data = response.json()["data"]
    after = data["after"]
    for post in data["children"]:
        title = post["data"]["title"].lower()
        for word in set(word_list):
            if word.lower() in title and not any(
                prefix in title for prefix in [f"{word}.", f"{word}!", f"{word}_"]
            ):
                instances[word] = instances.get(word, 0) + title.count(word.lower())

    if after is None:
        counts = sorted(
            [(k.lower(), v) for k, v in instances.items() if k.lower() in word_list],
            key=lambda x: (-x[1], x[0])
        )
        for word, count in counts:
            print(f"{word.lower()}: {count}")
        return

    count_words(subreddit, word_list, instances)
