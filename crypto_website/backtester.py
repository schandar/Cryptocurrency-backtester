import pandas as pd
import numpy as np


def intersection_non_empty(set1, set2, set3, set4):
    '''
    Find the intersections of four sets.

    Inputs:
      set1 (set): the first set
      set2 (set): the second set
      set3 (set): the third set
      set4 (set): the fourth set

    Returns:
      intersected (set): a set that contains the elements that are in all
      four inputted sets
    '''

    param = [x for x in [set1, set2, set3, set4] if x]
    if not param:
        return set()
    intersected = set(param[0]).intersection(*param)
    return intersected


def filter_non_time_params(args_dic):
    '''
    Takes the non time to time dataframe and the argument dictionary to filter
    for the coins that meet all the non-time dependent parameters: whitepaper
    complexity, first letter of the coin, total reddit subscribers, and total
    twitter subscribers.

    Input:
      args_dic (dictionary): a dictionary that contains the user's inputs

    Returns:
      final_matched_coins (set): a set of all the indices of coins that match
      all the non-time dependent parameters
    '''

    matched_coins = set()
    whitepaper_coins = set()
    reddit_coins = set()
    twitter_coins = set()
    initial_elimination_df = pd.read_csv("Static_Params.csv")
    for i, coin in enumerate(initial_elimination_df["Coin_Name"]):
        if "letter" in args_dic:
            if coin[0].lower() == args_dic["letter"].lower():
                matched_coins.add(i)
        if "complexity_score" in args_dic:
            if initial_elimination_df["White_Complexity"].iloc[i] >= \
            args_dic["complexity_score"]:
                whitepaper_coins.add(i)
        if "Reddit_Subscribers_Total" in args_dic:
            if initial_elimination_df["Total_Reddit_Subscribers"].iloc[i] \
            >= args_dic["Reddit_Subscribers_Total"]:
                reddit_coins.add(i)
        if "Twitter_Mentions" in args_dic:
            if initial_elimination_df["Twitter_Mentions"].iloc[i] >= \
            args_dic["Twitter_Mentions"]:
                twitter_coins.add(i)
    final_matched_coins = intersection_non_empty(matched_coins, \
    whitepaper_coins, reddit_coins, twitter_coins)
    return final_matched_coins


def calculate_returns(cur_df):
    '''
    Calculates the percent returns in decimal form for a coin in the starting
    date and ending date as specified by the user.

    Input:
      cur_df: a sub-dataframe of a coin's entire dataframe that only contains
      the range of dates the user specified

    Returns:
      returns (float): the percent returns of the coin in decimal form
    '''

    start_val = cur_df["Price"].iloc[0]
    end_val = cur_df["Price"].iloc[-1]
    if start_val == 0:
        returns = None
    else:
        returns = ((end_val - start_val) / start_val)
    return returns


def meet_social_media_params(cur_df, args_dic, column_name):
    '''
    Calculates the percent change for Reddit subscribers or google
    trends in the date range specified by the user. Checks whether the
    change meets the parameter specified by the user.

    Inputs:
      cur_df: a sub-dataframe of a coin's entire dataframe that only contains
      the range of dates the user specified
      args_dic (dictionary): a dictionary that contains the user's inputs
      column_name (string): the column name of the social media parameter
      we are looking at in cur_df

    Returns:
      This function returns a boolean value to indicate whether or not the
      social media percent change meets the user's set input.
    '''

    if column_name in args_dic:
        start_val = cur_df[column_name].iloc[0]
        end_val = cur_df[column_name].iloc[-1]
        percent_change = ((end_val - start_val) / start_val) * 100
        if percent_change < args_dic[column_name]:
            return False
        else:
            return True
    else:
        return True


def social_media_filter(cur_df, args_dic):
    '''
    Checks if all social media parameters as set by the user are met.

    Inputs:
      cur_df: a sub-dataframe of a coin's entire dataframe that only contains
      the range of dates the user specified
      args_dic (dictionary): a dictionary that contains the user's inputs

    Returns:
      This function returns a boolean value that indicates whether all
      time-dependent social media parameters are met.
    '''

    google_meet_params = meet_social_media_params(cur_df, args_dic, \
    "Google_Trends")
    reddit_meet_params = meet_social_media_params(cur_df, args_dic, \
    "Reddit_Subscribers_Growth")
    if google_meet_params == True and reddit_meet_params == True:
        return True
    else:
        return False


