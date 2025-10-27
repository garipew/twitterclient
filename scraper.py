import os
import sys
import time
import tweepy
import pandas as pd
from typing import cast
from dotenv import load_dotenv

def panic(msg):
    print(msg)
    exit(1) 

def load():
    if len(sys.argv) < 2:
        panic("Usage: python ./scraper.py <query>")
    query = sys.argv[1]

    envs = load_dotenv() 
    if not envs:
        panic("scrape: Missing .env file")

    bearer_token = os.getenv("BEARER_TOKEN")
    if not bearer_token:
        panic("scrape: Missing BEARER_TOKEN in .env")
    return query, bearer_token

def save_to_csv(tweets, query, filename="tweets.csv"):
    df = pd.DataFrame(tweets)
    df["query"] = query

    if os.path.exists(filename):
        df.to_csv(filename, mode="a", index=False, header=False)
    else:
        df.to_csv(filename, index=False)

def collect_tweets(query, client, since_id=None, pages=5):
    tweets = []

    paginator = tweepy.Paginator(
            client.search_recent_tweets,
            query,
            tweet_fields=["created_at", "author_id", "text", "public_metrics"],
            expansions=["author_id"],
            user_fields=["username"],
            max_results=100,
            since_id=since_id,
            limit=pages
            )

    for response in paginator:
        response = cast(tweepy.Response, response)
        if not response.data:
            continue
        users = {user.id : user.username for user in response.includes["users"]}
        for tweet in response.data:
            tweets.append({
                "id": tweet.id,
                "created_at": tweet.created_at,
                "author": users[tweet.author_id],
                "text": tweet.text.replace("\n", " "),
                "likes": tweet.public_metrics["like_count"],
                })
    return tweets

query, bearer_token = load()
client: tweepy.Client = tweepy.Client(bearer_token=bearer_token)
while True:
    print("Collecting tweets...")
    tweets = collect_tweets(query, client)
    if(tweets):
        save_to_csv(tweets, query)
        print(f'Saved {len(tweets)} tweets.')
    print('Preparing for the next request...')
    time.sleep(900)
