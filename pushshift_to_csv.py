# coding: utf-8
import logging
from psaw import PushshiftAPI
import pandas as pd
import datetime as dt

# logging config's
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger = logging.getLogger('psaw')
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def unix_to_utc(utc_dt):
    """
    Convers unix to UTC time.
    """
    return pd.to_datetime(utc_dt, unit='s')


def gen_search(date_range):
    """
    Yield responses from multiple queries.
    """
    api = PushshiftAPI()
    for date in date_range:
        date = int(date)
        delta = int(dt.timedelta(days=1).total_seconds())
        yield from api.search_submissions(
            after=date,
            before=date + delta,
            subreddit="wallstreetbets",
            sort="desc",
            sort_type="num_comments",
            filter=['id', 'author', 'title', 'url', 'created_utc', 'num_comments'],
            limit=1000,
            max_results_per_request=1000
        )


# get main query's date range list
start_date = int(dt.datetime(2021, 1, 10).timestamp())
date_list = [start_date + int(dt.timedelta(days=x).total_seconds()) for x in range(31)]
gen = gen_search(date_list)

# output data to CSV
df = pd.DataFrame([obj.d_ for obj in gen])
df['created_utc_converted'] = df['created_utc'].apply(unix_to_utc)
df.drop_duplicates(inplace=True)
df.to_csv('posts_jan_feb.csv', index=False)
