import os
import sys
import tweepy
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


query, bearer_token = load()
client: tweepy.Client = tweepy.Client(bearer_token=bearer_token)
response: tweepy.Response = client.search_recent_tweets(
        query,
        max_results=100
 )
