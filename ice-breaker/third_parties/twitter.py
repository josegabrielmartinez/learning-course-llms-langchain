import requests


def scrape_user_tweets(username: str, num_tweets: int = 5, mock: bool = False):
    """
    Scrapes a Twitter user's original tweets and return them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    :param username: username of the user in twitter
    :param num_tweets: number of tweets to scrap
    :param mock: True if we want to use the mock file instead of twitter API (cost money)
    :return: list of tweets
    """
    tweet_list = []
    # I'm not implementing the Twitter API calls because cost money, must the mocking part
    twitter_url = "https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json"
    tweets = requests.get(
        twitter_url,
        timeout=10,
    ).json()

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    tweets = scrape_user_tweets(username="Eden Marco", num_tweets=5, mock=True)
    print(tweets)
