from twitterscraper import query_tweets
import pandas as pd
import datetime as dt

'''
Use twitterscraper package from GitHub
(installed using "pip3 install twitterscraper")
to count the number of mentions of a coin or #[its ticker]
on Twitter on March 1st, 2018. Stop counting after 1000 mentions.
Create a CSV file containing the number of mentions for each
of the 250 coins of interest. 

'''
if __name__ == '__main__':
    coin_df = pd.read_csv("Updated_Cryptocoins.csv")
    all_coins = [x.lower() for x in coin_df["Name"]][0:250]
    all_tickers = list(coin_df["Symbol"])[0:250]
    coin_tuples = list(zip(all_coins, all_tickers))
    start_date = dt.date(2018, 3, 1)
    end_date = dt.date(2018, 3, 2)
    num_list = []
    df_dict = {}
    for tup in coin_tuples:
        tweet_list = query_tweets(tup[0] + " OR #" + tup[1], \
            limit = 1000, begindate=start_date, enddate=end_date, \
            poolsize = 1, lang = '')
        if len(tweet_list) > 1000:
            num_list.append(1000)
        else:
            num_list.append(len(tweet_list))
        print(tup)
        print(num_list)
    df_dict["Coin_Name"] = all_coins
    df_dict["Twitter_Mentions"] = num_list
    df = pd.DataFrame(df_dict)
    df.to_csv("dataframes/twitter.csv")

'''
UNUSED BECAUSE TOO SLOW
if __name__ == '__main__':
    coin_df = pd.read_csv("Cryptocoins.csv")
    all_coins = [x.lower() for x in coin_df["Name"]][0:1]
    all_tickers = list(coin_df["Symbol"])[0:1]
    coin_tuples = list(zip(all_coins, all_tickers))
    start_date = dt.date(2016, 1, 1)
    end_date = dt.date(2018, 3, 2)
    date_list = [start_date + dt.timedelta(days=x) for x in range(0, (end_date - start_date).days)]
    for tup in coin_tuples:
        all_tweets = []
        df_dict = {}
        for i in range(0, len(date_list[0:10])):
            list_of_tweets = query_tweets(tup[0] + " OR #" + tup[1], \
            limit = 1000, begindate=date_list[i], enddate=date_list[i+1], poolsize = 1)
            all_tweets.append(len(list_of_tweets))
            print(all_tweets)
        df_dict["Twitter_Mentions"] = all_tweets
        df_dict["Dates"] = date_list[0:10]
        df = pd.DataFrame(df_dict)
        df.to_csv("dataframes/" + tup[0] + "_twitter.csv")
'''
