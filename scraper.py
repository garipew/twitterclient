import os
import sys
import tweepy
import pandas as pd
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

query, bearer_token = load()
client: tweepy.Client = tweepy.Client(bearer_token=bearer_token)
response: tweepy.Response = client.search_recent_tweets(
        query,
        tweet_fields=["created_at", "author_id", "text", "like_count"],
        expansions=["author_id"],
        user_fields=["username"],
        max_results=100
)
users = {user["author_id"] : user["username"] for user in response.includes["users"]}

tweets = []
for tweet in response.data:
    tweets.append({
        "id": tweet.id,
        "created_at": tweet.created_at,
        "author": users[tweet.author_id],
        "text": tweet.text.replace("\n", " "),
        "likes": tweet.like_count,
        })

save_to_csv(tweets, query)
