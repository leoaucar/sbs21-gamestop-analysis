# coding: utf-8
from psaw import PushshiftAPI
import pandas as pd
import datetime as dt

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

api = PushshiftAPI()
start_epoch = int(dt.datetime(2021, 1, 10).timestamp())
end_epoch = int(dt.datetime(2021, 2, 10).timestamp())
gen = api.search_submissions(
    after=start_epoch,
    before=end_epoch,
    subreddit="wallstreetbets",
    sort="desc",
    sort_type="num_comments",
    #limit=100,
    )

df = pd.DataFrame([obj.d_ for obj in gen])
df = df[['id', 'author', 'title', 'url', 'created_utc', 'num_comments' ]]

df.to_csv('posts_jan_feb.csv', index=False)