def calculate_sharpe_ratio(cur_df):
    '''
    Calculates the sharpe ratio for a coin in the portfolio.

    Input:
      cur_df: a sub-dataframe of a coin's entire dataframe that only contains
      the range of dates the user specified

    Returns:
      sharpe_ratio (float): the sharpe ratio of the coin
    '''

    price_list = []
    returns_list = []
    for price in cur_df["Price"]:
        price_list.append(price)
    for i in range(len(price_list) - 1):
        daily_return = float(price_list[i]) / float(price_list[i + 1]) - 1
        returns_list.append(daily_return)
    duration_years = len(price_list) / 365
    mean = np.mean(returns_list)
    stand_dev = np.std(returns_list)
    ann_return = (1 + mean) ** (1 / duration_years) - 1
    risk_free = 0.02868  #This is the ten year treasury yield.
    sharpe_ratio = (ann_return - risk_free) / stand_dev
    return sharpe_ratio


def bitcoin_benchmark(args_dic):
    '''
    Calculates the percent returns in decimal form for Bitcoin in the date
    range specified by the user. This will be the benchmark with which we
    compare the returns of the user's portfolio.

    Input:
      args_dic (dictionary): a dictionary that contains the user's inputs

    Returns:
      returns (float): the percent returns in decimal form for Bitcoin
    '''

    bitcoin_df = pd.read_csv("final_coins/bitcoin.csv")
    start_date = args_dic["start_date"]
    start_index = pd.Index(bitcoin_df["Dates"]).get_loc(start_date)
    end_date = args_dic["end_date"]
    end_index = pd.Index(bitcoin_df["Dates"]).get_loc(end_date)
    specified_dates_df = bitcoin_df.loc[start_index: end_index]
    returns = calculate_returns(specified_dates_df)
    return returns


def filter_coins_for_output_calc(matched_coin_index, args_dic):
    '''
    Takes the indices of coins that meet the non-time dependent parameters
    specified by the users and further filters the portfolio to get only the
    coins that also meet the day to day parameters. Calculated the returns,
    benchmark returns, and sharpe ratio of the coins who meet all user
    inputs and were in existence in the date range the user specified.

    Inputs:
      matched_coin_index (set): a set of the indices of coins that match
      the non-time dependent parameters set by the user
      args_dic (dictionary): a dictionary that contains the user's inputs

    Returns:
      percent_returns (float): the percent returns of the coins in the
      portfolio when all coins are weighted equally
      benchmark_returns (float): the percent returns of the coins in the
      portfolio with Bitcoin returns as a benchmark
      sharpe_ratio (float): the average sharpe ratio of the coins in the
      portfolio
      final_output_ls (list): a list of the coins in the portfolio
    '''

    percent_returns = 0
    sharpe_ratio = 0
    final_output_ls = []
    all_coins_df = pd.read_csv("Updated_Cryptocoins.csv")
    for i in matched_coin_index:
        coin_name = all_coins_df["Name"].iloc[i].lower()
        cur_coin_df = pd.read_csv("final_coins/" + coin_name + ".csv")
        start_date = args_dic["start_date"]
        start_index = pd.Index(cur_coin_df["Dates"]).get_loc(start_date)
        end_date = args_dic["end_date"]
        end_index = pd.Index(cur_coin_df["Dates"]).get_loc(end_date)
        specified_dates_df = cur_coin_df.loc[start_index: end_index]
        meet_params = social_media_filter(specified_dates_df, args_dic)
        if meet_params == True:
            cur_returns = calculate_returns(specified_dates_df)
            if cur_returns is not None:
                percent_returns += cur_returns
                final_output_ls.append(coin_name)
            else:
                continue
            sharpe = calculate_sharpe_ratio(specified_dates_df)
            sharpe_ratio += sharpe
    if percent_returns == 0:
        return None
    percent_returns = percent_returns / len(final_output_ls)
    sharpe_ratio = sharpe_ratio / len(final_output_ls)
    bitcoin_returns = bitcoin_benchmark(args_dic)
    benchmark_returns = percent_returns - bitcoin_returns
    return percent_returns, benchmark_returns, sharpe_ratio, final_output_ls


def backtester(args_dic):
    '''
    This function is the backtester. We input the user's argument dictionary
    and find the coins that meet all parameters to test the user's strategy.

    Input:
      args_dic (dictionary): a dictionary that contains the user's inputs

    Returns:
      If one or more coins match the user's parameters, the functions returns
      If no coins match the user's parameters, the function returns a string
      that informs the user of this.
    '''

    matched_coin_index = filter_non_time_params(args_dic)
    output = filter_coins_for_output_calc(matched_coin_index, args_dic)
    if output != None:
        return [["Username", "Strategies", "Returns", "Benchmark Returns", \
        "Sharpe Ratio", "Portfolio"], [[args_dic["User_Name"], args_dic, \
        output[0], output[1], output[2], output[3]]]]
    else:
        return ["Your parameters do not match any coins. Please try again" + \
        " with different parameters."]
